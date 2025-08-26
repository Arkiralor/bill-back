from config.boilerplate.model_template import TemplateModel
from pydantic import Field
from typing import List, Optional
from auth_app.models import UserModel

class BillItemModel(TemplateModel):
    name: str = Field(...)
    description: Optional[str] = Field(default=None)

    class Meta:
        collection_name: str = "bill_items"

    class Config:
        from_attributes = True
        validate_by_name = True

    def save(self, *args, **kwargs):
        self.name = self.name.strip().title()
        if self.description:
            self.description = self.description.strip()
        return super(self, BillItemModel).save(*args, **kwargs)


class BillModel(TemplateModel):
    user: UserModel = Field(...)
    customer_name: str = Field(...)
    customer_email: Optional[str] = Field(default=None)
    customer_address: str = Field(...)
    customer_phone: str = Field(...)
    items: Optional[List[BillItemModel]] = Field(default=None)

    class Meta:
        collection_name: str = "bills"

    class Config:
        from_attributes = True
        validate_by_name = True

    def save(self, *args, **kwargs):
        self.customer_name = self.customer_name.strip().title()
        if self.customer_email:
            self.customer_email = self.customer_email.strip().lower()
        self.customer_address = self.customer_address.strip()
        self.customer_phone = self.customer_phone.strip()
        return super(self, BillModel).save(*args, **kwargs)

