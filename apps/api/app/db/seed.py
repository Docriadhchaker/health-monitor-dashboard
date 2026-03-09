"""
Seed taxonomy and reference data: layers, source_classes, trust_tiers,
evidence_statuses, specialties, jurisdictions (region presets).
Then seed sample events for Phase 2 vertical slice.
Run from repo root: cd apps/api && uv run python -m app.db.seed
"""
import hashlib
import os
import sys
import uuid
from datetime import datetime, timezone

# Ensure app is importable when run as module from apps/api
sys.path.insert(0, os.path.realpath(os.path.dirname(__file__) + "/../.."))

from geoalchemy2.elements import WKTElement

from app.db.session import SessionLocal
from app.models import (
    EvidenceStatus,
    Event,
    EventSourceLink,
    EventTranslation,
    IngestionRun,
    Jurisdiction,
    Layer,
    RawDocument,
    SourceClass,
    SourceFeed,
    SourceProvider,
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


# --- Phase 2: sample providers, feeds, runs, events ---
PROVIDERS = [
    ("who", "World Health Organization", 1, 1, "https://www.who.int"),
    ("ecdc", "European Centre for Disease Prevention and Control", 1, 1, "https://www.ecdc.europa.eu"),
    ("pubmed", "PubMed / NCBI", 2, 1, "https://pubmed.ncbi.nlm.nih.gov"),
    ("medrxiv", "medRxiv / bioRxiv", 3, 3, "https://www.medrxiv.org"),
    ("fda", "FDA Drug Safety", 4, 1, "https://www.fda.gov"),
]

# (layer_code, provider_slug, title, summary_en, country_code, region_code, location_name, lon, lat, evidence_code, with_fr_translation)
SAMPLE_EVENTS = [
    ("PUB_HEALTH", "who", "Weekly cholera outbreak update — Eastern Mediterranean", "WHO reports an update on cholera cases in the Eastern Mediterranean region with case counts and affected countries.", "EG", "MENA", "Cairo", 31.2357, 30.0444, "SURVEILLANCE_REPORT", True),
    ("PUB_HEALTH", "ecdc", "Seasonal influenza surveillance summary — Europe", "ECDC publishes the weekly influenza surveillance summary for the WHO European region.", None, "EUROPE", "Stockholm", 18.0686, 59.3293, "SURVEILLANCE_REPORT", False),
    ("PUB_HEALTH", "who", "Dengue situation report — Americas", "WHO reports on the dengue situation in the Americas region.", "BR", "AMERICAS", "Brasília", -47.8825, -15.7942, "SURVEILLANCE_REPORT", True),
    ("PUB_HEALTH", "ecdc", "COVID-19 variant update", "ECDC issues an update on SARS-CoV-2 variant circulation in the EU/EEA.", None, "EUROPE", "Brussels", 4.3517, 50.8503, "SURVEILLANCE_REPORT", False),
    ("GUIDELINES", "who", "Updated guideline on tuberculosis treatment", "WHO releases an updated guideline on the treatment of drug-susceptible tuberculosis.", None, "WORLD", None, None, None, "GUIDELINE", True),
    ("GUIDELINES", "ecdc", "Guidance on infection prevention in healthcare", "ECDC publishes guidance on infection prevention and control in healthcare settings.", None, "EUROPE", None, None, None, "GUIDELINE", False),
    ("LITERATURE", "pubmed", "Meta-analysis of vaccine effectiveness against influenza", "A meta-analysis evaluates vaccine effectiveness against seasonal influenza in adults.", "US", "AMERICAS", "Bethesda", -77.1025, 38.9897, "PEER_REVIEWED_ARTICLE", False),
    ("LITERATURE", "pubmed", "Cohort study on long COVID in European population", "A cohort study describes the prevalence of long COVID in a European population.", None, "EUROPE", "London", -0.1276, 51.5074, "PEER_REVIEWED_ARTICLE", True),
    ("LITERATURE", "pubmed", "Randomized trial of new antiviral for respiratory infection", "A randomized controlled trial reports on the efficacy of a new antiviral for respiratory infection.", "JP", "ASIA", "Tokyo", 139.6917, 35.6892, "PEER_REVIEWED_ARTICLE", False),
    ("PREPRINTS", "medrxiv", "Preprint: SARS-CoV-2 wastewater surveillance sensitivity", "A preprint presents a model for wastewater-based surveillance sensitivity for SARS-CoV-2.", "AU", "OCEANIA", "Sydney", 151.2093, -33.8688, "PREPRINT", True),
    ("PREPRINTS", "medrxiv", "Preprint: Novel biomarker for sepsis outcome", "A preprint describes a novel biomarker associated with sepsis outcome in ICU patients.", "ZA", "AFRICA", "Cape Town", 18.4241, -33.9249, "PREPRINT", False),
    ("PREPRINTS", "medrxiv", "Preprint: Vaccine hesitancy survey in MENA", "A preprint reports survey results on vaccine hesitancy in selected MENA countries.", "JO", "MENA", "Amman", 35.9300, 31.9454, "PREPRINT", False),
    ("PHARMACOVIGILANCE", "fda", "Drug safety communication: label change for anticoagulant", "FDA announces a label change for an anticoagulant following postmarket data review.", "US", "AMERICAS", "Silver Spring", -76.9375, 38.9959, "REGULATORY_NOTICE", True),
    ("PHARMACOVIGILANCE", "fda", "Recall: certain lots of sterile injectable", "FDA reports a recall of certain lots of a sterile injectable product due to particulate matter.", "US", "AMERICAS", None, None, None, "REGULATORY_NOTICE", False),
    ("PHARMACOVIGILANCE", "ecdc", "Signal assessment: new adverse event for vaccine", "ECDC publishes a signal assessment for a potential adverse event following immunization.", None, "EUROPE", "Stockholm", 18.0686, 59.3293, "REGULATORY_NOTICE", False),
]


def _id_by_code(db, model, code_attr, code_val):
    row = db.query(model).filter(getattr(model, code_attr) == code_val).first()
    return row.id if row else None


def seed_providers_feeds_runs(db):
    if db.query(SourceProvider).first():
        return
    layer1 = db.query(Layer).filter(Layer.code == "PUB_HEALTH").first()
    if not layer1:
        return
    providers = {}
    feeds = {}
    runs = {}
    for slug, name, sc_id, tt_id, homepage in PROVIDERS:
        pid = uuid.uuid4()
        db.add(
            SourceProvider(
                id=pid,
                name=name,
                slug=slug,
                source_class_id=sc_id,
                trust_tier_id=tt_id,
                homepage_url=homepage,
                is_active=True,
            )
        )
        providers[slug] = pid
    db.commit()

    for slug, name, sc_id, tt_id, _ in PROVIDERS:
        pid = providers[slug]
        layer_id = _id_by_code(db, Layer, "code", "PUB_HEALTH")
        if slug == "pubmed":
            layer_id = _id_by_code(db, Layer, "code", "LITERATURE")
        elif slug == "medrxiv":
            layer_id = _id_by_code(db, Layer, "code", "PREPRINTS")
        elif slug == "fda":
            layer_id = _id_by_code(db, Layer, "code", "PHARMACOVIGILANCE")
        fid = uuid.uuid4()
        db.add(
            SourceFeed(
                id=fid,
                provider_id=pid,
                name=f"{name} feed",
                feed_type="api",
                endpoint_url=f"https://example.com/{slug}",
                default_layer_id=layer_id or 1,
                polling_interval_minutes=60,
                is_active=True,
            )
        )
        feeds[slug] = fid
    db.commit()

    for slug in feeds:
        fid = feeds[slug]
        rid = uuid.uuid4()
        now = datetime.now(timezone.utc)
        db.add(
            IngestionRun(
                id=rid,
                source_feed_id=fid,
                status="success",
                started_at=now,
                finished_at=now,
                records_fetched=0,
                records_inserted=0,
                records_promoted=0,
            )
        )
        runs[slug] = rid
    db.commit()
    print("Seeded providers, feeds, ingestion runs.")


def seed_sample_events(db):
    if db.query(Event).first():
        return
    layers = {r.code: r.id for r in db.query(Layer).all()}
    providers = {r.slug: r.id for r in db.query(SourceProvider).all()}
    evidence = {r.code: r.id for r in db.query(EvidenceStatus).all()}
    trust_tiers = {r.code: r.id for r in db.query(TrustTier).all()}
    feed_by_provider = {str(f.provider_id): f.id for f in db.query(SourceFeed).all()}
    run_by_feed = {}
    for r in db.query(IngestionRun).all():
        run_by_feed[str(r.source_feed_id)] = r.id

    for layer_code, prov_slug, title, summary_en, country_code, region_code, location_name, lon, lat, evidence_code, with_fr in SAMPLE_EVENTS:
        provider_id = providers.get(prov_slug)
        if not provider_id:
            continue
        layer_id = layers.get(layer_code, 1)
        evidence_id = evidence.get(evidence_code, 1)
        tt_id = trust_tiers.get("HIGH", 1)
        if prov_slug == "medrxiv":
            tt_id = trust_tiers.get("EXPLORATORY", 3)

        feed_id = feed_by_provider.get(str(provider_id))
        run_id = run_by_feed.get(str(feed_id)) if feed_id else None
        if not run_id or not feed_id:
            continue

        raw_id = uuid.uuid4()
        url = f"https://example.com/source/{raw_id}"
        payload = {"title": title, "url": url}
        content_hash = hashlib.sha256(url.encode()).hexdigest()[:128]
        db.add(
            RawDocument(
                id=raw_id,
                ingestion_run_id=run_id,
                source_feed_id=feed_id,
                provider_id=provider_id,
                original_title=title,
                original_url=url,
                raw_payload_json=payload,
                content_hash=content_hash,
                parsing_status="parsed",
            )
        )

        event_id = uuid.uuid4()
        location_point = None
        if lon is not None and lat is not None:
            location_point = WKTElement(f"POINT({lon} {lat})", srid=4326)
        region_val = region_code if region_code and region_code != "WORLD" else None
        db.add(
            Event(
                id=event_id,
                layer_id=layer_id,
                primary_provider_id=provider_id,
                evidence_status_id=evidence_id,
                trust_tier_id=tt_id,
                title=title,
                summary_en=summary_en,
                geographic_scope="regional" if region_val else "global",
                country_code=country_code,
                region_code=region_val,
                location_name=location_name,
                location_point=location_point,
                visibility_status="visible",
                is_active=True,
            )
        )
        db.add(
            EventSourceLink(
                id=uuid.uuid4(),
                event_id=event_id,
                raw_document_id=raw_id,
                provider_id=provider_id,
                relationship_type="primary",
                is_display_source=True,
            )
        )
        if with_fr and summary_en:
            db.add(
                EventTranslation(
                    id=uuid.uuid4(),
                    event_id=event_id,
                    language_code="fr",
                    translated_summary=f"[FR] {summary_en[:80]}…",
                    translation_provider="deepl",
                    is_machine_translated=True,
                )
            )
    db.commit()
    print("Seeded sample events.")


def main() -> None:
    db = SessionLocal()
    try:
        seed_layers(db)
        seed_source_classes(db)
        seed_trust_tiers(db)
        seed_evidence_statuses(db)
        seed_specialties(db)
        seed_jurisdictions(db)
        seed_providers_feeds_runs(db)
        seed_sample_events(db)
        print("Seed complete.")
    finally:
        db.close()


if __name__ == "__main__":
    main()
