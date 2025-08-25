from schema.bills import CreateBillSchema, CreateBillResponseSchema, AddItemToBillSchema
from models.bill import BillModel, BillItemModel
from models.auth import UserModel

class BillModelHelpers:

    @classmethod
    def create_bill(cls, user:UserModel = None, bill_data: CreateBillSchema = None):
        data = bill_data.model_dump()
        data["user"] = user.model_dump()
        if bill_data.items:
            items = []
            for item in bill_data.items:
                item_obj = BillItemModel(**item.model_dump())
                item_obj.save()
                items.append(item_obj)
            data["items"] = items

        bill_obj = BillModel(**data)
        bill_obj.save()
        return CreateBillResponseSchema.model_validate(bill_obj)