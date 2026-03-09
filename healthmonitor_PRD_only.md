# Product Requirements Document (PRD): HealthMonitor

## 1. Introduction

### 1.1 Project Overview
HealthMonitor is a real-time global health intelligence dashboard designed for healthcare professionals. It centralizes, monitors, and summarizes relevant health-related events, publications, alerts, and signals through an interactive, map-based interface.

The platform is intended to provide rapid situational awareness by aggregating geospatially relevant health information from scientific, institutional, regulatory, and selected news sources. Its purpose is to help users identify potentially relevant signals quickly, understand them through a compact neutral summary, and then verify the original source.

### 1.2 Vision Statement
"A real-time global health intelligence dashboard for healthcare professionals."

### 1.3 Product Non-Scope
HealthMonitor is not intended to replace clinical reference tools or medical judgment. It is not:
- An Electronic Health Record (EHR)
- A patient data platform
- A Clinical Decision Support System (CDSS)
- A diagnostic engine
- A prescribing or patient management advisor
- A direct replacement for editorial clinical reference products such as UpToDate

## 2. Goals and Success Metrics

### 2.1 Product Goals
1. **Demonstrate Map Value**: prove that a global, layered map offers faster and more useful situational awareness than traditional feed-based monitoring.
2. **Validate Source Quality**: prove that the selected sources are credible, filterable, and useful for healthcare professionals.
3. **Prove AI Summary Utility**: prove that short, descriptive, neutral summaries save time without creating clinical ambiguity.
4. **Validate Core Workflow**: establish the user workflow of spotting a signal, understanding it quickly, and verifying the original source.

### 2.2 Success Metrics
| Metric | Target | Rationale |
|---|---:|---|
| User Return Rate | 3+ sessions per user per week | Indicates recurring monitoring value |
| Source Verification Rate | > 60% of event card opens lead to source click-through | Confirms the card supports triage and verification |
| Summary Scanability | Most summaries readable in under 10 seconds | Confirms the summary layer is concise and useful |
| Data Freshness | 90% of priority official alerts surfaced within 1 hour of publication | Confirms real-time value |
| Filter Usage | > 50% of sessions use at least one advanced filter | Confirms filtering is useful for professionals |

## 3. Target Users and Positioning

### 3.1 Target Users
The primary users are healthcare professionals who need continuous monitoring of scientific, epidemiological, regulatory, and public-health signals, including:
- Physicians
- Pharmacists
- Biologists and laboratory professionals
- Paramedical professionals involved in surveillance or response
- Public health professionals
- Health researchers

### 3.2 Product Positioning
HealthMonitor is positioned as an **intelligent health surveillance dashboard** combining:
1. Scientific and regulatory monitoring
2. Geospatial signal visualization
3. AI-assisted summarization for rapid triage

It is a professional monitoring and intelligence tool, not a clinical decision engine.

## 4. Functional Requirements

### 4.1 Core Interface and Layout
The product must follow the visual and interaction logic of WorldMonitor while remaining adaptable for a clinical audience.

Required interface principles:
- **Central element**: interactive world map
- **Left panel**: layers, filters, and region selection
- **Map behavior**: markers displayed strictly according to active filters and layers
- **Language**: English by default, with French translation support
- **Readability**: clean, high-contrast interface suitable for professional use
- **Accessibility**: non-color-only differentiation for key statuses such as source credibility

### 4.2 Geographical Interaction
| Requirement ID | Description | Priority |
|---|---|---|
| FR-GEO-001 | Display an interactive world map with mandatory point clustering based on density and zoom level | Must-Have |
| FR-GEO-002 | Support regional presets: World, Americas, MENA, Europe, Asia, Africa, Oceania | Must-Have |
| FR-GEO-003 | Allow filtering and selection at country level via map interaction or selection control | Must-Have |
| FR-GEO-004 | Support dynamic time-window filtering such as 24h, 7d, and 30d | Must-Have |
| FR-GEO-005 | Show a compact regional summary when a region or country is selected, including total signals, breakdown by layer, and top topics | Should-Have |
| FR-GEO-006 | Defer custom drawn geographic areas and advanced geo-analytics to a later phase | Deferred |

### 4.3 Layer Management and Source Classification
The MVP will support **five core layers**.

| Layer ID | Layer Name | Primary Source Class | Default Trust Tier |
|---|---|---|---|
| L-PUB | Public Health / Outbreaks / Surveillance | Official Authority | High |
| L-GUI | Guidelines / Official Health Authority Updates | Official Authority | High |
| L-LIT | Scientific Literature (Peer-Reviewed) | Scientific Literature | High |
| L-PHV | Pharmacovigilance / Recalls / Drug Safety | Regulatory Authority | High |
| L-PRE | Preprints | Preprint Server | Exploratory |

Overarching source controls must allow users to filter between:
- Official Sources
- Non-Official Sources

This classification must be visible both in filtering and in event presentation.

### 4.4 Layer Metadata and Filtering Requirements
Each layer must support filtering beyond content type. The system must support, where applicable:
- Time window
- Geography
- Source class
- Trust tier
- Specialty category
- Disease or topic tag
- Issuing body, regulator, or institution
- Evidence status
- Update status
- Language

Examples of layer-specific metadata:
- **Guidelines**: issuing body, current vs superseded, target population
- **Pharmacovigilance**: regulator, ingredient or product, alert type, jurisdiction
- **Scientific Literature**: article type, study design, journal, evidence status
- **Preprints**: platform, specialty, topic, evidence status = preprint
- **Public Health / Surveillance**: pathogen, event type, reporting body, outbreak scope

### 4.5 Event Card Requirements
The event card is the core product moment. It must allow the user to understand whether an event matters before opening the source.

Each event card must include:
- Title
- Layer
- Source class
- Trust tier
- Freshness indicator
- AI summary
- Specialty tags
- Topic or disease tags
- Geographic scope
- Evidence status
- Date
- Location
- Source name
- Link to original source
- Core actions: Open Source, Copy Link, Save/Bookmark

### 4.6 Core User Workflow
The expected 3-step workflow is:
1. **Spot and Triage**: the user sees a signal on the map and decides whether it deserves attention
2. **Understand Quickly**: the user opens the compact event card and gets immediate context
3. **Verify**: the user opens the original source for validation and deeper reading

The product must optimize this workflow for speed and clarity.

### 4.7 AI Summary Requirements
AI summaries must be:
- Descriptive
- Short
- Informative
- Neutral
- Traceable to the source
- Free from clinical recommendation

Required summary characteristics:
- 50 to 90 words maximum
- 2 to 3 short sentences preferred
- Must answer: what happened, where, when, and according to whom
- Must include source-linked factual framing

#### AI Summary Red Lines
The summary system must strongly prevent or reject:
- Recommendation language such as “should,” “must,” “need to,” “recommended”
- Clinical advice, prescribing language, treatment suggestions, or triage instructions
- Prescriptive urgency not directly attributed to the source
- Causality overreach when the source only reports association
- Hype or sensational terms such as “breakthrough,” “game changer,” or “alarming”
- Speculative future impact statements
- Moral or emotional framing
- Evidence-quality judgment unless explicitly represented elsewhere
- Hallucinated context not present in the source

### 4.8 Language Requirements
- Default language: English
- Secondary language: French
- The following must support translation: UI labels, filters, and AI summaries
- Original source titles must remain in their original language
- Machine-translated summaries must be clearly labeled as translated
- Users must be able to access the original English summary when relevant

## 5. Data Requirements

### 5.1 Priority Source Streams for MVP Validation
The initial product must validate both real-time monitoring and scientific relevance by prioritizing these source families:
1. PubMed
2. Europe PMC
3. medRxiv / bioRxiv
4. WHO and ECDC official feeds
5. Selected pharmacovigilance and drug-safety sources

### 5.2 Deduplication Requirements
The platform must reduce duplication across sources and prevent map noise.

Minimum deduplication logic must include:
- Title similarity comparison
- Source URL comparison
- Topic, place, and time similarity grouping
- Merging or grouping closely related reports where appropriate

### 5.3 Data Volume and Reliability Targets
The system must be designed to support:
- Up to 10,000 active queryable events in the relevant time window
- Smooth interaction through clustering and filtered rendering
- A manageable number of visible map objects at any one time

## 6. MVP Scope

### 6.1 In Scope for MVP
The MVP must include:
- Interactive world map
- Marker clustering
- Region presets and country-level filtering
- Five core layers
- Official vs non-official source filtering
- Compact event cards with source credibility information
- Neutral AI summaries
- English UI with French translation support for relevant elements
- Basic search
- Date filtering
- Deduplication logic

### 6.2 Out of Scope for MVP
The following are deferred to later phases:
- Custom geographic drawing tools
- Province or city-level advanced geospatial analytics
- Live YouTube or streaming integration
- Advanced user accounts and saved alert systems
- Full personalization by specialty
- AI prioritization or ranking layers
- Complex analytics dashboards
- Patient data integration of any kind

## 7. Acceptance Criteria for MVP
The MVP should be considered successful if it demonstrates all of the following:
1. Users can identify and open relevant signals directly from a map-based view
2. The map remains readable and performant under realistic event density
3. Professionals can filter events meaningfully by source type, geography, layer, and time
4. Event cards provide enough context for rapid triage before source verification
5. AI summaries remain neutral, short, and free of clinical advice
6. Source credibility is visible and understandable
7. The product supports English-first usage with usable French translation support
