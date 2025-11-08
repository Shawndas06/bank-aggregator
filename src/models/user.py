from sqlalchemy import Column, Integer, String, Date, Boolean, DateTime, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from src.database import Base
from src.constants.constants import AccountType

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    name = Column(String(255), nullable=False)
    birth_date = Column(Date, nullable=False)
    account_type = Column(
        Enum(AccountType),
        default=AccountType.FREE,
        nullable=False
    )
    is_verified = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    bank_accounts = relationship("BankAccount", back_populates="user", cascade="all, delete-orphan")
    group_memberships = relationship("GroupMember", back_populates="user", cascade="all, delete-orphan")
    owned_groups = relationship("Group", back_populates="owner", cascade="all, delete-orphan")
    sent_invitations = relationship(
        "Invitation",
        foreign_keys="[Invitation.inviter_id]",
        back_populates="inviter",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<User(id={self.id}, email={self.email}, name={self.name})>"
