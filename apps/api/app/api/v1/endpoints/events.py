from uuid import UUID

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.repositories.event_repository import get_event_by_id, list_events
from app.schemas.event import EventDetail, EventListItem, EventListResponse

router = APIRouter()


@router.get("", response_model=EventListResponse)
def list_events_endpoint(
    db: Session = Depends(get_db),
    layer_ids: list[int] | None = Query(None, description="Filter by layer id(s)"),
    region_code: str | None = Query(None, description="Region preset: WORLD, EUROPE, etc."),
    country_code: str | None = Query(None, description="ISO country code"),
    time_window: str | None = Query(None, description="24h, 7d, 30d"),
    source_class_id: int | None = Query(None, description="Filter by source class id"),
    trust_tier_id: int | None = Query(None, description="Filter by trust tier id"),
    min_lon: float | None = Query(None, description="Bbox min longitude"),
    min_lat: float | None = Query(None, description="Bbox min latitude"),
    max_lon: float | None = Query(None, description="Bbox max longitude"),
    max_lat: float | None = Query(None, description="Bbox max latitude"),
    limit: int = Query(500, ge=1, le=2000),
    offset: int = Query(0, ge=0),
):
    items, total = list_events(
        db,
        layer_ids=layer_ids,
        region_code=region_code,
        country_code=country_code,
        time_window=time_window,
        source_class_id=source_class_id,
        trust_tier_id=trust_tier_id,
        min_lon=min_lon,
        min_lat=min_lat,
        max_lon=max_lon,
        max_lat=max_lat,
        limit=limit,
        offset=offset,
    )
    return EventListResponse(
        items=[EventListItem(**x) for x in items],
        total=total,
    )


@router.get("/{event_id}", response_model=EventDetail)
def get_event_endpoint(event_id: UUID, db: Session = Depends(get_db)):
    event = get_event_by_id(db, event_id)
    if not event:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Event not found")
    return EventDetail(**event)
