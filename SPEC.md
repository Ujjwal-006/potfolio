# System Specification: Portfolio Backend & Extraction Ledger

Generated via comprehensive static extraction of all HTML template assets in `html/`.

---

## 1. Forms and Input Elements

### In `html/transfer desk.html` (`transfer_desk.html`)
- **Form Element**: `<form id="transfer-form" onsubmit="handleTransferSubmit(event)">`
  - **Inputs / Controls**:
    1. **Caller Name / Agent**:
       - `id`: `caller-name`
       - `name`: `caller_name`
       - `type`: `text`
       - `required`: `True`
       - `placeholder`: `e.g. Jürgen K. / Sporting Director`
    2. **Club / Organization**:
       - `id`: `caller-org`
       - `name`: `caller_org`
       - `type`: `text`
       - `required`: `False` (Optional)
       - `placeholder`: `e.g. Red Bull Arena Group / Enterprise Lab`
    3. **Official Email Address**:
       - `id`: `caller-email`
       - `name`: `caller_email`
       - `type`: `email`
       - `required`: `True`
       - `placeholder`: `director@club-or-enterprise.com`
    4. **Engagement Nature / Role Scope**:
       - `id`: `engagement-type`
       - `name`: `engagement_type`
       - `type`: `<select>`
       - `required`: `True`
       - **Options**:
         - `lead-architect` ("Principal / Lead Solutions Architect (Permanent)")
         - `contract-webgl` ("WebGL & 3D Interactive Graphics Contract (Sprint / Retainer)")
         - `technical-leadership` ("Fractional VP Engineering / Technical Directorate")
         - `advisory` ("High-Scale Frontend Advisory & Performance Audit")
         - `other` ("General Inquiries / Media & Panel Requests")
    5. **Tactical Objectives & Contract Scope**:
       - `id`: `contract-terms`
       - `name`: `contract_terms`
       - `type`: `<textarea>`
       - `required`: `True`
       - `placeholder`: `Detail your squad objectives, timelines, tech stack requirements, and targeted deliverables...`
  - **Submit Button**:
    - `<button id="submit-btn" type="submit">` (Contains label `btn-text`, icon `btn-icon`, spinner `btn-spinner`)
  - **Confirmation Element**:
    - `<div id="confirmation-banner">` (revealed on successful dispatch)

*(No other `<form>` elements exist across the other 5 HTML templates).*

---

## 2. JavaScript Event Handlers Requiring Real Backend Integration

1. **`handleTransferSubmit(event)` in `html/transfer desk.html`**:
   - **Current Behavior**: Intercepts submit with `event.preventDefault()`, executes a local 750ms `setTimeout`, and reveals `#confirmation-banner` without transmitting network payload.
   - **Target Integration**: Asynchronous `fetch('/api/transfer-inquiries', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(...) })`. Handles 200 success (displays confirmation) and 422/500 error feedback gracefully.
2. **`exportLedgerJSON()` in `html/contect and match record.html`**:
   - **Current Behavior**: Encodes a hardcoded JavaScript object client-side into a data URI.
   - **Target Integration**: Triggers download from backend endpoint `/api/records` or downloads backend-verified JSON directly.
3. **`triggerDownloadAlert(event)` in `html/contect and match record.html`**:
   - **Current Behavior**: Triggers download alert then calls local `exportLedgerJSON()`.
   - **Target Integration**: Redirects / fetches `/api/download-cv`.

---

## 3. Dead Links & Navigation Routing Map

Across all 6 templates, navigation elements use `data-path="..."` and `href="#"`. These map cleanly to the following FastAPI routes:

| Semantic Route | Associated Template | File on Disk | Dead Link / Identifier |
| :--- | :--- | :--- | :--- |
| `/` or `/home` | `hero_page.html` | `html/hero page.html` | `data-path="home"`, `href="#"` |
| `/about` | `about_me.html` | `html/about me.html` | `data-path="about"`, `href="#"` |
| `/projects` | `project.html` | `html/project.html` | `data-path="projects"`, `href="#"` |
| `/experience` | `contect_and_match_record.html` | `html/contect and match record.html` | `data-path="experience"`, `href="#"` |
| `/contact` | `transfer_desk.html` | `html/transfer desk.html` | `data-path="contact"`, `href="#"` |
| `/attributes` | `atribute.html` | `html/atribute.html` | `data-path="trophy-room"`, `href="#"` |
| `/scouting-reports` | `about_me.html` | `html/about me.html` | `data-path="scouting-reports"` in hero |
| `/api/download-cv` | CV Download Asset | (Generated / Static payload) | `data-path="cv"`, `data-path="download-cv"`, `href="#download"` |

In addition, direct template paths will return HTTP 200:
- `/about_me.html` & `/about%20me.html`
- `/atribute.html`
- `/contect_and_match_record.html` & `/contect%20and%20match%20record.html`
- `/hero_page.html` & `/hero%20page.html`
- `/project.html`
- `/transfer_desk.html` & `/transfer%20desk.html`

---

## 4. Hard-Coded Content Candidates for Dynamic API Endpoints

1. **Tactical Projects (11 items)** in `project.html`:
   - Attackers: Neo-Stadium (Three.js/GLSL), Champions HUD (React/D3), Aura Trading (WebSockets/Canvas)
   - Midfield: Stream Engine (Go/WebRTC), Tactical Radar (TypeScript/WebGL), Pipeline FC (Docker/K8s/Rust)
   - Defense: Kop Design (Tailwind Tokens), Apex Protocol (GraphQL/Redis), Cipher Shield (ZK/Cryptography), Telemetry Bus (Kafka)
   - Goalkeeper: The Core Portfolio Engine (60 FPS WebGL Hub)
   - **Endpoint**: `GET /api/projects`
2. **Contract & Match Dossier Records** in `contect and match record.html`:
   - Career Experience (4 records: Anfield Digital Labs, Apex Broadcast Media, Tactical Metrics UK, Mersey Tech Foundry)
   - Education (2 records: University of Liverpool, Anfield Scientific Academy)
   - Certifications (4 records: UEFA Tech Hackathon, Three.js Journey, AWS PSA, CNCF CKA)
   - **Endpoint**: `GET /api/records`
3. **Tactical Telemetry & Attributes** in `atribute.html` & `about me.html`:
   - Overall Rating (94)
   - FUT 6 Attributes (COD 96, DBG 94, ARC 98, SPD 92, TEA 95, PHY 91)
   - Radar Hexagon (Frontend 98, 3D WebGL 95, Sys Arch 96, Cloud 92, Leadership 94, Direction 90)
   - Honours List (4 major awards)
   - **Endpoint**: `GET /api/attributes`
