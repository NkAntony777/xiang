# Shensha API Router
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app import crud
from app.schemas.shensha import (
    ShenshaResponse,
    ShenshaByGanzhiResponse,
    GanzhiShenshaResponse,
    ZixingListResponse
)

router = APIRouter(prefix="/api/shensha", tags=["神煞"])


@router.get("", response_model=List[ShenshaResponse])
def get_shensha_list(
    skip: int = Query(0, ge=0, description="Offset for pagination"),
    limit: int = Query(100, ge=1, le=100, description="Limit number of results"),
    db: Session = Depends(get_db)
):
    """
    Get list of all Shensha.
    """
    return crud.shensha.get_all_shensha(db, skip=skip, limit=limit)


@router.get("/types", response_model=List[str])
def get_shensha_types(db: Session = Depends(get_db)):
    """
    Get all unique Shensha types.
    """
    return crud.shensha.get_shensha_types(db)


@router.get("/type/{shensha_type}", response_model=List[ShenshaResponse])
def get_shensha_by_type(shensha_type: str, db: Session = Depends(get_db)):
    """
    Get all Shensha by type.
    """
    return crud.shensha.get_shensha_by_type(db, shensha_type)


@router.get("/zixing", response_model=List[ShenshaResponse])
def get_zixing_list(db: Session = Depends(get_db)):
    """
    Get all Zixing (自星) Shensha.
    """
    return crud.shensha.get_zixing_shensha(db)


@router.get("/ganzhi/{ganzhi_name}", response_model=List[ShenshaByGanzhiResponse])
def get_shensha_by_ganzhi(ganzhi_name: str, db: Session = Depends(get_db)):
    """
    Get all Shensha for a specific Ganzhi.
    """
    results = crud.shensha.get_shensha_by_ganzhi(db, ganzhi_name)
    if not results:
        # Return empty list instead of 404 for valid Ganzhi
        return []
    return results


@router.get("/{shensha_name}", response_model=ShenshaResponse)
def get_shensha_detail(shensha_name: str, db: Session = Depends(get_db)):
    """
    Get detailed information for a specific Shensha.
    """
    result = crud.shensha.get_shensha_by_name(db, shensha_name)
    if not result:
        raise HTTPException(status_code=404, detail=f"Shensha '{shensha_name}' not found")
    return result


@router.get("/{shensha_name}/ganzhi", response_model=List[GanzhiShenshaResponse])
def get_ganzhi_by_shensha(shensha_name: str, db: Session = Depends(get_db)):
    """
    Get all Ganzhi that have a specific Shensha.
    """
    results = crud.shensha.get_ganzhi_by_shensha(db, shensha_name)
    if not results:
        raise HTTPException(status_code=404, detail=f"Shensha '{shensha_name}' not found")
    return results
