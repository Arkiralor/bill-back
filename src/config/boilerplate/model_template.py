from datetime import datetime, timezone
from pydantic import BaseModel, Field
from typing import Optional
from uuid import uuid4, UUID

from database import database


class TemplateModel(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()), alias="_id")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: Optional[datetime] = Field(default=None)

    class Meta:
        collection_name: str = "template_collection"

    class Config:
        from_attributes = False
        validate_by_name = True

    # def create(self, *args, **kwargs):
    #     if not self.created_at:
    #         self.created_at = datetime.now(timezone.utc)
    #     self.updated_at = datetime.now(timezone.utc)
    #     data = self.model_dump(by_alias=True)
    #     database[self.Meta.collection_name].insert_one(data)
    #     return self

    def create(self, *args, **kwargs):
        now = datetime.now(timezone.utc)
        if not self.created_at:
            self.created_at = now
        self.updated_at = now

        data = self.model_dump(by_alias=True)
        result = database[self.Meta.collection_name].insert_one(data)

        # if Mongo assigned an _id (you’re overriding with str(uuid4()), but still safe)
        if result.inserted_id and not self.id:
            self.id = str(result.inserted_id)

        return self

    # def save(self, *args, **kwargs):
    #     if not self.id:
    #         return self.create(*args, **kwargs)
    #     self.updated_at = datetime.now(timezone.utc)
    #     data = self.model_dump(by_alias=True)
    #     return database[self.Meta.collection_name].insert_one(data)

    def save(self, *args, **kwargs):
        coll = database[self.Meta.collection_name]

        if not self.id:  # create new if no id
            return self.create(*args, **kwargs)

        self.updated_at = datetime.now(timezone.utc)
        data = self.model_dump(by_alias=True)
        coll.update_one({"_id": self.id}, {"$set": data}, upsert=True)
        return self
