import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database import Base, get_db
from main import app
from models import TransferInquiry

# Use an in-memory SQLite database or test SQLite for isolated test runs
TEST_DATABASE_URL = "sqlite:///./test_portfolio.db"
test_engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(autouse=True, scope="module")
def setup_database():
    Base.metadata.create_all(bind=test_engine)
    yield
    Base.metadata.drop_all(bind=test_engine)


client = TestClient(app)


# =================================================================
# 1. HTML Page Routes (All must return HTTP 200)
# =================================================================
@pytest.mark.parametrize(
    "path",
    [
        "/",
        "/hero_page.html",
        "/about",
        "/about_me.html",
        "/projects",
        "/project.html",
        "/experience",
        "/contect_and_match_record.html",
        "/contact",
        "/transfer_desk.html",
        "/attributes",
        "/atribute.html",
    ],
)
def test_html_pages_return_200(path: str):
    response = client.get(path)
    assert response.status_code == 200, f"Route {path} did not return 200. Got {response.status_code}"
    assert "text/html" in response.headers.get("content-type", "")
    assert len(response.text) > 0


# =================================================================
# 2. Form Submission - Valid Payload (Returns HTTP 200 & Persists)
# =================================================================
def test_valid_inquiry_submission():
    payload = {
        "caller_name": "Jürgen Klopp",
        "caller_org": "Red Bull Global Soccer",
        "caller_email": "jurgen@redbull.football",
        "engagement_type": "lead-architect",
        "contract_terms": "Lead tactical graphics engine for next-gen telemetry broadcast across European fixtures.",
    }
    response = client.post("/api/transfer-inquiries", json=payload)
    assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"

    data = response.json()
    assert "id" in data
    assert data["caller_name"] == payload["caller_name"]
    assert data["caller_org"] == payload["caller_org"]
    assert data["caller_email"] == payload["caller_email"]
    assert data["engagement_type"] == payload["engagement_type"]
    assert data["contract_terms"] == payload["contract_terms"]
    assert "created_at" in data

    # Verify persistence in database
    db = TestingSessionLocal()
    inquiry = db.query(TransferInquiry).filter(TransferInquiry.id == data["id"]).first()
    assert inquiry is not None
    assert inquiry.caller_name == "Jürgen Klopp"
    db.close()


# =================================================================
# 3. Form Submission - Optional Field Omitted (Returns HTTP 200)
# =================================================================
def test_optional_field_omitted_submission():
    payload = {
        "caller_name": "Independent Scout",
        "caller_email": "scout@anfield.io",
        "engagement_type": "advisory",
        "contract_terms": "Reviewing 3D WebGL performance caps and memory footprint.",
    }
    response = client.post("/api/transfer-inquiries", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["caller_org"] is None
    assert data["caller_name"] == "Independent Scout"


# =================================================================
# 4. Form Submission - Missing Required Field (Returns HTTP 422)
# =================================================================
@pytest.mark.parametrize(
    "missing_field",
    ["caller_name", "caller_email", "engagement_type", "contract_terms"],
)
def test_missing_required_field_returns_422(missing_field: str):
    valid_payload = {
        "caller_name": "Pep L.",
        "caller_org": "Tactical Labs",
        "caller_email": "pep@tactical.dev",
        "engagement_type": "technical-leadership",
        "contract_terms": "Overseeing frontend distributed architecture.",
    }
    payload = {k: v for k, v in valid_payload.items() if k != missing_field}
    response = client.post("/api/transfer-inquiries", json=payload)
    assert response.status_code == 422, f"Expected 422 when missing {missing_field}, got {response.status_code}"


def test_empty_string_required_field_returns_422():
    payload = {
        "caller_name": "   ",  # whitespace only
        "caller_email": "test@example.com",
        "engagement_type": "advisory",
        "contract_terms": "Valid terms",
    }
    response = client.post("/api/transfer-inquiries", json=payload)
    assert response.status_code == 422


# =================================================================
# 5. Form Submission - Invalid Email Format (Returns HTTP 422)
# =================================================================
@pytest.mark.parametrize(
    "invalid_email",
    [
        "plainaddress",
        "@missingusername.com",
        "username@.com",
        "username@domain..com",
        "username@domain,com",
        "invalid email@domain.com",
    ],
)
def test_invalid_email_format_returns_422(invalid_email: str):
    payload = {
        "caller_name": "Director of Football",
        "caller_email": invalid_email,
        "engagement_type": "contract-webgl",
        "contract_terms": "Volumetric shader architecture consultancy.",
    }
    response = client.post("/api/transfer-inquiries", json=payload)
    assert response.status_code == 422, f"Expected 422 for email '{invalid_email}', got {response.status_code}"


# =================================================================
# 6. Dynamic API Endpoints Tests
# =================================================================
def test_api_projects_endpoint():
    response = client.get("/api/projects")
    assert response.status_code == 200
    data = response.json()
    assert "projects" in data
    assert len(data["projects"]) >= 11
    assert data["formation"] == "4-3-3 Attack"


def test_api_records_endpoint():
    response = client.get("/api/records")
    assert response.status_code == 200
    data = response.json()
    assert "experience" in data
    assert "education" in data
    assert "certifications" in data
    assert len(data["experience"]) >= 4


def test_api_attributes_endpoint():
    response = client.get("/api/attributes")
    assert response.status_code == 200
    data = response.json()
    assert "fut_attributes" in data
    assert data["fut_attributes"]["ARC"] == 98
    assert "radar_scores" in data


def test_api_download_cv_endpoint():
    response = client.get("/api/download-cv")
    assert response.status_code == 200
    data = response.json()
    assert data["dossier"] == "ANF-2025-CV"


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
