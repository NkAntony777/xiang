# Pydantic schemas for Ganzhi API
from pydantic import BaseModel
from typing import Optional, List


# Ganzhi schemas
class GanzhiBase(BaseModel):
    tiangan: str
    dizhi: str
    ganzhi: str


class GanzhiBasic(BaseModel):
    """Basic Ganzhi info for list responses"""
    id: int
    tiangan: str
    dizhi: str
    ganzhi: str
    tiangan_wuxing: Optional[str] = None
    dizhi_wuxing: Optional[str] = None
    yinyang: Optional[str] = None

    class Config:
        from_attributes = True


class GanzhiDetail(GanzhiBasic):
    """Detailed Ganzhi info"""
    fangwei: Optional[str] = None
    jijie: Optional[str] = None
    tiangan_yuanshiming: Optional[str] = None
    dizhi_yuanshiming: Optional[str] = None
    special_desc: Optional[str] = None

    class Config:
        from_attributes = True


# Nayin schemas
class NayinBase(BaseModel):
    id: int
    ganzhi_id: int
    nayin_name: Optional[str] = None
    nayin_wuxing: Optional[str] = None
    zhuangtai: Optional[str] = None
    shengda_xiaoruo: Optional[str] = None
    zhuangtai_desc: Optional[str] = None

    class Config:
        from_attributes = True


# Xiangyi schemas
class XiangyiBase(BaseModel):
    id: int
    ganzhi_id: int
    type: Optional[str] = None
    category: Optional[str] = None
    content: Optional[str] = None
    description: Optional[str] = None
    source: Optional[str] = None
    confidence: Optional[float] = None

    class Config:
        from_attributes = True


# Shensha schemas
class ShenshaBase(BaseModel):
    id: int
    name: Optional[str] = None
    type: Optional[str] = None
    check_method: Optional[str] = None
    jixiong: Optional[str] = None
    yuanwen: Optional[str] = None
    modern_desc: Optional[str] = None
    remark: Optional[str] = None

    class Config:
        from_attributes = True


class GanzhiShenshaBase(BaseModel):
    id: int
    ganzhi_id: int
    shensha_id: int
    is_zixing: bool = False

    class Config:
        from_attributes = True


# Xiji schemas
class XijiBase(BaseModel):
    id: int
    ganzhi_id: int
    type: Optional[str] = None
    target_type: Optional[str] = None
    target_value: Optional[str] = None
    remark: Optional[str] = None

    class Config:
        from_attributes = True


# Guanxi schemas
class GuanxiBase(BaseModel):
    id: int
    ganzhi1: str
    ganzhi2: str
    relation_type: Optional[str] = None
    remark: Optional[str] = None

    class Config:
        from_attributes = True


# Complete Ganzhi response with all related data
class GanzhiWithDetails(BaseModel):
    """Complete Ganzhi with all related information"""
    # Basic info
    id: int
    tiangan: str
    dizhi: str
    ganzhi: str
    tiangan_wuxing: Optional[str] = None
    dizhi_wuxing: Optional[str] = None
    yinyang: Optional[str] = None
    fangwei: Optional[str] = None
    jijie: Optional[str] = None
    tiangan_yuanshiming: Optional[str] = None
    dizhi_yuanshiming: Optional[str] = None
    special_desc: Optional[str] = None

    # Related data
    nayin: Optional[NayinBase] = None
    xiangyi: List[XiangyiBase] = []
    shensha: List[ShenshaBase] = []
    xiji: List[XijiBase] = []
    guanxi: List[GuanxiBase] = []

    class Config:
        from_attributes = True


# Compare request/response
class CompareRequest(BaseModel):
    """Request to compare multiple Ganzhi"""
    ganzhi_list: List[str]


class CompareResponse(BaseModel):
    """Response with compared Ganzhi data"""
    items: List[GanzhiWithDetails]


# Search response
class SearchResponse(BaseModel):
    """Search results response"""
    total: int
    items: List[GanzhiBasic]
