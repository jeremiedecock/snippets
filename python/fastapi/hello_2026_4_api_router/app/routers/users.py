from fastapi import APIRouter

router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.get("/")
async def read_users():
    return [{"username": "Rick"}, {"username": "Morty"}]


@router.get("/{username}")
async def read_user(username: str):
    return {"username": username}