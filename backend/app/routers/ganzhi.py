# Ganzhi API Router
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app import crud
from app.schemas.ganzhi import (
    GanzhiBasic,
    GanzhiWithDetails,
    SearchResponse,
    CompareRequest,
    CompareResponse
)

router = APIRouter(prefix="/api/ganzhi", tags=["干支"])


@router.get("", response_model=List[GanzhiBasic])
def get_ganzhi_list(
    skip: int = Query(0, ge=0, description="Offset for pagination"),
    limit: int = Query(60, ge=1, le=60, description="Limit number of results"),
    db: Session = Depends(get_db)
):
    """
    Get list of all 60 Ganzhi.
    """
    return crud.ganzhi.get_ganzhi_list(db, skip=skip, limit=limit)


@router.get("/search", response_model=SearchResponse)
def search_ganzhi(
    q: str = Query(..., min_length=1, description="Search query"),
    skip: int = Query(0, ge=0, description="Offset for pagination"),
    limit: int = Query(20, ge=1, le=60, description="Limit number of results"),
    db: Session = Depends(get_db)
):
    """
    Search Ganzhi by query string.
    Supports fuzzy search by ganzhi name, tiangan, or dizhi.
    """
    total, items = crud.ganzhi.search_ganzhi(db, query=q, skip=skip, limit=limit)
    return {"total": total, "items": items}


@router.get("/names", response_model=List[str])
def get_ganzhi_names(db: Session = Depends(get_db)):
    """
    Get all Ganzhi names (for autocomplete).
    """
    return crud.ganzhi.get_all_ganzhi_names(db)


@router.get("/{ganzhi_name}", response_model=GanzhiWithDetails)
def get_ganzhi_detail(ganzhi_name: str, db: Session = Depends(get_db)):
    """
    Get detailed information for a specific Ganzhi.

    Returns:
    - Basic info (tiangan, dizhi, wuxing, yinyang, etc.)
    - Nayin info
    - Xiangyi (象意) list
    - Shensha (神煞) list
    - Xiji (喜忌) list
    - Guanxi (关系) list
    """
    result = crud.ganzhi.get_ganzhi_with_details(db, ganzhi_name)
    if not result:
        raise HTTPException(status_code=404, detail=f"Ganzhi '{ganzhi_name}' not found")
    return result


@router.post("/compare", response_model=CompareResponse)
def compare_ganzhi(request: CompareRequest, db: Session = Depends(get_db)):
    """
    Compare multiple Ganzhi (2-4 items).

    Request body:
    - ganzhi_list: List of Ganzhi names to compare
    """
    if len(request.ganzhi_list) < 2:
        raise HTTPException(status_code=400, detail="At least 2 Ganzhi required for comparison")

    if len(request.ganzhi_list) > 4:
        raise HTTPException(status_code=400, detail="Maximum 4 Ganzhi can be compared at once")

    results = crud.ganzhi.compare_ganzhi(db, request.ganzhi_list)

    if not results:
        raise HTTPException(status_code=404, detail="No valid Ganzhi found")

    # Verify all requested Ganzhi were found
    found_names = {r['ganzhi'] for r in results}
    missing = set(request.ganzhi_list) - found_names
    if missing:
        raise HTTPException(status_code=404, detail=f"Ganzhi not found: {', '.join(missing)}")

    return {"items": results}
