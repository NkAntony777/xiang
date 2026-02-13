# CRUD operations for Ganzhi
from sqlalchemy.orm import Session
from app.models import Ganzhi, Nayin, Xiangyi, Shensha, GanzhiShensha, Xiji, Guanxi
from typing import List, Optional


def get_ganzhi_list(db: Session, skip: int = 0, limit: int = 60) -> List[Ganzhi]:
    """Get list of all Ganzhi"""
    return db.query(Ganzhi).offset(skip).limit(limit).all()


def get_ganzhi_by_id(db: Session, ganzhi_id: int) -> Optional[Ganzhi]:
    """Get Ganzhi by ID"""
    return db.query(Ganzhi).filter(Ganzhi.id == ganzhi_id).first()


def get_ganzhi_by_name(db: Session, ganzhi_name: str) -> Optional[Ganzhi]:
    """Get Ganzhi by name (e.g., '甲子')"""
    return db.query(Ganzhi).filter(Ganzhi.ganzhi == ganzhi_name).first()


def search_ganzhi(db: Session, query: str, skip: int = 0, limit: int = 20) -> tuple:
    """
    Search Ganzhi by query string
    Returns (total_count, results)
    """
    # Build search filter
    filter_query = db.query(Ganzhi).filter(
        (Ganzhi.ganzhi.contains(query)) |
        (Ganzhi.tiangan.contains(query)) |
        (Ganzhi.dizhi.contains(query))
    )

    total = filter_query.count()
    results = filter_query.offset(skip).limit(limit).all()

    return total, results


def get_ganzhi_with_details(db: Session, ganzhi_name: str) -> Optional[dict]:
    """Get complete Ganzhi with all related data"""
    ganzhi = db.query(Ganzhi).filter(Ganzhi.ganzhi == ganzhi_name).first()
    if not ganzhi:
        return None

    # Get Nayin
    nayin = db.query(Nayin).filter(Nayin.ganzhi_id == ganzhi.id).first()

    # Get Xiangyi
    xiangyi = db.query(Xiangyi).filter(Xiangyi.ganzhi_id == ganzhi.id).all()

    # Get Shensha (through GanzhiShensha)
    shensha_ids = db.query(GanzhiShensha.shensha_id).filter(
        GanzhiShensha.ganzhi_id == ganzhi.id
    ).all()
    shensha_ids = [s[0] for s in shensha_ids]
    shensha = db.query(Shensha).filter(Shensha.id.in_(shensha_ids)).all() if shensha_ids else []

    # Get Xiji
    xiji = db.query(Xiji).filter(Xiji.ganzhi_id == ganzhi.id).all()

    # Get Guanxi (relations where this ganzhi is either ganzhi1 or ganzhi2)
    guanxi = db.query(Guanxi).filter(
        (Guanxi.ganzhi1 == ganzhi.ganzhi) |
        (Guanxi.ganzhi2 == ganzhi.ganzhi)
    ).all()

    return {
        "id": ganzhi.id,
        "tiangan": ganzhi.tiangan,
        "dizhi": ganzhi.dizhi,
        "ganzhi": ganzhi.ganzhi,
        "tiangan_wuxing": ganzhi.tiangan_wuxing,
        "dizhi_wuxing": ganzhi.dizhi_wuxing,
        "yinyang": ganzhi.yinyang,
        "fangwei": ganzhi.fangwei,
        "jijie": ganzhi.jijie,
        "tiangan_yuanshiming": ganzhi.tiangan_yuanshiming,
        "dizhi_yuanshiming": ganzhi.dizhi_yuanshiming,
        "special_desc": ganzhi.special_desc,
        "nayin": nayin,
        "xiangyi": xiangyi,
        "shensha": shensha,
        "xiji": xiji,
        "guanxi": guanxi
    }


def compare_ganzhi(db: Session, ganzhi_names: List[str]) -> List[dict]:
    """Compare multiple Ganzhi by their names"""
    results = []
    for name in ganzhi_names:
        data = get_ganzhi_with_details(db, name)
        if data:
            results.append(data)
    return results


def get_all_ganzhi_names(db: Session) -> List[str]:
    """Get all Ganzhi names (for autocomplete)"""
    ganzhis = db.query(Ganzhi).all()
    return [g.ganzhi for g in ganzhis]
