from sqlmodel.ext.asyncio.session import AsyncSession
from .schemas import BookCreateModel, BookUpdateModel, Book
from sqlmodel import select, desc


class BookService: 
    async def get_all_books(self, session:AsyncSession):
        statement = select(Book).order_by(desc(Book.created_at))
        result = await session.exec(statement=statement)

        return result.all()

    async def get_book(self, book_uid:str, session:AsyncSession):
        statement = select(Book).where(Book.uid == book_uid)

        result = await session.exec(statement=statement)

        return result.first()

    async def create_book(self, book_data:BookCreateModel, session:AsyncSession):
        book_data_dict = book_data.model_dump()

        new_book = Book(**book_data_dict)

        session.add(new_book)

        session.commit()

        return new_book

    async def update_book(self, book_uid:str, update_book_data:BookUpdateModel, session:AsyncSession):
        pass

    async def delete_book(self, book_uid:str, session:AsyncSession):
        pass    