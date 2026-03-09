from fastapi import APIRouter

router = APIRouter()


@router.get("/{event_id}")
def get_event_translations(event_id: str):
    return {"event_id": event_id, "translations": []}
