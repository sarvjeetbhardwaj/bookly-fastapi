from pydantic import BaseModel, Field
import uuid
from datetime import datetime as dt
from typing import Optional

class ReviewModel(BaseModel):
    uid : uuid.UUID 
    rating : int = Field(lt=5)
    rating_text : str
    user_uid : Optional[uuid.UUID] 
    book_uid : Optional[uuid.UUID] 
    created_at : dt 
    updated_at : dt 

class ReviewCreateModel(BaseModel):
    rating : int = Field(lt=5)
    rating_text : str




