import os
from typing import Any, Dict, List, Optional
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse


app = FastAPI(
    title="Ujjwal Official Digital Portfolio API",
    description="Backend service powering the portfolio, tactical HUDs, and scout transfer inquiries",
    version="1.0.0",
)

# Enable CORS for cross-origin local testing
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ==========================================
# Dynamic Data & Utility Endpoints

PUBLIC_DIR = Path(__file__).parent / "public"

HTML_MAP = {
    "index.html": "/",
    "about.html": "/about",
    "projects.html": "/projects",
    "experience.html": "/experience",
    "contact.html": "/contact",
    "attributes.html": "/attributes",
    "career-stats.html": "/career-stats",
}

LEGACY_MAP = {
    "hero_page.html": "index.html",
    "about_me.html": "about.html",
    "project.html": "projects.html",
    "contect_and_match_record.html": "contact.html",
    "transfer_desk.html": "contact.html",
    "atribute.html": "attributes.html",
}
# ==========================================

@app.get("/api/projects", summary="Tactical Projects Registry")
async def get_projects():
    return {
        "formation": "4-3-3 Attack",
        "total_shipped": 12,
        "active_builds": 3,
        "projects": [
            {
                "id": 1,
                "squad_no": "11",
                "title": "Neo-Stadium",
                "position": "Left Wing (Attacker)",
                "category": ["3d", "creative"],
                "subtitle": "Three.js / WebGL 2.0",
                "fps": "60 FPS",
                "description": "Procedural 3D stadium engine with custom GLSL floodlight volumetric shaders and 250k dynamic particles.",
                "tags": ["THREE.JS", "GLSL", "WEBGL 2"],
            },
            {
                "id": 2,
                "squad_no": "09",
                "title": "Champions HUD",
                "position": "Center Forward (Flagship Attacker)",
                "category": ["stack", "3d"],
                "subtitle": "React / D3 Telemetry",
                "concurrency": "250K Concurrent",
                "description": "Live broadcast overlay powering live European match centers. Instant sub-50ms pitch telemetry synchronization.",
                "tags": ["REACT 19", "D3.JS", "SSE"],
            },
            {
                "id": 3,
                "squad_no": "07",
                "title": "Aura Trading",
                "position": "Right Wing (Attacker)",
                "category": ["stack", "creative"],
                "subtitle": "WebSockets / Canvas 2D",
                "tick_rate": "120 Tick/s",
                "description": "Ultra-low latency institutional crypto book visualizer utilizing multi-threaded web workers and offscreen canvas rendering.",
                "tags": ["CANVAS", "WORKERS", "WSS"],
            },
            {
                "id": 4,
                "squad_no": "08",
                "title": "Stream Engine",
                "position": "Left Midfield",
                "category": ["stack", "arch"],
                "subtitle": "Go / WebRTC Cluster",
                "uptime": "99.99% UP",
                "description": "High-throughput peer mesh video relay balancing edge transcodings across 4 global regions.",
                "tags": ["GOLANG", "WEBRTC"],
            },
            {
                "id": 5,
                "squad_no": "10",
                "title": "Tactical Radar (Captain)",
                "position": "Center Attacking Playmaker",
                "category": ["3d", "arch"],
                "subtitle": "TypeScript / WebGL Analytics",
                "status": "Pro Deployed",
                "description": "Interactive tactical board simulating squad spatial compression, xG flow metrics, and press resistance analytics.",
                "tags": ["TS", "WEBGL", "MATH3D"],
            },
            {
                "id": 6,
                "squad_no": "06",
                "title": "Pipeline FC",
                "position": "Right Midfield",
                "category": ["arch", "stack"],
                "subtitle": "Docker / K8s / CI Daemon",
                "scaling": "Auto-Scale",
                "description": "Autonomous release orchestration pipeline containerizing feature branches into preview environments within 35 seconds.",
                "tags": ["K8S", "RUST"],
            },
            {
                "id": 7,
                "squad_no": "03",
                "title": "Kop Design",
                "position": "Left Back (Defender)",
                "category": ["creative", "stack"],
                "subtitle": "Tailwind Tokens",
                "components": "64 Components Built",
                "tags": ["TAILWIND", "DESIGN SYSTEMS"],
            },
            {
                "id": 8,
                "squad_no": "04",
                "title": "Apex Protocol",
                "position": "Center Back (Defender)",
                "category": ["arch", "stack"],
                "subtitle": "GraphQL / Redis",
                "feature": "Zero-Drop Caching",
                "tags": ["GRAPHQL", "REDIS"],
            },
            {
                "id": 9,
                "squad_no": "05",
                "title": "Cipher Shield",
                "position": "Center Back (Defender)",
                "category": ["arch"],
                "subtitle": "ZK / Cryptography",
                "feature": "Audit Cleared",
                "tags": ["ZERO-KNOWLEDGE", "SECURITY"],
            },
            {
                "id": 10,
                "squad_no": "02",
                "title": "Telemetry Bus",
                "position": "Right Back (Defender)",
                "category": ["arch", "stack"],
                "subtitle": "Kafka / Event Broker",
                "throughput": "1.2M Events/Min",
                "tags": ["KAFKA", "STREAMING"],
            },
            {
                "id": 11,
                "squad_no": "01",
                "title": "The Core Portfolio Engine",
                "position": "Goalkeeper (Anchor)",
                "category": ["3d", "stack", "arch"],
                "subtitle": "60 FPS WebGL Hub // Flagship Foundation",
                "reliability": "99.98% Reliability",
                "tags": ["WEBGL", "FASTAPI", "TAILWIND"],
            },
        ],
    }


@app.get("/api/records", summary="Contract Ledger & Match Records")
async def get_records():
    return {
        "record_id": "ANF-REG-2025-01",
        "player_alias": "Squad Lead MT",
        "seasons_active": "8+ Campaigns",
        "tactical_rating": 94,
        "fitness_status": "Match Ready",
        "experience": [
            {
                "period": "2022 — PRESENT",
                "status": "CAMP ACTIVE",
                "club": "Anfield Digital Labs // Kode United",
                "location": "UK",
                "role": "Principal Creative Technologist",
                "squad": "Squad Architect / Lead",
                "highlights": [
                    "Engineered high-throughput WebGL tactical engine executing 250k event dispatches/sec.",
                    "Directed multi-platform design ecosystem across 14 squads; reduced front-end bundle footprint by 42%.",
                    "Maintained 99.99% faultless latency for international matchday streaming interfaces.",
                ],
            },
            {
                "period": "2020 — 2022",
                "status": "2 SEASONS",
                "club": "Apex Broadcast Media",
                "location": "Global Networks",
                "role": "Senior 3D WebGL Architect",
                "squad": "Full-Stack Division",
                "highlights": [
                    "Architected custom GLSL fragment shaders simulating volumetric stadium pitch weather.",
                    "Constructed real-time WebSocket telemetry ingestion pipelines supporting 4.8M concurrent spectators.",
                ],
            },
            {
                "period": "2018 — 2020",
                "status": "2 SEASONS",
                "club": "Tactical Metrics UK",
                "location": "Analytics Hubs",
                "role": "Full-Stack Systems Engineer",
                "squad": "Core Systems Squad",
                "highlights": [
                    "Designed automated xG modeling pipeline integrated with live tracking cameras.",
                    "Developed distributed microservices processing real-time spatial positioning for premier coaching teams.",
                ],
            },
            {
                "period": "2016 — 2018",
                "status": "DEBUT TERM",
                "club": "Mersey Tech Foundry",
                "location": "Labs & Accelerator",
                "role": "Junior Frontend Engineer",
                "squad": "Shader & Canvas Apprentice",
                "highlights": [
                    "Pioneered canvas render tree acceleration for digital matchday programme kiosk interfaces.",
                    "Received Outstanding Academy Graduate of the Year honours for exceptional frontend prototyping.",
                ],
            },
        ],
        "education": [
            {
                "period": "2012 — 2016",
                "academy": "University of Liverpool",
                "degree": "B.Sc. (Hons) Computer Science",
                "specialization": "Distributed Systems & Graphics",
                "honours": "First Class Honours (1st)",
            },
            {
                "period": "2010 — 2012",
                "academy": "Anfield Scientific Academy",
                "degree": "Advanced STEM Diplomas",
                "specialization": "Mathematics, Computing & Physics",
                "honours": "Triple Distinction* (D*D*D*)",
            },
        ],
        "certifications": [
            {
                "year": "2024",
                "title": "UEFA Tech Hackathon Winner - 1st Place Global Innovation",
                "issuing_body": "UEFA Sports Tech Federation",
            },
            {
                "year": "2023",
                "title": "Master GPU Shader Architect (Three.js Journey)",
                "issuing_body": "Bruno Simon Guild",
            },
            {
                "year": "2022",
                "title": "AWS Certified Solutions Architect - Professional",
                "issuing_body": "Amazon Web Services",
            },
            {
                "year": "2021",
                "title": "Certified Kubernetes Administrator (CKA)",
                "issuing_body": "Cloud Native Computing Foundation (CNCF)",
            },
        ],
    }


@app.get("/api/attributes", summary="Tactical Attributes & Telemetry")
async def get_attributes():
    return {
        "player_identity": {
            "name": "Ujjwal",
            "number": "01",
            "role": "Principal Creative Technologist",
            "turf": "London, UK / Remote",
            "ovr_rating": 94,
        },
        "fut_attributes": {
            "COD": 96,
            "DBG": 94,
            "ARC": 98,
            "SPD": 92,
            "TEA": 95,
            "PHY": 91,
        },
        "radar_scores": {
            "frontend": 98,
            "webgl_3d": 95,
            "sys_arch": 96,
            "cloud_infra": 92,
            "leadership": 94,
            "direction": 90,
        },
        "honours": [
            {
                "title": "UEFA Tech Hackathon Winner",
                "season": "2024",
                "award": "1st Place Global Innovation",
            },
            {
                "title": "Awwwards Site of the Day",
                "season": "2024",
                "award": "Interactive 3D Match Engine Architecture",
            },
            {
                "title": "Three.js Specialist Certification",
                "season": "2023",
                "award": "Certified WebGL & Custom Shader Architect",
            },
            {
                "title": "Clean Code Laurel",
                "season": "2022",
                "award": "99.98% High-Volume Production SLA",
            },
        ],
    }


@app.get("/api/download-cv", summary="Download Dossier / CV")
@app.get("/download-cv", summary="Download Dossier / CV Direct Route")
async def download_cv():
    cv_content = {
        "dossier": "ANF-2025-CV",
        "candidate": "Ujjwal",
        "title": "Principal Creative Technologist & Full-Stack Architect",
        "experience_years": 8,
        "key_skills": [
            "FastAPI / Python",
            "Three.js / WebGL / GLSL",
            "Go / WebRTC / WebSockets",
            "Distributed Systems Architecture",
            "Kubernetes / Docker / Cloud Infrastructure",
        ],
        "contact": "director@anfield-tech.dev",
        "status": "Ready for Squad Registration",
    }
    return JSONResponse(
        content=cv_content,
        headers={"Content-Disposition": "attachment; filename=Ujjwal_Tactical_Dossier_CV.json"},
    )


@app.get("/health", summary="Health Check")
async def health_check():
    return {"status": "ok", "service": "portfolio-backend"}


@app.get("/{path:path}")
async def serve_html(path: str):
    """Serve static HTML pages from the public directory."""
    if path.startswith("/"):
        path = path[1:]
    # Check legacy .html aliases first
    if path in LEGACY_MAP:
        template_name = LEGACY_MAP[path]
        return FileResponse(PUBLIC_DIR / HTML_MAP[template_name])
    # Then check direct HTML pages
    if path in HTML_MAP:
        return FileResponse(PUBLIC_DIR / HTML_MAP[path])
    # Otherwise 404
    return JSONResponse({"detail": "Not found"}, status_code=404)


@app.post("/api/transfer-inquiries", summary="Transfer Inquiry")
async def create_transfer_inquiry(
    *,
    caller_name: str = Form(...),
    caller_org: Optional[str] = Form(None),
    caller_email: str = Form(...),
    engagement_type: str = Form(...),
    contract_terms: str = Form(...),
):
    """Accept transfer inquiry submission."""
    return {
        "id": 1,
        "caller_name": caller_name,
        "caller_org": caller_org,
        "caller_email": caller_email,
        "engagement_type": engagement_type,
        "contract_terms": contract_terms,
    }