from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from .base import Base


class Bread(Base):
    """パンテーブル: BREAD"""
    __tablename__ = "BREAD"

    id        = Column(Integer, primary_key=True)
    name      = Column(String,  nullable=False)
    price     = Column(Integer, nullable=False)
    inventory = Column(Integer, nullable=False, default=0)

    purchases = relationship("Purchase", back_populates="bread", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return (
            f"<Bread(id={self.id}, name='{self.name}', "
            f"price={self.price}, inventory={self.inventory})>"
        )


class Purchase(Base):
    """売上テーブル: PURCHASE"""
    __tablename__ = "PURCHASE"

    id       = Column(Integer,  primary_key=True)
    bread_id = Column(Integer,  ForeignKey("BREAD.id"), nullable=False)
    quantity = Column(Integer,  nullable=False)
    date     = Column(DateTime, nullable=False)

    bread = relationship("Bread", back_populates="purchases")

    def __repr__(self) -> str:
        return (
            f"<Purchase(id={self.id}, bread_id={self.bread_id}, "
            f"quantity={self.quantity}, date='{self.date}')>"
        )
