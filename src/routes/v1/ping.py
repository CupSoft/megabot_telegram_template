from fastapi import APIRouter, status

router = APIRouter()


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
)
async def ping():
    return {"ping": "Pong!"}
