"""
Seed taxonomy and reference data: layers, source_classes, trust_tiers,
evidence_statuses, specialties, jurisdictions (region presets).
Run from repo root: cd apps/api && uv run python -m app.db.seed
"""
import os
import sys
import uuid

# Ensure app is importable when run as module from apps/api
sys.path.insert(0, os.path.realpath(os.path.dirname(__file__) + "/../.."))

from app.db.session import SessionLocal
from app.models import (
    EvidenceStatus,
    Jurisdiction,
    Layer,
    SourceClass,
    Specialty,
    TrustTier,
)


LAYERS = [
    ("PUB_HEALTH", "Public Health / Surveillance", 1),
    ("GUIDELINES", "Guidelines / Official Updates", 2),
    ("LITERATURE", "Scientific Literature", 3),
    ("PREPRINTS", "Preprints", 4),
    ("PHARMACOVIGILANCE", "Pharmacovigilance / Drug Safety", 5),
]

SOURCE_CLASSES = [
    ("OFFICIAL_AUTHORITY", "Official Authority"),
    ("SCIENTIFIC_DATABASE", "Scientific Database"),
    ("PREPRINT_SERVER", "Preprint Server"),
    ("REGULATORY_DATABASE", "Regulatory Database"),
    ("MEDIA", "Media"),
]

TRUST_TIERS = [
    ("HIGH", "High", 1),
    ("MODERATE", "Moderate", 2),
    ("EXPLORATORY", "Exploratory", 3),
]

EVIDENCE_STATUSES = [
    ("SURVEILLANCE_REPORT", "Surveillance Report"),
    ("GUIDELINE", "Guideline"),
    ("PEER_REVIEWED_ARTICLE", "Peer-Reviewed Article"),
    ("PREPRINT", "Preprint"),
    ("REGULATORY_NOTICE", "Regulatory Notice"),
    ("MEDIA_REPORT", "Media Report"),
]

SPECIALTIES = [
    ("infectious_disease", "Infectious Disease"),
    ("pharmacy", "Pharmacy"),
    ("laboratory_medicine", "Laboratory Medicine"),
    ("oncology", "Oncology"),
    ("public_health", "Public Health"),
]

JURISDICTIONS = [
    ("WORLD", "World", "global", None),
    ("AMERICAS", "Americas", "region", None),
    ("MENA", "MENA", "region", None),
    ("EUROPE", "Europe", "region", None),
    ("ASIA", "Asia", "region", None),
    ("AFRICA", "Africa", "region", None),
    ("OCEANIA", "Oceania", "region", None),
]


def seed_layers(db):
    if db.query(Layer).first():
        return
    for code, name, sort_order in LAYERS:
        db.add(Layer(code=code, name=name, sort_order=sort_order))
    db.commit()
    print("Seeded layers.")


def seed_source_classes(db):
    if db.query(SourceClass).first():
        return
    for code, name in SOURCE_CLASSES:
        db.add(SourceClass(code=code, name=name))
    db.commit()
    print("Seeded source_classes.")


def seed_trust_tiers(db):
    if db.query(TrustTier).first():
        return
    for code, name, sort_order in TRUST_TIERS:
        db.add(TrustTier(code=code, name=name, sort_order=sort_order))
    db.commit()
    print("Seeded trust_tiers.")


def seed_evidence_statuses(db):
    if db.query(EvidenceStatus).first():
        return
    for code, name in EVIDENCE_STATUSES:
        db.add(EvidenceStatus(code=code, name=name))
    db.commit()
    print("Seeded evidence_statuses.")


def seed_specialties(db):
    if db.query(Specialty).first():
        return
    for code, name in SPECIALTIES:
        db.add(Specialty(id=uuid.uuid4(), code=code, name=name))
    db.commit()
    print("Seeded specialties.")


def seed_jurisdictions(db):
    if db.query(Jurisdiction).first():
        return
    for code, name, j_type, country in JURISDICTIONS:
        db.add(Jurisdiction(id=uuid.uuid4(), code=code, name=name, jurisdiction_type=j_type, country_code=country))
    db.commit()
    print("Seeded jurisdictions (region presets).")


def main() -> None:
    db = SessionLocal()
    try:
        seed_layers(db)
        seed_source_classes(db)
        seed_trust_tiers(db)
        seed_evidence_statuses(db)
        seed_specialties(db)
        seed_jurisdictions(db)
        print("Seed complete.")
    finally:
        db.close()


if __name__ == "__main__":
    main()
