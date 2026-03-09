# User Flow

# USER FLOW DOCUMENT: HealthMonitor

## 1. Purpose

This document defines the expected user journeys for the HealthMonitor MVP.

It translates the product concept into concrete user interactions so the application can be implemented consistently across frontend, backend, and data layers.

The core workflow of the product is:

**Map Detection -> Compact Contextual Understanding -> Source Verification**

The system is designed for healthcare professionals who need to identify relevant global health signals quickly, understand their context in seconds, and verify the original source when needed.

## 2. Design Intent

The user flow must support the following principles:

- Fast signal triage from a global map view
- Clear distinction between source classes and trust levels
- Low-friction filtering by geography, layer, and time
- Compact event understanding before source verification
- Professional, calm, readable interaction patterns
- English-first experience with French summary support

The application is not designed as a clinical decision support workflow. It is a monitoring and intelligence workflow.

## 3. Primary User Journey

### 3.1 Step 1: Load, Filter, and Scope the Monitoring View

**Goal:** Let the user define the monitoring context before inspecting individual signals.

**Typical user actions:**
- Open the application
- View the default global map
- Select a region preset if needed
- Adjust the time window
- Toggle one or more content layers
- Optionally refine by source type, trust tier, topic, specialty, or country

**System behavior:**
- Load the map centered on the selected default region
- Show clustered markers based on active filters
- Update markers and counts immediately when filters change
- Keep the left-side filter panel persistent and accessible
- Preserve the map as the primary visual workspace

**Default initial state for MVP:**
- Region: `World`
- Time window: `Last 7 Days`
- Active layers: all five MVP layers enabled by default
- Language: English

### 3.2 Step 2: Spot and Triage Signals on the Map

**Goal:** Let the user decide in a few seconds whether a visible signal deserves closer inspection.

**User action:**
- Scan the map visually
- Hover over or click a marker or cluster

**System must provide enough visual information to support triage:**
- Marker presence indicates the event matches the active layer and current filters
- Marker style must reflect source-class grouping without relying on color alone
- Clusters must display the number of aggregated events
- Mixed-source clusters must indicate that they contain multiple source classes
- Hover interaction should provide a short preview when practical
- Click interaction should open the compact event card

**User decision at this step:**
- Ignore the signal
- Inspect the signal
- Zoom further into a dense region

### 3.3 Step 3: Review the Compact Event Card

**Goal:** Let the user understand the event before opening the original source.

This is the critical product moment.

The compact event card must answer five questions quickly:
1. What is this?
2. Why does it matter?
3. What kind of source is this?
4. Is it relevant to my geography or specialty?
5. Is it worth opening now?

**User action:**
- Click a marker
- Read the event card
- Decide whether to continue to source verification

**System behavior:**
- Keep the map visible while the card appears as an overlay, drawer, or side panel
- Preserve enough spatial context so the user does not feel lost
- Allow the user to close the card and continue scanning the map

### 3.4 Step 4: Verify the Original Source

**Goal:** Support professional verification and deeper reading.

**User action:**
- Click the primary action: `Open Source`

**System behavior:**
- Open the original source in a new tab or external view
- Preserve the current state of the dashboard so the user can return to the same map, filters, and selected event

**Verification outcome:**
- The user validates the relevance and credibility of the signal
- The user may return to the map and continue exploration

## 4. Compact Event Card Requirements

The compact event card is the primary interpretation layer between raw data and source verification.

### 4.1 Required Card Structure

The card must contain the following sections.

#### A. Identity and Signal Context
- Headline (source-derived title in the original source language)
- Layer name
- Source class
- Trust tier
- Freshness indicator

#### B. AI Summary
- Neutral, short, descriptive summary
- 2 to 3 sentences preferred
- 50 to 90 words maximum
- Focused on: what happened, where, when, and according to whom

#### C. Context Tags
- Topic or disease tag
- Specialty tag
- Geographic scope
- Evidence status

#### D. Core Event Details
- Date and time
- Location
- Source name
- Link to original source

#### E. Actions
- Open Source
- Copy Link
- Translate Toggle

`Save/Bookmark` is deferred from MVP and must not be treated as a required primary action in version 1.

### 4.2 Card Behavior Rules

- The card must be readable in under 10 seconds for a typical event
- The card must not hide or replace the map entirely
- The card must support closing without resetting current filters
- The card must remain compact and scannable on desktop layouts
- On dense clusters, selecting an event should be one step away from cluster expansion

## 5. AI Summary Behavior in the User Flow

The summary is not an opinion layer. It is a factual briefing layer.

### 5.1 Required Summary Characteristics

The summary must be:
- Descriptive
- Short
- Informative
- Neutral
- Traceable to the source
- Free of clinical recommendation

### 5.2 Hard Constraints

The summary must not:
- Tell the user what to do
- Use recommendation language such as `should`, `must`, `need to`, `recommended`
- Suggest treatment, diagnosis, or patient management
- Add urgency unless directly attributed to the source
- Turn association into causation without source support
- Use hype, emotional wording, or sensational framing
- Add speculative future implications
- Invent context not present in the source

### 5.3 Summary Formula

The target summary formula is:

**What happened + where + when + according to whom**

## 6. Filtering and Layer Interaction Flow

### 6.1 MVP Layers

The MVP includes five core layers:
1. Public Health / Outbreaks / Surveillance
2. Guidelines / Official Health Authority Updates
3. Scientific Literature
4. Pharmacovigilance / Recalls / Drug Safety
5. Preprints

### 6.2 Filter Logic

The user must be able to update the map view using combinations of the following:
- Region preset
- Country filter
- Time window
- Layer toggles
- Source grouping: Official vs Non-Official
- Source class
- Trust tier
- Topic or disease
- Specialty

### 6.3 Source Representation Logic

The user flow depends on a clear credibility distinction.

The application must separate:
- **Source grouping:** Official vs Non-Official
- **Source class:** Official Authority, Regulatory Authority, Scientific Literature, Preprint Server, Media, Database, or equivalent class used by the product
- **Trust tier:** High, Medium, Exploratory, or equivalent operational trust label

These concepts must not be collapsed into a single label.

### 6.4 Filter Update Behavior

When the user changes any major filter:
- The map refreshes markers and clusters
- The visible result count updates
- The selected region summary updates when applicable
- The current event card closes if the selected event is no longer part of the result set

## 7. Geographical Interaction Flow

### 7.1 Region Presets

The user can quickly switch the monitoring scope using predefined presets:
- World
- Americas
- MENA
- Europe
- Asia
- Africa
- Oceania

### 7.2 Country-Level Exploration

The user can click a country or select it through a filter control.

When a country is selected:
- The map recenters or zooms appropriately
- The result set is filtered to that jurisdiction
- A compact regional summary appears

### 7.3 Regional Summary Behavior

When a region or country is selected, the interface should show:
- Total visible signals
- Breakdown by active layer
- Top topics or diseases in the current selection

This summary supports situational awareness without replacing event-level exploration.

### 7.4 Cluster Interaction

Cluster behavior must support dense map usage reliably.

When a cluster is clicked:
- The system zooms in or opens a grouped list of events
- The user must be able to reach an individual event card with minimal extra interaction
- Mixed clusters must indicate that they contain multiple event or source types when possible

## 8. Language Flow

### 8.1 English-First Usage

The default application language is English.

The default generated summary is English.

### 8.2 French Support

When French mode is active:
- UI labels and filters must appear in French
- The AI summary must be shown in French
- The translated summary must be labeled as machine-translated
- The original English summary must remain accessible through a toggle
- The original source title must remain in its original language

## 9. Empty, Loading, and Failure States

These states are required in the MVP user flow.

### 9.1 Loading State

When the user changes filters or opens the application:
- The interface must show that new results are loading
- Previous results may remain visible briefly if progressive loading is used
- The user must not lose filter context

### 9.2 Empty State

If no events match the current filters:
- The map remains visible
- The interface displays a clear message such as `No events found for the current filters`
- The user is prompted to broaden filters or expand the time range

### 9.3 Partial Failure or Degraded Source State

If one or more source pipelines fail:
- The application must continue to function with remaining available data
- The user may be shown a non-blocking warning that some sources are temporarily unavailable
- The map must not collapse into a broken state if partial data is still available

## 10. Performance Expectations Within the User Flow

The user flow must feel responsive under realistic monitoring conditions.

MVP expectations:
- Smooth interaction with clustered rendering under realistic event density
- Reliable support for up to 10,000 active queryable events in the selected time window
- Fast visual feedback when filters change
- Event card opening with low perceived latency
- Map interaction that remains usable under dense regional concentrations

## 11. Out-of-Scope for MVP User Flow

The following are intentionally excluded from the MVP user flow:
- Live YouTube or streaming workflows
- Saved watchlists and user libraries
- Personalized alert subscriptions
- Team collaboration workflows
- Cross-source comparison tools inside the event card
- Custom drawn geographic monitoring zones
- Advanced geo-analytics and playback timelines

## 12. MVP User Flow Acceptance Criteria

The MVP user flow is successful when:
1. A user can open the application and reach a useful map view immediately
2. A user can change region, time, and layers without confusion
3. A user can identify a relevant marker or cluster and inspect it quickly
4. A user can understand an event from the compact card before opening the source
5. A user can verify the event source without losing application state
6. French translation works for summaries and UI without hiding the original English summary
7. Empty, loading, and degraded-data states remain understandable and usable
