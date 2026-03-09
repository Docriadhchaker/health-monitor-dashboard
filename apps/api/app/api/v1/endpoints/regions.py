from fastapi import APIRouter

router = APIRouter()


@router.get("")
def list_region_presets():
    return {"items": ["World", "Americas", "MENA", "Europe", "Asia", "Africa", "Oceania"]}
