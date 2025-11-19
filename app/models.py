import uuid
from datetime import datetime, timezone
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import CheckConstraint
from sqlalchemy import Enum

class PrestigeLevelEnum(str, Enum):
    HUMAN = "human"
    DEMON = "demon"

class User(db.Model):
    __tablename__ = "users"
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    username = db.Column(db.String(15), unique=True, nullable=False)
    email = db.Column(db.string(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    reset_token = db.Column(db.String(128), nullable=True)
    reset_token_expires = db.Column(db.DateTime(timezone=True), nullable=True)
    role = db.Column(db.String(50), default="player")
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f"<User {self.username}>"

class UserProfile(db.Model):
    __tablename__ = "user_profiles"
    
    id = db.Column(UUID(as_uuid=True), db.ForeignKey("users.id"), primary_key=True)
    strength = db.Column(db.Integer, default=1, nullable=False)
    spirit_energy = db.Column(db.Integer, default=1, nullable=False)
    defense = db.Column(db.Integer, default=1, nullable=False)
    agility = db.Column(db.Integer, default=1, nullable=False)
    demon_energy = db.Column(db.Integer, default=0, nullable=False)
    
    prestige = db.Column(
        db.Enum(PrestigeLevelEnum, name="prestige_levels"),
        default=PrestigeLevelEnum.HUMAN,
        nullable=False
    )
    
    user = db.relationship("User", backref=db.backref("profile", uselist=False))
    
    __table_args__ = (
        CheckConstraint('strength >= 0 AND strength <=120', name='strength_range'),
        CheckConstraint('spirit_energy >= 0 AND spirit_energy <=120', name='spirit_energy_range'),
        CheckConstraint('defense >= 0 AND defense <=120', name='defense_range'),
        CheckConstraint('agility >= 0 AND agility <=120', name='agility_range'),
        CheckConstraint('demon_energy >= 0 AND demon_energy <=120', name='demon_energy_range')
    )