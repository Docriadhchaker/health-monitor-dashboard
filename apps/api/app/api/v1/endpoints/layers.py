from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models import Layer

router = APIRouter()


@router.get("")
def list_layers(db: Session = Depends(get_db)):
    layers = db.query(Layer).order_by(Layer.sort_order).all()
    return {
        "items": [
            {"id": l.id, "code": l.code, "name": l.name, "sort_order": l.sort_order}
            for l in layers
        ]
    }
