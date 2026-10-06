import re
from datetime import datetime, timezone
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator
from sqlalchemy import Column, DateTime, Integer, String, Text

from database import Base


# ==========================================
# SQLAlchemy ORM Models
# ==========================================
class TransferInquiry(Base):
    __tablename__ = "transfer_inquiries"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    caller_name = Column(String(255), nullable=False)
    caller_org = Column(String(255), nullable=True)
    caller_email = Column(String(255), nullable=False)
    engagement_type = Column(String(100), nullable=False)
    contract_terms = Column(Text, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)


# ==========================================
# Pydantic Validation & Serialization Schemas
# ==========================================
EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9_.+-]+@([a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}$")


class TransferInquiryCreate(BaseModel):
    caller_name: str = Field(..., min_length=1, description="Full Name or Agent Name")
    caller_org: Optional[str] = Field(default=None, description="Club or Organization (optional)")
    caller_email: str = Field(..., min_length=3, description="Official Contact Email")
    engagement_type: str = Field(..., min_length=1, description="Engagement Nature / Role Scope")
    contract_terms: str = Field(..., min_length=1, description="Tactical Objectives & Terms")

    @field_validator("caller_name", "engagement_type", "contract_terms")
    @classmethod
    def check_non_empty_stripped(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Field cannot be empty or whitespace only")
        return v.strip()

    @field_validator("caller_email")
    @classmethod
    def check_valid_email(cls, v: str) -> str:
        stripped = v.strip() if v else ""
        if not EMAIL_REGEX.match(stripped):
            raise ValueError("Invalid email address format")
        return stripped


class TransferInquiryResponse(BaseModel):
    id: int
    caller_name: str
    caller_org: Optional[str] = None
    caller_email: str
    engagement_type: str
    contract_terms: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
