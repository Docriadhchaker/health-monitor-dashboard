from fastapi import APIRouter

router = APIRouter()


@router.get("")
def api_health():
    return {"status": "ok", "service": "api"}
