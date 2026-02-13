# CRUD operations for Guanxi
from sqlalchemy.orm import Session
from app.models import Guanxi, Ganzhi
from typing import List, Optional


def get_all_guanxi(db: Session, skip: int = 0, limit: int = 300) -> List[Guanxi]:
    """Get all Guanxi relationships"""
    return db.query(Guanxi).offset(skip).limit(limit).all()


def get_guanxi_by_id(db: Session, guanxi_id: int) -> Optional[Guanxi]:
    """Get Guanxi by ID"""
    return db.query(Guanxi).filter(Guanxi.id == guanxi_id).first()


def get_guanxi_by_type(db: Session, relation_type: str) -> List[dict]:
    """Get all Guanxi by relation type"""
    relationships = db.query(Guanxi).filter(Guanxi.relation_type == relation_type).all()

    results = []
    for rel in relationships:
        results.append({
            "id": rel.id,
            "ganzhi1": rel.ganzhi1,
            "ganzhi2": rel.ganzhi2,
            "relation_type": rel.relation_type,
            "remark": rel.remark
        })

    return results


def get_guanxi_by_ganzhi(db: Session, ganzhi_name: str) -> List[dict]:
    """Get all Guanxi relationships for a specific Ganzhi"""
    relationships = db.query(Guanxi).filter(
        (Guanxi.ganzhi1 == ganzhi_name) | (Guanxi.ganzhi2 == ganzhi_name)
    ).all()

    results = []
    for rel in relationships:
        # Determine which is the "other" ganzhi
        other_ganzhi = rel.ganzhi2 if rel.ganzhi1 == ganzhi_name else rel.ganzhi1

        results.append({
            "id": rel.id,
            "ganzhi1": rel.ganzhi1,
            "ganzhi2": rel.ganzhi2,
            "relation_type": rel.relation_type,
            "remark": rel.remark,
            "other_ganzhi": other_ganzhi
        })

    return results


def get_guanxi_between(db: Session, ganzhi1: str, ganzhi2: str) -> Optional[dict]:
    """Get the Guanxi relationship between two specific Ganzhi"""
    rel = db.query(Guanxi).filter(
        ((Guanxi.ganzhi1 == ganzhi1) & (Guanxi.ganzhi2 == ganzhi2)) |
        ((Guanxi.ganzhi1 == ganzhi2) & (Guanxi.ganzhi2 == ganzhi1))
    ).first()

    if not rel:
        return None

    return {
        "id": rel.id,
        "ganzhi1": rel.ganzhi1,
        "ganzhi2": rel.ganzhi2,
        "relation_type": rel.relation_type,
        "remark": rel.remark
    }


def get_relation_types(db: Session) -> List[str]:
    """Get all unique relation types"""
    types = db.query(Guanxi.relation_type).distinct().all()
    return [t[0] for t in types if t[0]]


def get_ganzhi_pairs_by_type(db: Session, relation_type: str) -> List[dict]:
    """Get all Ganzhi pairs for a specific relation type"""
    relationships = db.query(Guanxi).filter(Guanxi.relation_type == relation_type).all()

    results = []
    for rel in relationships:
        results.append({
            "ganzhi1": rel.ganzhi1,
            "ganzhi2": rel.ganzhi2,
            "remark": rel.remark
        })

    return results
