# Admin API Router
# Provides CRUD operations for all entities and import/export functionality
from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from typing import List
import json
import io

from app.database import get_db
from app.models import Ganzhi, Nayin, Xiangyi, Shensha, GanzhiShensha, Xiji, Guanxi

router = APIRouter(prefix="/api/admin", tags=["管理"])


# ==================== Statistics ====================

@router.get("/stats")
def get_database_stats(db: Session = Depends(get_db)):
    """
    Get database statistics.
    """
    return {
        "ganzhi_count": db.query(Ganzhi).count(),
        "nayin_count": db.query(Nayin).count(),
        "xiangyi_count": db.query(Xiangyi).count(),
        "shensha_count": db.query(Shensha).count(),
        "ganzhi_shensha_count": db.query(GanzhiShensha).count(),
        "xiji_count": db.query(Xiji).count(),
        "guanxi_count": db.query(Guanxi).count(),
    }


# ==================== Ganzhi CRUD ====================

@router.get("/ganzhi")
def get_all_ganzhi_admin(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Get all Ganzhi (admin)"""
    return db.query(Ganzhi).offset(skip).limit(limit).all()


@router.get("/ganzhi/{ganzhi_name}")
def get_ganzhi_admin(ganzhi_name: str, db: Session = Depends(get_db)):
    """Get single Ganzhi (admin)"""
    g = db.query(Ganzhi).filter(Ganzhi.ganzhi == ganzhi_name).first()
    if not g:
        raise HTTPException(status_code=404, detail="Ganzhi not found")
    return g


# ==================== Nayin CRUD ====================

@router.get("/nayin")
def get_all_nayin_admin(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Get all Nayin (admin)"""
    return db.query(Nayin).offset(skip).limit(limit).all()


# ==================== Xiangyi CRUD ====================

@router.get("/xiangyi")
def get_all_xiangyi_admin(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db)
):
    """Get all Xiangyi (admin)"""
    return db.query(Xiangyi).offset(skip).limit(limit).all()


# ==================== Shensha CRUD ====================

@router.get("/shensha")
def get_all_shensha_admin(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Get all Shensha (admin)"""
    return db.query(Shensha).offset(skip).limit(limit).all()


@router.get("/ganzhi-shensha")
def get_all_ganzhi_shensha_admin(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db)
):
    """Get all Ganzhi-Shensha relationships (admin)"""
    return db.query(GanzhiShensha).offset(skip).limit(limit).all()


# ==================== Xiji CRUD ====================

@router.get("/xiji")
def get_all_xiji_admin(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db)
):
    """Get all Xiji (admin)"""
    return db.query(Xiji).offset(skip).limit(limit).all()


# ==================== Guanxi CRUD ====================

@router.get("/guanxi")
def get_all_guanxi_admin(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db)
):
    """Get all Guanxi (admin)"""
    return db.query(Guanxi).offset(skip).limit(limit).all()


# ==================== Export ====================

@router.get("/export/ganzhi")
def export_ganzhi(db: Session = Depends(get_db)):
    """Export all Ganzhi as JSON"""
    data = db.query(Ganzhi).all()
    result = []
    for g in data:
        result.append({
            "id": g.id,
            "tiangan": g.tiangan,
            "dizhi": g.dizhi,
            "ganzhi": g.ganzhi,
            "tiangan_wuxing": g.tiangan_wuxing,
            "dizhi_wuxing": g.dizhi_wuxing,
            "yinyang": g.yinyang,
            "fangwei": g.fangwei,
            "jijie": g.jijie,
            "tiangan_yuanshiming": g.tiangan_yuanshiming,
            "dizhi_yuanshiming": g.dizhi_yuanshiming,
            "special_desc": g.special_desc,
        })

    json_str = json.dumps(result, ensure_ascii=False, indent=2)
    return StreamingResponse(
        io.BytesIO(json_str.encode("utf-8")),
        media_type="application/json",
        headers={"Content-Disposition": "attachment; filename=ganzhi.json"}
    )


@router.get("/export/nayin")
def export_nayin(db: Session = Depends(get_db)):
    """Export all Nayin as JSON"""
    data = db.query(Nayin).all()
    result = []
    for n in data:
        result.append({
            "id": n.id,
            "ganzhi_id": n.ganzhi_id,
            "nayin_name": n.nayin_name,
            "nayin_wuxing": n.nayin_wuxing,
            "zhuangtai": n.zhuangtai,
            "shengda_xiaoruo": n.shengda_xiaoruo,
            "zhuangtai_desc": n.zhuangtai_desc,
        })

    json_str = json.dumps(result, ensure_ascii=False, indent=2)
    return StreamingResponse(
        io.BytesIO(json_str.encode("utf-8")),
        media_type="application/json",
        headers={"Content-Disposition": "attachment; filename=nayin.json"}
    )


@router.get("/export/xiangyi")
def export_xiangyi(db: Session = Depends(get_db)):
    """Export all Xiangyi as JSON"""
    data = db.query(Xiangyi).all()
    result = []
    for x in data:
        result.append({
            "id": x.id,
            "ganzhi_id": x.ganzhi_id,
            "type": x.type,
            "category": x.category,
            "content": x.content,
            "description": x.description,
            "source": x.source,
            "confidence": x.confidence,
        })

    json_str = json.dumps(result, ensure_ascii=False, indent=2)
    return StreamingResponse(
        io.BytesIO(json_str.encode("utf-8")),
        media_type="application/json",
        headers={"Content-Disposition": "attachment; filename=xiangyi.json"}
    )


@router.get("/export/shensha")
def export_shensha(db: Session = Depends(get_db)):
    """Export all Shensha as JSON"""
    data = db.query(Shensha).all()
    result = []
    for s in data:
        result.append({
            "id": s.id,
            "name": s.name,
            "type": s.type,
            "check_method": s.check_method,
            "jixiong": s.jixiong,
            "yuanwen": s.yuanwen,
            "modern_desc": s.modern_desc,
            "remark": s.remark,
        })

    json_str = json.dumps(result, ensure_ascii=False, indent=2)
    return StreamingResponse(
        io.BytesIO(json_str.encode("utf-8")),
        media_type="application/json",
        headers={"Content-Disposition": "attachment; filename=shensha.json"}
    )


@router.get("/export/all")
def export_all(db: Session = Depends(get_db)):
    """Export all data as JSON"""
    data = {
        "ganzhi": [],
        "nayin": [],
        "xiangyi": [],
        "shensha": [],
        "ganzhi_shensha": [],
        "xiji": [],
        "guanxi": [],
    }

    # Export Ganzhi
    for g in db.query(Ganzhi).all():
        data["ganzhi"].append({
            "id": g.id,
            "tiangan": g.tiangan,
            "dizhi": g.dizhi,
            "ganzhi": g.ganzhi,
            "tiangan_wuxing": g.tiangan_wuxing,
            "dizhi_wuxing": g.dizhi_wuxing,
            "yinyang": g.yinyang,
            "fangwei": g.fangwei,
            "jijie": g.jijie,
        })

    # Export Nayin
    for n in db.query(Nayin).all():
        data["nayin"].append({
            "id": n.id,
            "ganzhi_id": n.ganzhi_id,
            "nayin_name": n.nayin_name,
            "nayin_wuxing": n.nayin_wuxing,
            "zhuangtai": n.zhuangtai,
            "shengda_xiaoruo": n.shengda_xiaoruo,
        })

    # Export Xiangyi
    for x in db.query(Xiangyi).all():
        data["xiangyi"].append({
            "id": x.id,
            "ganzhi_id": x.ganzhi_id,
            "type": x.type,
            "category": x.category,
            "content": x.content,
            "description": x.description,
        })

    # Export Shensha
    for s in db.query(Shensha).all():
        data["shensha"].append({
            "id": s.id,
            "name": s.name,
            "type": s.type,
            "jixiong": s.jixiong,
        })

    # Export Guanxi
    for g in db.query(Guanxi).all():
        data["guanxi"].append({
            "id": g.id,
            "ganzhi1": g.ganzhi1,
            "ganzhi2": g.ganzhi2,
            "relation_type": g.relation_type,
            "remark": g.remark,
        })

    json_str = json.dumps(data, ensure_ascii=False, indent=2)
    return StreamingResponse(
        io.BytesIO(json_str.encode("utf-8")),
        media_type="application/json",
        headers={"Content-Disposition": "attachment; filename=liushijiazi_all.json"}
    )


# ==================== Import ====================

@router.post("/import/ganzhi")
def import_ganzhi(data: List[dict], db: Session = Depends(get_db)):
    """Import Ganzhi data (replace all)"""
    # Clear existing
    db.query(Ganzhi).delete()

    # Insert new
    for item in data:
        g = Ganzhi(
            tiangan=item.get("tiangan", ""),
            dizhi=item.get("dizhi", ""),
            ganzhi=item.get("ganzhi", ""),
            tiangan_wuxing=item.get("tiangan_wuxing", ""),
            dizhi_wuxing=item.get("dizhi_wuxing", ""),
            yinyang=item.get("yinyang", ""),
            fangwei=item.get("fangwei", ""),
            jijie=item.get("jijie", ""),
            tiangan_yuanshiming=item.get("tiangan_yuanshiming", ""),
            dizhi_yuanshiming=item.get("dizhi_yuanshiming", ""),
            special_desc=item.get("special_desc", ""),
        )
        db.add(g)

    db.commit()
    return {"imported": len(data), "table": "ganzhi"}


@router.post("/import/nayin")
def import_nayin(data: List[dict], db: Session = Depends(get_db)):
    """Import Nayin data (replace all)"""
    db.query(Nayin).delete()

    for item in data:
        n = Nayin(
            ganzhi_id=item.get("ganzhi_id", 1),
            nayin_name=item.get("nayin_name", ""),
            nayin_wuxing=item.get("nayin_wuxing", ""),
            zhuangtai=item.get("zhuangtai", ""),
            shengda_xiaoruo=item.get("shengda_xiaoruo", ""),
            zhuangtai_desc=item.get("zhuangtai_desc", ""),
        )
        db.add(n)

    db.commit()
    return {"imported": len(data), "table": "nayin"}


# ==================== Health Check ====================

@router.get("/health")
def admin_health_check():
    """Admin API health check"""
    return {"status": "healthy", "service": "admin-api"}
