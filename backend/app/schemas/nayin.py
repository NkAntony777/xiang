# Pydantic schemas for Nayin API
from pydantic import BaseModel
from typing import Optional, List


class NayinByGanzhiResponse(BaseModel):
    """Response for Nayin by Ganzhi"""
    ganzhi: str
    tiangan: str
    dizhi: str
    nayin_name: Optional[str] = None
    nayin_wuxing: Optional[str] = None
    zhuangtai: Optional[str] = None
    shengda_xiaoruo: Optional[str] = None
    zhuangtai_desc: Optional[str] = None


class NayinByNayinResponse(BaseModel):
    """Response for Ganzhi by Nayin or Status"""
    ganzhi: str
    tiangan: str
    dizhi: str
    nayin_name: Optional[str] = None
    nayin_wuxing: Optional[str] = None
    zhuangtai: Optional[str] = None
    shengda_xiaoruo: Optional[str] = None


class NayinStatusListResponse(BaseModel):
    """Response for status list"""
    statuses: List[str]


class NayinCalcMethod(BaseModel):
    """Single calculation method"""
    name: str
    result: Optional[str] = None
    description: str


class NayinCalcResponse(BaseModel):
    """Response for Nayin calculation"""
    ganzhi: str
    tiangan: str
    dizhi: str
    tiangan_wuxing: str
    dizhi_wuxing: str
    methods: List[NayinCalcMethod]
