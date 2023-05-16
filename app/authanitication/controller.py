from fastapi import FastAPI, APIRouter
import jwt

router = APIRouter()


@router.get("/decode_token")
async def decode_token(token: str):
    try:
        decoded_token = jwt.decode(token, verify=False)
        return {"decoded_token": decoded_token}
    except jwt.InvalidTokenError:
        return {"error": "Invalid token"}
