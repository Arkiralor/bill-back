from bill_app.schema import CreateBillSchema, CreateBillResponseSchema, AddItemToBillSchema
from bill_app.models import BillModel, BillItemModel
from auth_app.models import UserModel

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
        return CreateBillResponseSchema(**bill_obj.model_dump())