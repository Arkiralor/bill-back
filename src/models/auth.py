from datetime import datetime

from config.boilerplate.model_template import TemplateModel
from pydantic import Field, EmailStr
from typing import List, Optional

class UserModel(TemplateModel):
    username: str = Field(...)
    email: EmailStr = Field(...)
    is_active: bool = Field(default=True)
    is_superuser: bool = Field(default=False)
    password:str = Field(..., max_length=256)

    last_login: Optional[datetime] = Field(default=None)
    login_attempts: int = Field(default=0)
    blocked_until: Optional[datetime] = Field(default=None)
    

    class Meta:
        collection_name: str = "users"

    class Config:
        orm_mode = True
        allow_population_by_field_name = True

    def save(self, *args, **kwargs):
        self.username = self.username.strip().lower()
        self.email = self.email.strip().lower()
        return super(UserModel, self).save(*args, **kwargs)