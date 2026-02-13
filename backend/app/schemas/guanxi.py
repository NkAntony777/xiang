# Pydantic schemas for Guanxi API
from pydantic import BaseModel
from typing import Optional, List


class GuanxiBase(BaseModel):
    """Base Guanxi schema"""
    ganzhi1: str
    ganzhi2: str
    relation_type: Optional[str] = None
    remark: Optional[str] = None

    class Config:
        from_attributes = True


class GuanxiResponse(GuanxiBase):
    """Guanxi response"""
    id: int


class GuanxiByGanzhiResponse(BaseModel):
    """Guanxi relationship for a specific Ganzhi"""
    id: int
    ganzhi1: str
    ganzhi2: str
    relation_type: Optional[str] = None
    remark: Optional[str] = None
    other_ganzhi: str


class GuanxiBetweenResponse(BaseModel):
    """Guanxi between two Ganzhi"""
    id: int
    ganzhi1: str
    ganzhi2: str
    relation_type: Optional[str] = None
    remark: Optional[str] = None


class GuanxiListResponse(BaseModel):
    """List of Guanxi relationships"""
    items: List[GuanxiResponse]
    total: int


class RelationTypesResponse(BaseModel):
    """List of relation types"""
    types: List[str]
