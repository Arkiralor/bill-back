from fastapi.routing import APIRouter
from schema.bills import CreateBillSchema, CreateBillResponseSchema, AddItemToBillSchema

router = APIRouter(prefix="/bills", tags=["bills"])


@router.get("/list/")
async def list_bills():
    return {"bills": []}


@router.post("/create/", response_model=CreateBillResponseSchema)
async def create_bill(bill: CreateBillSchema):
    return {"message": "Bill created"}


@router.get("/{bill_id}/")
async def get_bill(bill_id: int):
    return {"bill_id": bill_id, "details": "Bill details here"}


@router.delete("/{bill_id}/")
async def delete_bill(bill_id: int):
    return {"message": f"Bill {bill_id} deleted"}


@router.patch("/{bill_id}/", response_model=CreateBillResponseSchema)
async def add_items_to_bill(bill_id: int, items: AddItemToBillSchema):
    return {"message": f"Items added to bill {bill_id}"}


@router.put("/{bill_id}/")
async def update_bill(bill_id: int):
    return {"message": f"Bill {bill_id} updated"}
