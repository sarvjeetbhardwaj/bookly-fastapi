from fastapi import APIRouter, Depends
from src.auth.models import User
from src.review.schemas import ReviewCreateModel, ReviewModel
from src.db.create_engine import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from src.review.service import ReviewService
from src.auth.dependencies import get_current_user



review_service = ReviewService()
review_router = APIRouter()

@review_router.post('/review/book/{book_uid}')
async def add_review_to_book(book_uid:str, review_data:ReviewCreateModel, current_user:User= Depends(get_current_user),
                             session:AsyncSession=Depends(get_session)):
    new_review = await review_service.add_review_to_book(user_email=current_user.email, review_data=review_data,
                                                         session=session, book_uid=book_uid )
    print(new_review)
    return new_review
    