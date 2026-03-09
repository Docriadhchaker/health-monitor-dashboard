# Styling Guidelines

## 1. Purpose

This document defines the visual and interaction styling rules for HealthMonitor, a real-time global health intelligence dashboard for healthcare professionals.

The interface must preserve the structural logic inspired by WorldMonitor:
- map-first layout
- persistent left-side layer and filter rail
- compact event cards
- high-density, triage-oriented scanning

The visual execution must be adapted for a clinical audience:
- calmer and more trustworthy
- less saturated and less alarmist
- highly readable under time pressure
- accessible by default

This document covers only styling and presentation rules. Functional product requirements, technical architecture, user flow, and database design are defined in separate documents.

---

## 2. Design Principles

### 2.1 Clinical Readability First

Every visual choice must prioritize fast comprehension for busy healthcare professionals. The interface must support quick scanning, low cognitive load, and predictable information hierarchy.

### 2.2 Calm, Neutral, Professional Tone

The dashboard must not look like a military OSINT dashboard, breaking-news app, or consumer news portal. It should feel closer to a professional health intelligence tool.

### 2.3 Structural Fidelity, Visual Flexibility

The layout logic should follow the WorldMonitor pattern, but branding, colors, typography, and density should be adapted for clinical trust and accessibility.

### 2.4 Color Is Never the Only Signal

Meaning, trust, and state must never depend on color alone. Shape, text labels, icons, borders, and badges must reinforce meaning.

### 2.5 Predictable Components

Cards, badges, markers, chips, filters, and panels must behave consistently across all layers.

---

## 3. Accessibility Baseline

### 3.1 Standard

The interface must meet **WCAG 2.2 AA** as the minimum accessibility baseline.

### 3.2 Minimum Rules

- Normal text contrast: **4.5:1** minimum
- Large text contrast: **3:1** minimum
- Non-text UI components and graphical indicators: **3:1** minimum
- Visible keyboard focus on all interactive elements
- Interactive targets: **minimum 24 x 24 px**, except map pins where spatial fidelity is essential
- Status and trust cues must not rely on color alone

### 3.3 Practical Accessibility Rules

- Body text and AI summaries should exceed minimum contrast where possible
- Focus rings must remain visible in both light and dark mode
- Marker meaning must remain identifiable through shape and labels, not only color
- Truncated content must expose full text on hover, click, or expansion

---

## 4. Design Tokens

### 4.1 Color Tokens

#### Light Mode

```txt
--color-bg-primary: #F8FAFC;
--color-bg-surface: #FFFFFF;
--color-bg-elevated: #F1F5F9;
--color-bg-muted: #E2E8F0;

--color-text-primary: #0F172A;
--color-text-secondary: #475569;
--color-text-muted: #64748B;
--color-text-inverse: #F8FAFC;

--color-border-default: #CBD5E1;
--color-border-strong: #94A3B8;
--color-divider: #E2E8F0;

--color-accent-primary: #0F6CBD;
--color-accent-primary-hover: #0B5EA7;
--color-accent-secondary: #0F766E;

--color-success: #15803D;
--color-warning: #B45309;
--color-danger: #B91C1C;
--color-info: #1D4ED8;
```

#### Dark Mode

```txt
--color-bg-primary: #0F172A;
--color-bg-surface: #111827;
--color-bg-elevated: #1F2937;
--color-bg-muted: #334155;

--color-text-primary: #F8FAFC;
--color-text-secondary: #CBD5E1;
--color-text-muted: #94A3B8;
--color-text-inverse: #0F172A;

--color-border-default: #334155;
--color-border-strong: #475569;
--color-divider: #1F2937;

--color-accent-primary: #38BDF8;
--color-accent-primary-hover: #0EA5E9;
--color-accent-secondary: #2DD4BF;

--color-success: #22C55E;
--color-warning: #F59E0B;
--color-danger: #EF4444;
--color-info: #60A5FA;
```

### 4.2 Semantic Source and Layer Colors

These colors define stable meaning across markers, badges, filter chips, and cards.

```txt
Official Authority / Regulatory      -> Blue
Scientific Literature (Peer Reviewed)-> Green
Preprints                            -> Amber
Pharmacovigilance                    -> Red or Amber-Red
Public Health / Surveillance         -> Blue-Red depending on severity
Media / Non-Official                 -> Slate / Muted Amber
Database / Structured Feed           -> Teal
```

### 4.3 Typography Tokens

#### Font Family

```txt
font-family-sans: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
font-family-mono: "SFMono-Regular", Consolas, "Liberation Mono", Menlo, monospace;
```

#### Font Size Scale

```txt
--font-size-xs: 12px;
--font-size-sm: 13px;
--font-size-md: 14px;
--font-size-lg: 16px;
--font-size-xl: 18px;
--font-size-2xl: 20px;
--font-size-3xl: 24px;
```

#### Line Height Scale

```txt
--line-height-tight: 1.2;
--line-height-normal: 1.45;
--line-height-relaxed: 1.6;
```

#### Font Weight Scale

```txt
--font-weight-regular: 400;
--font-weight-medium: 500;
--font-weight-semibold: 600;
--font-weight-bold: 700;
```

### 4.4 Spacing Tokens

```txt
--space-1: 4px;
--space-2: 8px;
--space-3: 12px;
--space-4: 16px;
--space-5: 20px;
--space-6: 24px;
--space-8: 32px;
--space-10: 40px;
```

### 4.5 Radius Tokens

```txt
--radius-sm: 6px;
--radius-md: 10px;
--radius-lg: 14px;
--radius-xl: 18px;
--radius-full: 9999px;
```

### 4.6 Shadow Tokens

```txt
--shadow-sm: 0 1px 2px rgba(15, 23, 42, 0.06);
--shadow-md: 0 4px 12px rgba(15, 23, 42, 0.10);
--shadow-lg: 0 12px 28px rgba(15, 23, 42, 0.14);
```

### 4.7 Motion Tokens

```txt
--duration-fast: 120ms;
--duration-normal: 180ms;
--duration-slow: 240ms;
--ease-standard: cubic-bezier(0.2, 0, 0, 1);
```

Use motion sparingly. No decorative animation. Motion must support orientation and interaction only.

### 4.8 Z-Index Scale

```txt
--z-map: 0;
--z-map-controls: 10;
--z-left-rail: 20;
--z-floating-card: 30;
--z-dropdown: 40;
--z-modal: 50;
--z-toast: 60;
```

---

## 5. Layout Rules

### 5.1 Desktop Layout

The primary layout must be:
- left rail for layers and filters
- central map viewport
- floating or docked event card
- optional top utility bar for language/theme/global search

### 5.2 Width Rules

```txt
Left rail width: 320px default, 360px max
Event card width: 360px to 440px
Top bar height: 56px
Map viewport: remaining width and full available height
```

### 5.3 Density Rules

- Information density should be high but not cramped
- Default card padding: `16px`
- Default panel padding: `16px`
- Tight metadata rows may use `12px`
- Avoid overly tall cards; prioritize scan order and truncation

### 5.4 Responsive Rules

#### Tablet
- Left rail may collapse into an overlay drawer
- Event card may dock bottom-right or slide in

#### Mobile
- Full desktop map dashboard is not the priority for MVP
- Mobile should support map viewing, filter access, and card reading
- Deep analysis behavior may move into stacked screens or bottom sheets

---

## 6. Component Styling Rules

### 6.1 Map Canvas

- Map background must remain neutral and not overly saturated
- Political boundaries and labels should be subtle
- Avoid heavy visual styling that competes with markers
- Map controls must use elevated surfaces with strong contrast

### 6.2 Left Rail

- Surface uses `bg-surface` or `bg-elevated`
- Clear section grouping for layers, geography, date range, and source filters
- Section headers: small uppercase or semibold labels
- Active filters should be visually obvious through fill + border + text, not color alone

### 6.3 Buttons

#### Primary Button
- Filled with primary accent
- White or inverse text
- Used for high-priority actions only, such as `Open Source`

#### Secondary Button
- Neutral surface with visible border
- Used for actions like `Show Original`, `Translate`, `Reset Filters`

#### Ghost Button
- Minimal chrome
- Used only for low-weight utility actions

### 6.4 Input Controls

- Inputs, dropdowns, toggles, and chips must share the same radius family
- Focus state must be visible and contrast-safe
- Invalid state uses border + icon + message, not color alone

### 6.5 Layer Chips and Filter Chips

- Height: `28px` to `32px`
- Radius: `full`
- Chips must include icon or text cue where needed
- Selected chip uses stronger contrast and border
- Unselected chip remains readable, never washed out

### 6.6 Event Card

The event card is the most important component in the product.

#### Card Container
- Surface: elevated neutral background
- Radius: `14px`
- Shadow: `md`
- Border: default subtle border
- Padding: `16px`

#### Card Scan Order
1. Headline
2. Meta row
3. AI summary
4. Context chips
5. Core details
6. Action row

#### Headline Rules
- Font size: `18px` to `20px`
- Weight: `600`
- Maximum 2 lines before truncation
- Original title language must be preserved

#### Meta Row Rules
- Use small type (`12px` to `13px`)
- Items separated by bullets or dividers
- Must remain scannable in one line when possible
- If wrapping is required, wrap cleanly without overlap

#### AI Summary Rules
- Font size: `14px` to `16px`
- Line height: `1.45` to `1.6`
- Maximum 3 short sentences
- Default display should clamp to approximately 5 lines if needed
- Summary block must not visually dominate the card

#### Context Chips Rules
- Wrap cleanly across lines
- Use compact spacing
- Do not allow more than 2 rows before collapse on dense cards

#### Detail Row Rules
- Date and time use tabular numerals
- Location and source should use secondary text color
- Source link must remain visually clear and clickable

### 6.7 Marker Styling

Marker styling must communicate credibility and source category immediately.

#### Official Source Marker
- Shape: solid circle
- Fill: blue
- Border: strong contrast outline

#### Scientific Literature Marker
- Shape: solid circle
- Fill: green
- Border: strong outline or subtle ring

#### Preprint Marker
- Shape: diamond
- Fill: amber
- Border: visible outline

#### Pharmacovigilance Marker
- Shape: triangle or alert diamond
- Fill: red or amber-red depending on severity
- Border: strong outline

#### Non-Official / Media Marker
- Shape: square or outlined diamond
- Fill: muted slate or muted amber
- Border: clear outline

### 6.8 Cluster Styling

- Cluster markers must scale with count
- Cluster count must be centered and legible
- Minimum cluster size: `28px`
- Maximum cluster size: `48px`
- Official-only clusters should inherit official color logic
- Mixed-source clusters should use mixed styling or segmented inner badge
- Cluster click behavior is defined elsewhere; this document only defines appearance

### 6.9 Badges and Trust Labels

Trust and source labels must be concise and visually distinct.

#### Recommended Badge Mapping
- `Official Authority` -> blue badge
- `Scientific Literature` -> green badge
- `Preprint` -> amber badge
- `Non-Official` -> slate badge
- `High Confidence` -> blue or green outlined badge
- `Exploratory` -> amber outlined badge

### 6.10 Empty, Loading, and Degraded States

#### Loading
- Use skeleton blocks or subdued progress indicators
- Avoid flashy spinners as the only signal

#### Empty State
- Must explain why no results are shown
- Include one recovery action such as `Reset filters`

#### Degraded State
- Use warning surface or inline system notice
- Explain that some feeds may be unavailable without breaking overall layout

---

## 7. Layer Styling Rules

The MVP includes exactly **5 layers**:
1. Public Health / Surveillance
2. Guidelines / Official Health Authority Updates
3. Scientific Literature
4. Pharmacovigilance / Recalls / Safety Alerts
5. Preprints

### 7.1 Layer Tokens

| Layer | Icon Direction | Primary Color | Marker Shape | Card Accent |
|---|---|---:|---|---|
| Public Health / Surveillance | Globe, pathogen, alert | Blue / Red by severity | Circle | Top border or badge |
| Guidelines / Official Updates | Scroll, shield, institution | Blue | Circle | Top border or badge |
| Scientific Literature | Book, journal, atom | Green | Circle | Top border or badge |
| Pharmacovigilance | Pill, warning, recall | Red / Amber-Red | Triangle / Diamond | Top border or badge |
| Preprints | Draft, clock, paper | Amber | Diamond | Top border or badge |

### 7.2 Layer Toggle States

Each layer toggle must support:
- default state
- hover state
- selected state
- disabled state

Selected state must show:
- stronger border
- stronger text contrast
- icon visibility
- optional active indicator bar

---

## 8. Language and Translation Presentation

### 8.1 English as Base Interface

English is the default system language.

### 8.2 French Mode

When French mode is active:
- static UI strings are translated
- AI summaries may be machine-translated into French
- the original English summary must remain accessible
- original source titles remain in their original language

### 8.3 Translation Labeling

Every translated AI summary must show a visible label such as:
- `Machine-translated from English`

This label should appear in small secondary text directly above or beside the summary.

### 8.4 Toggle Behavior Styling

The language toggle for summaries should be compact, visible, and secondary in priority. It must never visually compete with `Open Source`.

---

## 9. AI Summary Presentation Constraints

The styling of the summary block must reinforce its intended role: a short factual brief, not advice.

### 9.1 Visual Rules

- Summary uses body style, not headline style
- No highlighted callout box suggesting urgency unless the source type explicitly warrants alert treatment
- No colored emphasis on specific verbs or claims
- No visual treatment that implies recommendation or clinical instruction

### 9.2 Content Presentation Rules

The summary block must remain visually neutral and concise.

It must not contain styling patterns associated with:
- warnings unless explicitly tied to a validated alert layer
- recommendations
- action prompts
- consumer advice

---

## 10. Dark and Light Mode Rules

### 10.1 Both Modes Are First-Class

Neither mode should be a low-quality adaptation. Both light and dark themes must maintain contrast, clarity, and source differentiation.

### 10.2 Light Mode Intent

Light mode should feel clean, clinical, and document-like.

### 10.3 Dark Mode Intent

Dark mode should feel calm and modern, not neon or cyberpunk.

### 10.4 Theme Consistency Rules

- Semantic meanings must remain stable across themes
- Marker shape meaning must remain identical
- Border and divider visibility must remain sufficient
- Focus rings must remain highly visible in both themes

---

## 11. Responsive and Density Rules

### 11.1 Text Truncation Rules

- Headline: max 2 lines
- Meta row: 1 line preferred, 2 lines max
- Summary: clamp to 5 lines in compact mode
- Chips: wrap, then collapse after 2 rows if needed

### 11.2 High-Density Dashboard Rules

- Avoid oversized headers
- Prefer compact spacing between metadata elements
- Reserve visual emphasis for the event card, selected markers, and active filters
- Do not overuse shadows, bright colors, or animation

### 11.3 Panel Behavior

- Left rail should scroll independently from the map
- Event card should remain usable without covering too much of the map
- Overlays should not stack excessively

---

## 12. Implementation Notes for Frontend

These guidelines are intended to map cleanly to a tokenized frontend implementation.

Recommended implementation approach:
- Tailwind CSS for utility styling
- CSS variables for theme tokens
- semantic component variants for badges, chips, markers, and cards
- theme-aware tokens defined at root level and switched with class-based theme mode

The frontend should implement styling through reusable component variants, not one-off inline styling.
