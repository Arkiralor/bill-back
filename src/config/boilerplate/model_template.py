from datetime import datetime, timezone
from pydantic import BaseModel, Field
from typing import Optional
from uuid import uuid4, UUID

from database import database

class TemplateModel(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()), alias="_id")
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: Optional[datetime] = Field(default=None)

    class Meta:
        collection_name: str = "template_collection"


    class Config:
        orm_mode = False
        allow_population_by_field_name = True

    def create(self, *args, **kwargs):
        if not self.created_at:
            self.created_at = datetime.now(timezone.utc)
        self.updated_at = datetime.now(timezone.utc)
        data = self.model_dump(by_alias=True)
        database[self.Meta.collection_name].insert_one(data)
        return self

    def save(self, *args, **kwargs):
        if not self.id:
            return self.create(*args, **kwargs)
        self.updated_at = datetime.now(timezone.utc)
        data = self.model_dump(by_alias=True)
        return database[self.Meta.collection_name].insert_one(data)