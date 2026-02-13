# CRUD operations for Shensha
from sqlalchemy.orm import Session
from app.models import Shensha, GanzhiShensha, Ganzhi
from typing import List, Optional


def get_all_shensha(db: Session, skip: int = 0, limit: int = 100) -> List[Shensha]:
    """Get all Shensha"""
    return db.query(Shensha).offset(skip).limit(limit).all()


def get_shensha_by_name(db: Session, name: str) -> Optional[Shensha]:
    """Get Shensha by name"""
    return db.query(Shensha).filter(Shensha.name == name).first()


def get_shensha_by_id(db: Session, shensha_id: int) -> Optional[Shensha]:
    """Get Shensha by ID"""
    return db.query(Shensha).filter(Shensha.id == shensha_id).first()


def get_shensha_by_ganzhi(db: Session, ganzhi_name: str) -> List[dict]:
    """Get all Shensha for a specific Ganzhi"""
    ganzhi = db.query(Ganzhi).filter(Ganzhi.ganzhi == ganzhi_name).first()
    if not ganzhi:
        return []

    # Get all shensha links
    links = db.query(GanzhiShensha).filter(GanzhiShensha.ganzhi_id == ganzhi.id).all()

    results = []
    for link in links:
        shensha = db.query(Shensha).filter(Shensha.id == link.shensha_id).first()
        if shensha:
            results.append({
                "id": shensha.id,
                "name": shensha.name,
                "type": shensha.type,
                "check_method": shensha.check_method,
                "jixiong": shensha.jixiong,
                "yuanwen": shensha.yuanwen,
                "modern_desc": shensha.modern_desc,
                "remark": shensha.remark,
                "is_zixing": link.is_zixing
            })

    return results


def get_ganzhi_by_shensha(db: Session, shensha_name: str) -> List[dict]:
    """Get all Ganzhi that have a specific Shensha"""
    shensha = db.query(Shensha).filter(Shensha.name == shensha_name).first()
    if not shensha:
        return []

    # Get all links
    links = db.query(GanzhiShensha).filter(GanzhiShensha.shensha_id == shensha.id).all()

    results = []
    for link in links:
        ganzhi = db.query(Ganzhi).filter(Ganzhi.id == link.ganzhi_id).first()
        if ganzhi:
            results.append({
                "ganzhi": ganzhi.ganzhi,
                "tiangan": ganzhi.tiangan,
                "dizhi": ganzhi.dizhi,
                "is_zixing": link.is_zixing
            })

    return results


def get_zixing_shensha(db: Session) -> List[dict]:
    """Get all Shensha that are Zixing (自星)"""
    # Get all zixing links
    links = db.query(GanzhiShensha).filter(GanzhiShensha.is_zixing == True).all()

    results = []
    seen_shensha = set()

    for link in links:
        if link.shensha_id in seen_shensha:
            continue

        shensha = db.query(Shensha).filter(Shensha.id == link.shensha_id).first()
        if shensha:
            seen_shensha.add(link.shensha_id)
            results.append({
                "id": shensha.id,
                "name": shensha.name,
                "type": shensha.type,
                "check_method": shensha.check_method,
                "jixiong": shensha.jixiong,
                "yuanwen": shensha.yuanwen,
                "modern_desc": shensha.modern_desc,
                "remark": shensha.remark
            })

    return results


def get_shensha_by_type(db: Session, shensha_type: str) -> List[Shensha]:
    """Get all Shensha by type (字形神煞/组合神煞)"""
    return db.query(Shensha).filter(Shensha.type == shensha_type).all()


def get_shensha_types(db: Session) -> List[str]:
    """Get all unique Shensha types"""
    types = db.query(Shensha.type).distinct().all()
    return [t[0] for t in types if t[0]]
