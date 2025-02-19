from datetime import datetime
from sqlalchemy import Column, BigInteger, DateTime, String, Text, ForeignKey, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class UploadedImage(Base):
    __tablename__ = "uploaded_images"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    image = Column(String(length=255), nullable=False)
    uploaded_at = Column(DateTime, default=datetime.utcnow)
    file_path = Column(Text, nullable=True)

    def __repr__(self):
        return f"<UploadedImage id={self.id} image='{self.image}'>"


class Profile(Base):
    __tablename__ = "profiles"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(UUID(as_uuid=True), nullable=False, unique=True, index=True)
    display_name = Column(Text, nullable=True)
    bio = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    medications = relationship("Medication", back_populates="profile")

    def __repr__(self):
        return f"<Profile id={self.id} display_name='{self.display_name}'>"


class Medication(Base):
    __tablename__ = "medication"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    profile_id = Column(BigInteger, ForeignKey("profiles.id"), nullable=False)
    title = Column(String(length=255), nullable=True)
    scan_date = Column(DateTime, default=datetime.utcnow)
    active_ingredients = Column(Text, nullable=True)
    scanned_text = Column(Text, nullable=True)
    dosage = Column(String(length=255), nullable=True)
    prescription_details = Column(JSON, nullable=True)

    profile = relationship("Profile", back_populates="medications")

    def __repr__(self):
        return f"<Medication id={self.id} title='{self.title}'>"
