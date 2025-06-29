from fastapi import APIRouter, Depends, status,BackgroundTasks
from src.auth.schemas import (
    UserCreateModel, UserModel, UserLoginModel, UserBooksModel, EmailModel,
    PassWordResetRequestModel, PasswordResetconfirmModel)
from src.auth.service import UserService
from src.db.create_engine import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi.exceptions import HTTPException
from src.auth.utils import (
    create_access_token, decode_token, verify_password, create_url_safe_token, decode_url_safe_token,
    generate_password_hash
)
from datetime import timedelta, datetime
from fastapi.responses import JSONResponse
from src.auth.dependencies import RefreshTokenBearer, AccessTokenBearer, get_current_user, RoleChecker
from src.mail import mail, create_message
from src.config import config
from src.celery_tasks import send_email

#from src.db.redis import add_jti_to_blocklist

auth_router = APIRouter()
user_service = UserService()
role_checker = RoleChecker(allowed_roles=['admin', 'user'])

REFRESH_TOKEN_EXPIRY = 2

@auth_router.post('/send_mail')
async def send_mail(emails:EmailModel,bg_task:BackgroundTasks):
    emails = emails.email_addresses
    subject = 'Welcome to our app'
    html ="<h1>Welcome to the app </h1>"

    #message = create_message(recepients=emails, subject='Welcome',body=html)
    #bg_task.add_task(mail.send_message, message) ## async task

    send_email.delay(emails=emails,subject=subject, body=html ) ## celery task

    return {'message' : 'Email sent successfully'}

@auth_router.post('/signup', status_code=status.HTTP_201_CREATED)
async def create_user_account(user_data:UserCreateModel, bg_task:BackgroundTasks,
                              session: AsyncSession=Depends(get_session)):
    email = user_data.email

    user_exists = await user_service.user_exists(email=email, session=session)

    if user_exists:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='User with email already exists')
    
    new_user = await user_service.create_user(user_data=user_data, session=session)

    token =  create_url_safe_token(data={'email':email})
    
    link = f'http://{config.DOMAIN}/{token}'

    html_message = f'''
                    <h1>Verify your email </h1>
                    <p>Please click this <a href="{link}">link</a> to verify you email </p>
                '''
    
    message = create_message(recepients=[email], subject='Verify your email address',body=html_message)

    bg_task.add_task(mail.send_message, message)

    return {
        'message': 'Account Created ! Check email to verify your account',
         "user":new_user
    }

@auth_router.get('/verify/{token}')
async def verify_user_account(token:str, session:AsyncSession=Depends(get_session)):
    token_data = decode_url_safe_token(token=token)
    user_email = token_data.get('email')

    if user_email:
        user = await user_service.get_user_by_email(email=user_email, session=session)

        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={'message': 'User not found'})
        
        await user_service.update_user(user=user, user_data={'is_verified':True} , session=session)

        return JSONResponse(content={'message': 'Account verified successfully'},
                            status_code=status.HTTP_200_OK)
    
    return JSONResponse(content={'message' : 'Error occured furing verification'},
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@auth_router.post('/login')
async def login_users(login_data:UserLoginModel, session:AsyncSession = Depends(get_session)):
    email = login_data.email
    password = login_data.password

    user = await user_service.get_user_by_email(email=email, session=session)

    if user is not None:
        password_valid = verify_password(password=password, hash=user.password_hash)

        if password_valid:
            access_token = create_access_token(user_data={'email': user.email, 'user_uid': str(user.uid),
                                                          'role': user.role})

            refresh_token = create_access_token(user_data={'email': user.email, 'user_uid': str(user.uid)},
                                                refresh=True, expiry=timedelta(days=REFRESH_TOKEN_EXPIRY))
            
            return JSONResponse(content={'message': 'Login_Successful',
                                         'access_token': access_token,
                                         'refresh_token': refresh_token,
                                         'user' : {
                                            'email': user.email,
                                            'uid' : str(user.uid)   
                                         }})
        
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Invalid Email or Password')

@auth_router.get('/refresh_token')
async def get_new_access_token(token_details:dict = Depends(RefreshTokenBearer())):

    expiry_timestamp = token_details['exp']

    if datetime.fromtimestamp(expiry_timestamp) > datetime.now():
        new_access_token = create_access_token(user_data=token_details['user'])
        return JSONResponse(content={'access_token':new_access_token})

    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Invalid or expired token')

#@auth_router.get('/logout')
#async def revoke_token(token_details:dict=Depends(AccessTokenBearer())):
#    jti = token_details['jti']
#
#    await add_jti_to_blocklist(jti=jti)

#    return JSONResponse(content={'message': 'Logged our Success'},
#                        status_code=status.HTTP_200_OK)



@auth_router.get('/me', response_model=UserBooksModel)
async def get_curr_user(user = Depends(get_current_user), _:bool=Depends(role_checker)):
    return user


@auth_router.post('/password_reset_request')
async def password_reset_request(email_data:PassWordResetRequestModel,bg_task:BackgroundTasks):
    email = email_data.email

    token =  create_url_safe_token(data={'email':email})
    
    link = f'http://{config.DOMAIN}/password-verify/{token}'

    html_message = f'''
                    <h1>Verify your email </h1>
                    <p>Please click this <a href="{link}">link</a> to verify you email </p>
                '''
    
    message = create_message(recepients=[email], subject='Reset your password',body=html_message)

    bg_task.add_task(mail.send_message, message)

    return JSONResponse(content={'message': 'Check your email for instrauction to reset your password'},
                        status_code=status.HTTP_200_OK)



@auth_router.post('/password-verify/{token}')
async def reset_account_password(token:str, password:PasswordResetconfirmModel , 
                                 session:AsyncSession=Depends(get_session)):
    
    new_password = password.new_password
    confirm_password = password.confirm_new_password

    if new_password != confirm_password:
        raise HTTPException(detail='Password Donot Match', status_code=status.HTTP_400_BAD_REQUEST)
    
    token_data = decode_url_safe_token(token=token)
    user_email = token_data.get('email')

    if user_email:
        user = await user_service.get_user_by_email(email=user_email, session=session)

        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={'message': 'User not found'})
        
        password_hash = generate_password_hash(password=new_password)
        await user_service.update_user(user=user, user_data={'password_hash':password_hash} , session=session)

        return JSONResponse(content={'message': 'Password Reset Successfully'},
                            status_code=status.HTTP_200_OK)
    
    return JSONResponse(content={'message' : 'Error occured during password request'},
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)