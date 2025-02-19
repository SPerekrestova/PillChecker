from pydantic import BaseModel, Field


class ProfileUpdateForm(BaseModel):
    display_name: str
    bio: str = Field(..., max_length=500)
