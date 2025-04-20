from src.review.models import Review
from src.auth.service import UserService
from src.books.service import BookService
from sqlmodel.ext.asyncio.session import AsyncSession
from src.review.schemas import ReviewCreateModel
from fastapi.exceptions import HTTPException
from fastapi import status

book_service = BookService()
user_service = UserService()

class ReviewService:
    async def add_review_to_book(self, user_email:str, book_uid:str, review_data:ReviewCreateModel, 
                                 session:AsyncSession):
        try:
            book = await book_service.get_book(book_uid=book_uid, session=session)
            user = await user_service.get_user_by_email(email=user_email, session=session)

            if not book:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Book not found')
            
            if not user:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')
            
            review_data_dict = review_data.model_dump()

            new_review = Review(**review_data_dict)

            new_review.user = user
            new_review.book = book

            session.add(new_review)

            await session.commit()

            return new_review
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail='Oops .... something went wrong')