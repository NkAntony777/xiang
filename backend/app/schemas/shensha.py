# Pydantic schemas for Shensha API
from pydantic import BaseModel
from typing import Optional, List


class ShenshaBase(BaseModel):
    """Base Shensha schema"""
    name: str
    type: Optional[str] = None
    check_method: Optional[str] = None
    jixiong: Optional[str] = None
    yuanwen: Optional[str] = None
    modern_desc: Optional[str] = None
    remark: Optional[str] = None

    class Config:
        from_attributes = True


class ShenshaResponse(ShenshaBase):
    """Shensha response"""
    id: int


class ShenshaWithGanzhi(ShenshaBase):
    """Shensha with Ganzhi list"""
    id: int
    ganzhi_list: List[dict] = []

    class Config:
        from_attributes = True


class GanzhiShenshaResponse(BaseModel):
    """Ganzhi-Shensha relationship response"""
    ganzhi: str
    tiangan: str
    dizhi: str
    is_zixing: bool = False

    class Config:
        from_attributes = True


class ShenshaByGanzhiResponse(BaseModel):
    """Shensha list for a specific Ganzhi"""
    id: int
    name: str
    type: Optional[str] = None
    check_method: Optional[str] = None
    jixiong: Optional[str] = None
    yuanwen: Optional[str] = None
    modern_desc: Optional[str] = None
    remark: Optional[str] = None
    is_zixing: bool = False

    class Config:
        from_attributes = True


class ZixingListResponse(BaseModel):
    """Zixing (自星) Shensha list"""
    items: List[ShenshaResponse]
