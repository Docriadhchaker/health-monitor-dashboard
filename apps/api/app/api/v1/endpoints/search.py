from fastapi import APIRouter

router = APIRouter()


@router.get("")
def search_events():
    return {"items": [], "total": 0}
