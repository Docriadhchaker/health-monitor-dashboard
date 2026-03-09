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

# --- Curated real-source demo events (replaceable later by real ingestion) ---
# One-to-one alignment: each source_url points to a single real page; title is that page's
# exact title or a faithful short version; summary describes that exact document only.
# source_published_at = real publication date of that source (no artificial "recent" dates).

CURATED_DEMO_EVENTS = [
    # Public Health / Surveillance — one specific document per event
    {
        "layer_code": "PUB_HEALTH",
        "provider_slug": "who",
        "title": "Data show marked increase in annual cholera deaths",
        "summary_en": "WHO news item on 2023 global cholera statistics: 13% rise in cases and 71% rise in deaths; 45 countries reported cases; geographic shift with large increase in Africa.",
        "source_url": "https://www.who.int/news/item/04-09-2024-data-show-marked-increase-in-annual-cholera-deaths",
        "source_published_at": "2024-09-04",
        "country_code": None,
        "region_code": "WORLD",
        "location_name": None,
        "lon": None,
        "lat": None,
        "evidence_code": "SURVEILLANCE_REPORT",
        "with_fr": True,
    },
    {
        "layer_code": "PUB_HEALTH",
        "provider_slug": "ecdc",
        "title": "Zoonotic influenza - Annual Epidemiological Report 2024",
        "summary_en": "ECDC annual report on zoonotic influenza in the EU/EEA for 2024: human infections with avian and swine influenza viruses reported by nine countries; no cases in EU/EEA in 2024.",
        "source_url": "https://www.ecdc.europa.eu/en/publications-data/zoonotic-influenza-annual-epidemiological-report-2024",
        "source_published_at": "2026-01-21",
        "country_code": None,
        "region_code": "EUROPE",
        "location_name": "Stockholm",
        "lon": 18.0686,
        "lat": 59.3293,
        "evidence_code": "SURVEILLANCE_REPORT",
        "with_fr": False,
    },
    {
        "layer_code": "PUB_HEALTH",
        "provider_slug": "ecdc",
        "title": "Measles - Annual Epidemiological Report for 2024",
        "summary_en": "ECDC annual epidemiological report on measles in the EU/EEA for 2024: 35 212 cases reported, a ten-fold increase from 2023; return to seasonal pattern after 2021–2023.",
        "source_url": "https://www.ecdc.europa.eu/en/publications-data/measles-annual-epidemiological-report-2024",
        "source_published_at": "2025-04-28",
        "country_code": None,
        "region_code": "EUROPE",
        "location_name": "Stockholm",
        "lon": 18.0686,
        "lat": 59.3293,
        "evidence_code": "SURVEILLANCE_REPORT",
        "with_fr": False,
    },
    # Guidelines — one specific publication per event
    {
        "layer_code": "GUIDELINES",
        "provider_slug": "who",
        "title": "WHO consolidated guidelines on tuberculosis. Module 4: treatment - drug-resistant tuberculosis treatment, 2022 update",
        "summary_en": "WHO guideline on drug-resistant TB treatment: recommendations for 6-month BPaLM and 9-month all-oral regimens, monitoring, ART timing, and surgery; for use by Member States.",
        "source_url": "https://www.who.int/publications/i/item/9789240063129",
        "source_published_at": "2022-06-15",
        "country_code": None,
        "region_code": "WORLD",
        "location_name": None,
        "lon": None,
        "lat": None,
        "evidence_code": "GUIDELINE",
        "with_fr": True,
    },
    # Scientific Literature — one article per event (title and summary match that article)
    {
        "layer_code": "LITERATURE",
        "provider_slug": "pubmed",
        "title": "Effectiveness of influenza vaccination to prevent severe disease: a systematic review and meta-analysis of test-negative design studies",
        "summary_en": "Systematic review and meta-analysis of test-negative design studies evaluating influenza vaccine effectiveness against severe influenza outcomes.",
        "source_url": "https://pubmed.ncbi.nlm.nih.gov/41093140/",
        "source_published_at": "2024-03-01",
        "country_code": "US",
        "region_code": "AMERICAS",
        "location_name": "Bethesda",
        "lon": -77.1025,
        "lat": 38.9897,
        "evidence_code": "PEER_REVIEWED_ARTICLE",
        "with_fr": False,
    },
    {
        "layer_code": "LITERATURE",
        "provider_slug": "pubmed",
        "title": "Interim Estimates of 2024-2025 Seasonal Influenza Vaccine Effectiveness - Four Vaccine Effectiveness Networks, United States",
        "summary_en": "Interim estimates of 2024-2025 seasonal influenza vaccine effectiveness from four US vaccine effectiveness networks, October 2024–February 2025.",
        "source_url": "https://pubmed.ncbi.nlm.nih.gov/40014791/",
        "source_published_at": "2025-02-15",
        "country_code": "US",
        "region_code": "AMERICAS",
        "location_name": "Bethesda",
        "lon": -77.1025,
        "lat": 38.9897,
        "evidence_code": "PEER_REVIEWED_ARTICLE",
        "with_fr": True,
    },
    # Preprints — one preprint per event (title matches that preprint)
    {
        "layer_code": "PREPRINTS",
        "provider_slug": "medrxiv",
        "title": "National-scale surveillance of emerging SARS-CoV-2 variants in wastewater",
        "summary_en": "Preprint: national-scale wastewater surveillance for emerging SARS-CoV-2 variants; methods and findings from the described study.",
        "source_url": "https://www.medrxiv.org/content/10.1101/2022.01.14.21267633v1",
        "source_published_at": "2022-01-14",
        "country_code": None,
        "region_code": "EUROPE",
        "location_name": None,
        "lon": None,
        "lat": None,
        "evidence_code": "PREPRINT",
        "with_fr": False,
    },
    # Pharmacovigilance — one specific safety communication or decision per event
    {
        "layer_code": "PHARMACOVIGILANCE",
        "provider_slug": "fda",
        "title": "FDA Adds Warning About Rare Occurrence of Serious Liver Injury with Use of Veozah (fezolinetant) for Hot Flashes Due to Menopause",
        "summary_en": "FDA Drug Safety Communication: boxed warning added for Veozah (fezolinetant) due to rare serious liver injury; recommends liver testing and discontinuation if injury occurs.",
        "source_url": "https://www.fda.gov/safety/medical-product-safety-information/fda-adds-warning-about-rare-occurrence-serious-liver-injury-use-veozah-fezolinetant-hot-flashes-due",
        "source_published_at": "2024-09-12",
        "country_code": "US",
        "region_code": "AMERICAS",
        "location_name": "Silver Spring",
        "lon": -76.9375,
        "lat": 38.9959,
        "evidence_code": "REGULATORY_NOTICE",
        "with_fr": True,
    },
    {
        "layer_code": "PHARMACOVIGILANCE",
        "provider_slug": "fda",
        "title": "FDA Requests Removal of Suicidal Behavior and Ideation Warning from Glucagon-Like Peptide-1 Receptor Agonist (GLP-1 RA) Medications",
        "summary_en": "FDA requests removal of suicidal behavior and ideation warning from GLP-1 RA drug labels following review; patients should continue medication as prescribed and report concerns to providers.",
        "source_url": "https://www.fda.gov/drugs/drug-safety-and-availability/fda-requests-removal-suicidal-behavior-and-ideation-warning-glucagon-peptide-1-receptor-agonist-glp",
        "source_published_at": "2026-01-13",
        "country_code": "US",
        "region_code": "AMERICAS",
        "location_name": "Silver Spring",
        "lon": -76.9375,
        "lat": 38.9959,
        "evidence_code": "REGULATORY_NOTICE",
        "with_fr": False,
    },
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

    WHO_RSS = "https://www.afro.who.int/rss/featured-news.xml"  # WHO AFRO official fallback (global feed 404)
    ECDC_RSS = "https://www.ecdc.europa.eu/en/taxonomy/term/1307/feed"
    for slug, name, sc_id, tt_id, _ in PROVIDERS:
        pid = providers[slug]
        layer_id = _id_by_code(db, Layer, "code", "PUB_HEALTH")
        if slug == "pubmed":
            layer_id = _id_by_code(db, Layer, "code", "LITERATURE")
        elif slug == "medrxiv":
            layer_id = _id_by_code(db, Layer, "code", "PREPRINTS")
        elif slug == "fda":
            layer_id = _id_by_code(db, Layer, "code", "PHARMACOVIGILANCE")
        endpoint = WHO_RSS if slug == "who" else (ECDC_RSS if slug == "ecdc" else f"https://example.com/{slug}")
        fid = uuid.uuid4()
        db.add(
            SourceFeed(
                id=fid,
                provider_id=pid,
                name=f"{name} feed",
                feed_type="rss" if slug in ("who", "ecdc") else "api",
                endpoint_url=endpoint,
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

    for ev in CURATED_DEMO_EVENTS:
        layer_code = ev["layer_code"]
        prov_slug = ev["provider_slug"]
        title = ev["title"]
        summary_en = ev["summary_en"]
        source_url = ev["source_url"]
        published_at_str = ev.get("source_published_at")
        published_at = None
        if published_at_str:
            try:
                if "T" in str(published_at_str):
                    published_at = datetime.fromisoformat(str(published_at_str).replace("Z", "+00:00"))
                else:
                    published_at = datetime.strptime(str(published_at_str), "%Y-%m-%d").replace(tzinfo=timezone.utc)
                if published_at.tzinfo is None:
                    published_at = published_at.replace(tzinfo=timezone.utc)
            except (ValueError, TypeError):
                published_at = None
        country_code = ev["country_code"]
        region_code = ev["region_code"]
        location_name = ev["location_name"]
        lon = ev["lon"]
        lat = ev["lat"]
        evidence_code = ev["evidence_code"]
        with_fr = ev["with_fr"]

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
        payload = {"title": title, "url": source_url}
        content_hash = hashlib.sha256(source_url.encode()).hexdigest()[:128]
        db.add(
            RawDocument(
                id=raw_id,
                ingestion_run_id=run_id,
                source_feed_id=feed_id,
                provider_id=provider_id,
                original_title=title,
                original_url=source_url,
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
                source_published_at=published_at,
                geographic_scope="regional" if region_val else "global",
                country_code=country_code,
                region_code=region_val,
                location_name=location_name,
                location_point=location_point,
                visibility_status="visible",
                is_active=True,
            )
        )
        db.flush()
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
    print("Seeded curated demo events.")


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
