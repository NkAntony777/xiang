# Nayin API Router
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app import crud
from app.schemas.nayin import (
    NayinByGanzhiResponse,
    NayinByNayinResponse,
    NayinStatusListResponse,
    NayinCalcResponse
)

router = APIRouter(prefix="/api/nayin", tags=["纳音"])


@router.get("/by-ganzhi/{ganzhi}", response_model=NayinByGanzhiResponse)
def get_nayin_by_ganzhi(ganzhi: str, db: Session = Depends(get_db)):
    """
    Get Nayin info by Ganzhi name.
    Returns: nayin_name, nayin_wuxing, zhuangtai, shengda_xiaoruo, etc.
    """
    result = crud.nayin.get_nayin_by_ganzhi(db, ganzhi)
    if not result:
        raise HTTPException(status_code=404, detail=f"Nayin for Ganzhi '{ganzhi}' not found")
    return result


@router.get("/{nayin_name}/ganzhi", response_model=List[NayinByNayinResponse])
def get_ganzhi_by_nayin(nayin_name: str, db: Session = Depends(get_db)):
    """
    Get all Ganzhi with a specific Nayin name.
    Example: /api/nayin/海中金/ganzhi returns [甲子, 乙丑]
    """
    results = crud.nayin.get_ganzhi_by_nayin(db, nayin_name)
    if not results:
        raise HTTPException(status_code=404, detail=f"Nayin '{nayin_name}' not found")
    return results


@router.get("", response_model=List[NayinByNayinResponse])
def get_all_nayin(db: Session = Depends(get_db)):
    """Get all Nayin records with their Ganzhi."""
    all_categories = crud.nayin.get_all_nayin_categories(db)
    results = []
    for nayin_name, data in all_categories.items():
        for gz in data.get("ganzhi_list", []):
            results.append({
                "ganzhi": gz["ganzhi"],
                "tiangan": gz["tiangan"],
                "dizhi": gz["dizhi"],
                "nayin_name": data["nayin_name"],
                "nayin_wuxing": data["nayin_wuxing"],
                "zhuangtai": gz["zhuangtai"],
                "shengda_xiaoruo": data["shengda_xiaoruo"]
            })
    return results


@router.get("/status", response_model=NayinStatusListResponse)
def get_status_list(db: Session = Depends(get_db)):
    """Get all available status (十二长生) values."""
    statuses = crud.nayin.get_status_list(db)
    return {"statuses": statuses}


@router.get("/status/{status}", response_model=List[NayinByNayinResponse])
def get_nayin_by_status(status: str, db: Session = Depends(get_db)):
    """
    Get all Ganzhi with a specific status.
    Example: /api/nayin/status/帝旺 returns all Ganzhi in 帝旺 state
    """
    results = crud.nayin.get_nayin_by_status(db, status)
    if not results:
        raise HTTPException(status_code=404, detail=f"No Ganzhi found with status '{status}'")
    return results


@router.get("/category/{category}", response_model=List[NayinByNayinResponse])
def get_nayin_by_category(category: str, db: Session = Depends(get_db)):
    """
    Get Nayin by category: shengda (盛大) or xiaoruo (小弱).
    Example: /api/nayin/category/shengda
    """
    if category not in ["shengda", "xiaoruo"]:
        raise HTTPException(status_code=400, detail="Category must be 'shengda' or 'xiaoruo'")

    results = crud.nayin.get_nayin_by_category(db, category)
    if not results:
        raise HTTPException(status_code=404, detail=f"No Ganzhi found in category '{category}'")
    return results


@router.get("/calc/{ganzhi}", response_model=NayinCalcResponse)
def calc_nayin(ganzhi: str):
    """
    Calculate Nayin using different methods.
    Returns step-by-step calculation for educational purposes.
    """
    result = crud.nayin.calc_nayin(ganzhi)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result
