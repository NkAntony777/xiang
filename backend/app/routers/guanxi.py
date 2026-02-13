# Guanxi API Router
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app import crud
from app.schemas.guanxi import (
    GuanxiResponse,
    GuanxiByGanzhiResponse,
    GuanxiBetweenResponse,
    RelationTypesResponse
)

router = APIRouter(prefix="/api/guanxi", tags=["干支关系"])


@router.get("", response_model=List[GuanxiResponse])
def get_guanxi_list(
    skip: int = Query(0, ge=0, description="Offset for pagination"),
    limit: int = Query(300, ge=1, le=500, description="Limit number of results"),
    db: Session = Depends(get_db)
):
    """
    Get list of all Guanxi relationships.
    """
    return crud.guanxi.get_all_guanxi(db, skip=skip, limit=limit)


@router.get("/types", response_model=RelationTypesResponse)
def get_relation_types(db: Session = Depends(get_db)):
    """
    Get all unique relation types.
    """
    types = crud.guanxi.get_relation_types(db)
    return {"types": types}


@router.get("/type/{relation_type}", response_model=List[GuanxiResponse])
def get_guanxi_by_type(relation_type: str, db: Session = Depends(get_db)):
    """
    Get all Guanxi relationships by relation type.
    Example: /api/guanxi/type/六合
    """
    return crud.guanxi.get_guanxi_by_type(db, relation_type)


@router.get("/ganzhi/{ganzhi_name}", response_model=List[GuanxiByGanzhiResponse])
def get_guanxi_by_ganzhi(ganzhi_name: str, db: Session = Depends(get_db)):
    """
    Get all Guanxi relationships for a specific Ganzhi.
    """
    return crud.guanxi.get_guanxi_by_ganzhi(db, ganzhi_name)


@router.get("/between/{ganzhi1}/{ganzhi2}", response_model=GuanxiBetweenResponse)
def get_guanxi_between(ganzhi1: str, ganzhi2: str, db: Session = Depends(get_db)):
    """
    Get the Guanxi relationship between two specific Ganzhi.
    Example: /api/guanxi/between/甲子/乙丑
    """
    result = crud.guanxi.get_guanxi_between(db, ganzhi1, ganzhi2)
    if not result:
        raise HTTPException(
            status_code=404,
            detail=f"No relationship found between {ganzhi1} and {ganzhi2}"
        )
    return result
