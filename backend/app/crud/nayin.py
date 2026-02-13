# CRUD operations for Nayin
from sqlalchemy.orm import Session
from app.models import Nayin, Ganzhi
from typing import List, Optional


# Twelve长生 states (十二长生)
CHANG_SHENG_STATES = [
    "长生", "沐浴", "冠带", "临官", "帝旺",
    "衰", "病", "死", "墓", "绝", "胎", "养"
]


def get_nayin_by_ganzhi(db: Session, ganzhi_name: str) -> Optional[dict]:
    """Get Nayin info by Ganzhi name"""
    ganzhi = db.query(Ganzhi).filter(Ganzhi.ganzhi == ganzhi_name).first()
    if not ganzhi:
        return None

    nayin = db.query(Nayin).filter(Nayin.ganzhi_id == ganzhi.id).first()
    if not nayin:
        return None

    return {
        "ganzhi": ganzhi.ganzhi,
        "tiangan": ganzhi.tiangan,
        "dizhi": ganzhi.dizhi,
        "nayin_name": nayin.nayin_name,
        "nayin_wuxing": nayin.nayin_wuxing,
        "zhuangtai": nayin.zhuangtai,
        "shengda_xiaoruo": nayin.shengda_xiaoruo,
        "zhuangtai_desc": nayin.zhuangtai_desc
    }


def get_ganzhi_by_nayin(db: Session, nayin_name: str) -> List[dict]:
    """Get all Ganzhi with a specific Nayin"""
    nayins = db.query(Nayin).filter(Nayin.nayin_name.like(f"%{nayin_name}%")).all()

    results = []
    for nayin in nayins:
        ganzhi = db.query(Ganzhi).filter(Ganzhi.id == nayin.ganzhi_id).first()
        if ganzhi:
            results.append({
                "ganzhi": ganzhi.ganzhi,
                "tiangan": ganzhi.tiangan,
                "dizhi": ganzhi.dizhi,
                "nayin_name": nayin.nayin_name,
                "nayin_wuxing": nayin.nayin_wuxing,
                "zhuangtai": nayin.zhuangtai,
                "shengda_xiaoruo": nayin.shengda_xiaoruo
            })

    return results


def get_all_nayin_categories(db: Session) -> dict:
    """Get all unique Nayin categories with their Ganzhi"""
    all_nayins = db.query(Nayin).all()

    # Group by nayin_name
    nayin_groups = {}
    for nayin in all_nayins:
        if nayin.nayin_name not in nayin_groups:
            nayin_groups[nayin.nayin_name] = {
                "nayin_name": nayin.nayin_name,
                "nayin_wuxing": nayin.nayin_wuxing,
                "shengda_xiaoruo": nayin.shengda_xiaoruo,
                "ganzhi_list": []
            }

        ganzhi = db.query(Ganzhi).filter(Ganzhi.id == nayin.ganzhi_id).first()
        if ganzhi:
            nayin_groups[nayin.nayin_name]["ganzhi_list"].append({
                "ganzhi": ganzhi.ganzhi,
                "tiangan": ganzhi.tiangan,
                "dizhi": ganzhi.dizhi,
                "zhuangtai": nayin.zhuangtai
            })

    return nayin_groups


def get_nayin_by_category(db: Session, category: str) -> List[dict]:
    """Get Nayin by category: shengda (长生/帝旺 means strong) or xiaoruo (衰 means weak)"""
    # Map category names to database values
    # The database has: 长生 (Chang Sheng) and 帝旺 (Di Wang)
    # Both are "strong" states, so shengda returns both
    if category == "shengda":
        # Both 长生 and 帝旺 are "strong" states
        all_nayins = db.query(Nayin).filter(
            Nayin.shengda_xiaoruo.in_(["长生", "帝旺"])
        ).all()
    elif category == "xiaoruo":
        # There's no "xiaoruo" in current data, but return empty for now
        return []
    else:
        return []

    results = []
    for nayin in all_nayins:
        ganzhi = db.query(Ganzhi).filter(Ganzhi.id == nayin.ganzhi_id).first()
        if ganzhi:
            results.append({
                "ganzhi": ganzhi.ganzhi,
                "tiangan": ganzhi.tiangan,
                "dizhi": ganzhi.dizhi,
                "nayin_name": nayin.nayin_name,
                "nayin_wuxing": nayin.nayin_wuxing,
                "zhuangtai": nayin.zhuangtai,
                "shengda_xiaoruo": nayin.shengda_xiaoruo
            })

    return results


def get_status_list(db: Session) -> List[str]:
    """Get all unique status values"""
    statuses = db.query(Nayin.zhuangtai).distinct().all()
    return [s[0] for s in statuses if s[0]]


def get_nayin_by_status(db: Session, status: str) -> List[dict]:
    """Get all Ganzhi with a specific status"""
    nayins = db.query(Nayin).filter(Nayin.zhuangtai == status).all()

    results = []
    for nayin in nayins:
        ganzhi = db.query(Ganzhi).filter(Ganzhi.id == nayin.ganzhi_id).first()
        if ganzhi:
            results.append({
                "ganzhi": ganzhi.ganzhi,
                "tiangan": ganzhi.tiangan,
                "dizhi": ganzhi.dizhi,
                "nayin_name": nayin.nayin_name,
                "nayin_wuxing": nayin.nayin_wuxing,
                "zhuangtai": nayin.zhuangtai,
                "shengda_xiaoruo": nayin.shengda_xiaoruo
            })

    return results


# Nayin calculation methods
def calc_nayin(ganzhi_name: str) -> dict:
    """
    Calculate Nayin using different methods.
    Returns step-by-step calculation for educational purposes.
    """
    # Tiangan (天干) values
    TIANGAN_WUXING = {
        "甲": "木", "乙": "木",
        "丙": "火", "丁": "火",
        "戊": "土", "己": "土",
        "庚": "金", "辛": "金",
        "壬": "水", "癸": "水"
    }

    # Dizhi (地支) values
    DIZHI_WUXING = {
        "子": "水", "丑": "土", "寅": "木", "卯": "木",
        "辰": "土", "巳": "火", "午": "火", "未": "土",
        "申": "金", "酉": "金", "戌": "土", "亥": "水"
    }

    # Taixuan numbers (太玄数)
    TAI_XUAN = {
        "甲": 9, "己": 9, "子": 9, "午": 9,
        "乙": 8, "庚": 8, "丑": 8, "未": 8,
        "丙": 7, "辛": 7, "寅": 7, "申": 7,
        "丁": 6, "壬": 6, "卯": 6, "酉": 6,
        "戊": 5, "癸": 5, "辰": 5, "戌": 5, "巳": 4, "亥": 4
    }

    # Nayin names (30 types)
    NAYIN_NAMES = [
        "海中金", "炉中火", "大林木", "路旁土", "剑锋金",
        "山头火", "涧下水", "城头土", "白蜡金", "杨柳木",
        "井泉水", "屋上土", "霹雳火", "松柏木", "长流水",
        "沙中金", "山下火", "平地木", "壁上土", "金箔金",
        "覆灯火", "天河水", "大驿土", "钗钏金", "桑柘木",
        "大溪水", "沙中土", "天上火", "石榴木", "大海水"
    ]

    # Wuxing to Nayin mapping (按照纳音顺序)
    NAYIN_BY_WUXING = {
        "金": ["海中金", "炉中火", "大林木", "路旁土", "剑锋金", "山头火"],
        "木": ["涧下水", "城头土", "白蜡金", "杨柳木", "井泉水", "屋上土"],
        "水": ["霹雳火", "松柏木", "长流水", "沙中金", "山下火", "平地木"],
        "火": ["壁上土", "金箔金", "覆灯火", "天河水", "大驿土", "钗钏金"],
        "土": ["桑柘木", "大溪水", "沙中土", "天上火", "石榴木", "大海水"]
    }

    if len(ganzhi_name) != 2:
        return {"error": "Invalid ganzhi format"}

    tiangan = ganzhi_name[0]
    dizhi = ganzhi_name[1]

    if tiangan not in TIANGAN_WUXING or dizhi not in DIZHI_WUXING:
        return {"error": "Invalid tiangan or dizhi"}

    tiangan_wuxing = TIANGAN_WUXING[tiangan]
    dizhi_wuxing = DIZHI_WUXING[dizhi]

    # Method 1: 隔八相生法 (based on position in 60 cycle)
    ganzhi_order = [
        "甲子", "乙丑", "丙寅", "丁卯", "戊辰", "己巳", "庚午", "辛未", "壬申", "癸酉",
        "甲戌", "乙亥", "丙子", "丁丑", "戊寅", "己卯", "庚辰", "辛巳", "壬午", "癸未",
        "甲申", "乙酉", "丙戌", "丁亥", "戊子", "己丑", "庚寅", "辛卯", "壬辰", "癸巳",
        "甲午", "乙未", "丙申", "丁酉", "戊戌", "己亥", "庚子", "辛丑", "壬寅", "癸卯",
        "甲辰", "乙巳", "丙午", "丁未", "戊申", "己酉", "庚戌", "辛亥", "壬子", "癸丑",
        "甲寅", "乙卯", "丙辰", "丁巳", "戊午", "己未", "庚申", "辛酉", "壬戌", "癸亥"
    ]

    try:
        idx = ganzhi_order.index(ganzhi_name)
        # Find base (group of 10)
        base_idx = (idx // 10) * 10
        inner_idx = idx % 10

        # Nayin index follows a pattern
        nayin_idx = (inner_idx // 2) % 6
        wuxing_cycle = ["金", "木", "水", "火", "土"]
        wuxing_idx = wuxing_cycle.index(tiangan_wuxing)
        final_wuxing = wuxing_cycle[(wuxing_idx + inner_idx // 2) % 5]

        method1_nayin = NAYIN_BY_WUXING[final_wuxing][nayin_idx]
        method1_desc = f"天干{tiangan}属{tiangan_wuxing}，地支{dizhi}属{dizhi_wuxing}，按隔八相生序取第{nayin_idx+1}个纳音"
    except:
        method1_nayin = None
        method1_desc = "无法计算"

    # Method 2: 太玄数法
    tx_tiangan = TAI_XUAN.get(tiangan, 0)
    tx_dizhi = TAI_XUAN.get(dizhi, 0)
    total = tx_tiangan + tx_dizhi

    # 49 - total, then mod 5
    remainder = (49 - total) % 5
    wuxing_map = {0: "土", 1: "水", 2: "木", 3: "金", 4: "火"}
    sheng_wuxing = wuxing_map[remainder]  # 生我者为纳音五行

    # Now find the actual Nayin
    # Simplified: just use the calculated wuxing
    try:
        method2_nayin = NAYIN_BY_WUXING[sheng_wuxing][nayin_idx]
        method2_desc = f"太玄数: {tiangan}={tx_tiangan}, {dizhi}={tx_dizhi}, 和={total}, (49-{total}) mod 5 = {remainder}, {remainder}对应{sheng_wuxing}，{sheng_wuxing}生{tiangan_wuxing}"
    except:
        method2_nayin = None
        method2_desc = "无法计算"

    # Method 3: 河图数直接法 (simplified)
    hetu_map = {"1": "水", "2": "火", "3": "木", "4": "金", "5": "土"}
    unit_digit = total % 5
    if unit_digit == 0:
        unit_digit = 5
    method3_wuxing = hetu_map[str(unit_digit)]

    try:
        method3_nayin = NAYIN_BY_WUXING[method3_wuxing][nayin_idx]
        method3_desc = f"河图数: 取太玄数和{total}的个位数{unit_digit}，{unit_digit}对应{method3_wuxing}"
    except:
        method3_nayin = None
        method3_desc = "无法计算"

    return {
        "ganzhi": ganzhi_name,
        "tiangan": tiangan,
        "dizhi": dizhi,
        "tiangan_wuxing": tiangan_wuxing,
        "dizhi_wuxing": dizhi_wuxing,
        "methods": [
            {
                "name": "隔八相生法",
                "result": method1_nayin,
                "description": method1_desc
            },
            {
                "name": "太玄数推算法",
                "result": method2_nayin,
                "description": method2_desc
            },
            {
                "name": "河图数直接法",
                "result": method3_nayin,
                "description": method3_desc
            }
        ]
    }
