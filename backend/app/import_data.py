#!/usr/bin/env python3
"""
Data import script.
Imports data from xiangyi.json and KG_logic.json into the database.
"""
import sys
import os
import json

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal, init_db
from app.models import Ganzhi, Nayin, Xiangyi, Shensha, GanzhiShensha, Xiji, Guanxi


# Tian Gan (Heavenly Stems) mapping
TIAN_GAN = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸']
TIAN_GAN_WUXING = {
    '甲': '木', '乙': '木',
    '丙': '火', '丁': '火',
    '戊': '土', '己': '土',
    '庚': '金', '辛': '金',
    '壬': '水', '癸': '水'
}
TIAN_GAN_YINYANG = {
    '甲': '阳', '乙': '阴',
    '丙': '阳', '丁': '阴',
    '戊': '阳', '己': '阴',
    '庚': '阳', '辛': '阴',
    '壬': '阳', '癸': '阴'
}

# Di Zhi (Earthly Branches) mapping
DI_ZHI = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥']
DI_ZHI_WUXING = {
    '子': '水', '丑': '土', '寅': '木', '卯': '木',
    '辰': '土', '巳': '火', '午': '火', '未': '土',
    '申': '金', '酉': '金', '戌': '土', '亥': '水'
}
DI_ZHI_YINYANG = {
    '子': '阳', '丑': '阴', '寅': '阳', '卯': '阴',
    '辰': '阳', '巳': '阴', '午': '阳', '未': '阴',
    '申': '阳', '酉': '阴', '戌': '阳', '亥': '阴'
}
DI_ZHI_FANGWEI = {
    '子': '北', '丑': '东北', '寅': '东北', '卯': '东',
    '辰': '东南', '巳': '东南', '午': '南', '未': '西南',
    '申': '西南', '酉': '西', '戌': '西北', '亥': '西北'
}
DI_ZHI_JIJIE = {
    '子': '十一月', '丑': '十二月', '寅': '正月', '卯': '二月',
    '辰': '三月', '巳': '四月', '午': '五月', '未': '六月',
    '申': '七月', '酉': '八月', '戌': '九月', '亥': '十月'
}

# 60 Jiazi sequence
JIAZI_SEQUENCE = [
    ('甲', '子'), ('乙', '丑'), ('丙', '寅'), ('丁', '卯'), ('戊', '辰'),
    ('己', '巳'), ('庚', '午'), ('辛', '未'), ('壬', '申'), ('癸', '酉'),
    ('甲', '戌'), ('乙', '亥'), ('丙', '子'), ('丁', '丑'), ('戊', '寅'),
    ('己', '卯'), ('庚', '辰'), ('辛', '巳'), ('壬', '午'), ('癸', '未'),
    ('甲', '申'), ('乙', '酉'), ('丙', '戌'), ('丁', '亥'), ('戊', '子'),
    ('己', '丑'), ('庚', '寅'), ('辛', '卯'), ('壬', '辰'), ('癸', '巳'),
    ('甲', '午'), ('乙', '未'), ('丙', '申'), ('丁', '酉'), ('戊', '戌'),
    ('己', '亥'), ('庚', '子'), ('辛', '丑'), ('壬', '寅'), ('癸', '卯'),
    ('甲', '辰'), ('乙', '巳'), ('丙', '午'), ('丁', '未'), ('戊', '申'),
    ('己', '酉'), ('庚', '戌'), ('辛亥'), ('壬', '子'), ('癸', '丑'),
    ('甲', '寅'), ('乙', '卯'), ('丙', '辰'), ('丁', '巳'), ('戊', '午'),
    ('己', '未'), ('庚', '申'), ('辛', '酉'), ('壬', '戌'), ('癸', '亥')
]


def import_ganzhi(db):
    """Import 60 Ganzhi records."""
    print("Importing 60 Ganzhi records...")

    # Clear existing data
    db.query(Ganzhi).delete()

    ganzhi_list = []
    for tg, dz in JIAZI_SEQUENCE:
        ganzhi_name = tg + dz
        # Determine the wuxing of the ganzhi (based on tian gan)
        tg_wuxing = TIAN_GAN_WUXING.get(tg, '')
        dz_wuxing = DI_ZHI_WUXING.get(dz, '')

        # Get tian gan yuan shi ming
        tg_yuanshiming = ''
        if tg in SHI_TIAN_GAN_DATA:
            tg_yuanshiming = SHI_TIAN_GAN_DATA[tg].get('原始命名', '')

        # Get di zhi yuan shi ming
        dz_yuanshiming = ''
        if dz in SHI_ER_DI_ZHI_DATA:
            dz_yuanshiming = SHI_ER_DI_ZHI_DATA[dz].get('原始命名', '')

        g = Ganzhi(
            tiangan=tg,
            dizhi=dz,
            ganzhi=ganzhi_name,
            tiangan_wuxing=tg_wuxing,
            dizhi_wuxing=dz_wuxing,
            yinyang=TIAN_GAN_YINYANG.get(tg, ''),
            fangwei=DI_ZHI_FANGWEI.get(dz, ''),
            jijie=DI_ZHI_JIJIE.get(dz, ''),
            tiangan_yuanshiming=tg_yuanshiming,
            dizhi_yuanshiming=dz_yuanshiming
        )
        ganzhi_list.append(g)

    db.add_all(ganzhi_list)
    db.commit()
    print(f"  Imported {len(ganzhi_list)} ganzhi records")


def import_nayin(db):
    """Import Nayin data for 60 Ganzhi."""
    print("Importing Nayin data...")

    # Clear existing data
    db.query(Nayin).delete()

    # Get all ganzhi
    all_ganzhi = db.query(Ganzhi).all()
    ganzhi_map = {g.ganzhi: g for g in all_ganzhi}

    # Get xiangyi data - use the JSON keys directly
    liu_shi_jia_zi = XIANGYI_DATA.get('liu_shi_jia_zi_na_yin', {})

    nayin_list = []
    for json_key, data in liu_shi_jia_zi.items():
        # Convert json key to Chinese ganzhi
        ganzhi_name = convert_jiazi_key(json_key)
        if ganzhi_name in ganzhi_map:
            g = ganzhi_map[ganzhi_name]
            nayin_name = data.get('纳音', '')
            # Determine zhuangtai based on tian gan
            tg = g.tiangan
            zhuangtai_map = {
                '甲': '旺', '乙': '衰', '丙': '旺', '丁': '衰',
                '戊': '旺', '己': '衰', '庚': '旺', '辛': '衰',
                '壬': '旺', '癸': '衰'
            }
            zhuangtai = zhuangtai_map.get(tg, '平')

            # Determine shengda xiaoruo
            shengda_map = {
                '甲': '长生', '乙': '帝旺', '丙': '帝旺', '丁': '长生',
                '戊': '长生', '己': '帝旺', '庚': '帝旺', '辛': '长生',
                '壬': '帝旺', '癸': '长生'
            }
            shengda = shengda_map.get(tg, '')

            n = Nayin(
                ganzhi_id=g.id,
                nayin_name=nayin_name,
                nayin_wuxing=nayin_name[0] if nayin_name else '',
                zhuangtai=zhuangtai,
                shengda_xiaoruo=shengda,
                zhuangtai_desc=data.get('备注', '')
            )
            nayin_list.append(n)

    db.add_all(nayin_list)
    db.commit()
    print(f"  Imported {len(nayin_list)} nayin records")


def import_xiangyi(db):
    """Import Xiangyi data."""
    print("Importing Xiangyi data...")

    # Clear existing data
    db.query(Xiangyi).delete()

    # Get all ganzhi
    all_ganzhi = db.query(Ganzhi).all()
    ganzhi_map = {g.ganzhi: g for g in all_ganzhi}

    # Import tian gan xiangyi
    xiangyi_list = []
    for tg, data in SHI_TIAN_GAN_DATA.items():
        # Find the ganzhi that starts with this tian gan
        for g in all_ganzhi:
            if g.tiangan == tg:
                # Core xiangyi
                core_yixiang = data.get('核心象意', [])
                for content in core_yixiang:
                    x = Xiangyi(
                        ganzhi_id=g.id,
                        type='核心',
                        category='综合',
                        content=content,
                        description='',
                        source='原文',
                        confidence=1.0
                    )
                    xiangyi_list.append(x)

                # Detailed xiangyi
                detail = data.get('细分象意', {})
                for category, contents in detail.items():
                    for content in contents:
                        x = Xiangyi(
                            ganzhi_id=g.id,
                            type='细分',
                            category=category,
                            content=content,
                            description='',
                            source='原文',
                            confidence=1.0
                        )
                        xiangyi_list.append(x)
                break

    # Import di zhi xiangyi
    for dz, data in SHI_ER_DI_ZHI_DATA.items():
        for g in all_ganzhi:
            if g.dizhi == dz:
                core_yixiang = data.get('核心象意', [])
                for content in core_yixiang:
                    x = Xiangyi(
                        ganzhi_id=g.id,
                        type='核心',
                        category='综合',
                        content=content,
                        description='',
                        source='原文',
                        confidence=1.0
                    )
                    xiangyi_list.append(x)

                detail = data.get('细分象意', {})
                for category, contents in detail.items():
                    for content in contents:
                        x = Xiangyi(
                            ganzhi_id=g.id,
                            type='细分',
                            category=category,
                            content=content,
                            description='',
                            source='原文',
                            confidence=1.0
                        )
                        xiangyi_list.append(x)
                break

    # Import 60 jiazi xiangyi
    liu_shi_jia_zi = XIANGYI_DATA.get('liu_shi_jia_zi_na_yin', {})
    for json_key, data in liu_shi_jia_zi.items():
        ganzhi_name = convert_jiazi_key(json_key)
        if ganzhi_name in ganzhi_map:
            g = ganzhi_map[ganzhi_name]
            core_yixiang = data.get('核心象意', [])
            for content in core_yixiang:
                x = Xiangyi(
                    ganzhi_id=g.id,
                    type='核心',
                    category='综合',
                    content=content,
                    description=data.get('备注', ''),
                    source='原文',
                    confidence=1.0
                )
                xiangyi_list.append(x)

    db.add_all(xiangyi_list)
    db.commit()
    print(f"  Imported {len(xiangyi_list)} xiangyi records")


def import_shensha(db):
    """Import Shensha data and links to Ganzhi."""
    print("Importing Shensha data...")

    # Clear existing data
    db.query(GanzhiShensha).delete()
    db.query(Shensha).delete()

    # Get all ganzhi
    all_ganzhi = db.query(Ganzhi).all()
    ganzhi_map = {g.ganzhi: g for g in all_ganzhi}

    # Collect all shensha from the data
    shensha_set = set()
    liu_shi_jia_zi = XIANGYI_DATA.get('liu_shi_jia_zi_na_yin', {})
    for data in liu_shi_jia_zi.values():
        for s in data.get('神煞', []):
            shensha_set.add(s)

    # Add shensha from KG_logic.json if available
    if KG_DATA.get('knowledge_graph', {}).get('nodes'):
        for node in KG_DATA['knowledge_graph']['nodes']:
            if node.get('type') == '神煞':
                shensha_set.add(node.get('label'))

    # Create shensha records
    shensha_list = []
    for name in shensha_set:
        s = Shensha(
            name=name,
            type='组合神煞',
            check_method='',
            jixiong='平',
            yuanwen='',
            modern_desc='',
            remark=''
        )
        shensha_list.append(s)

    db.add_all(shensha_list)
    db.commit()

    # Create shensha map
    shensha_map = {s.name: s for s in db.query(Shensha).all()}

    # Link shensha to ganzhi
    gs_list = []
    for json_key, data in liu_shi_jia_zi.items():
        ganzhi_name = convert_jiazi_key(json_key)
        if ganzhi_name in ganzhi_map:
            g = ganzhi_map[ganzhi_name]
            for s_name in data.get('神煞', []):
                if s_name in shensha_map:
                    gs = GanzhiShensha(
                        ganzhi_id=g.id,
                        shensha_id=shensha_map[s_name].id,
                        is_zixing=False
                    )
                    gs_list.append(gs)

    db.add_all(gs_list)
    db.commit()
    print(f"  Imported {len(shensha_list)} shensha records and {len(gs_list)} links")


def import_xiji(db):
    """Import Xi (喜) and Ji (忌) data."""
    print("Importing Xiji (喜忌) data...")

    # Clear existing data
    db.query(Xiji).delete()

    # Get all ganzhi
    all_ganzhi = db.query(Ganzhi).all()
    ganzhi_map = {g.ganzhi: g for g in all_ganzhi}

    liu_shi_jia_zi = XIANGYI_DATA.get('liu_shi_jia_zi_na_yin', {})

    xiji_list = []
    for json_key, data in liu_shi_jia_zi.items():
        ganzhi_name = convert_jiazi_key(json_key)
        if ganzhi_name in ganzhi_map:
            g = ganzhi_map[ganzhi_name]

            # 喜
            for target in data.get('喜', []):
                x = Xiji(
                    ganzhi_id=g.id,
                    type='喜',
                    target_type='五行/方位',
                    target_value=target,
                    remark=''
                )
                xiji_list.append(x)

            # 忌
            for target in data.get('忌', []):
                x = Xiji(
                    ganzhi_id=g.id,
                    type='忌',
                    target_type='五行/方位',
                    target_value=target,
                    remark=''
                )
                xiji_list.append(x)

    db.add_all(xiji_list)
    db.commit()
    print(f"  Imported {len(xiji_list)} xiji records")


def import_guanxi(db):
    """Import Guanxi (relationships) data."""
    print("Importing Guanxi data...")

    # Clear existing data
    db.query(Guanxi).delete()

    # Get all ganzhi
    all_ganzhi = db.query(Ganzhi).all()
    ganzhi_set = {g.ganzhi for g in all_ganzhi}

    # Process edges from KG_logic.json
    guanxi_list = []
    edges = KG_DATA.get('knowledge_graph', {}).get('edges', [])

    for edge in edges:
        from_node = edge.get('from', '')
        to_node = edge.get('to', '')
        relation = edge.get('relation', '')
        note = edge.get('note', '')

        # Convert node IDs to ganzhi names
        # e.g., "jia_zi" -> "甲子", "yi_chou" -> "乙丑"
        g1 = convert_jiazi_key(from_node)
        g2 = convert_jiazi_key(to_node)

        if g1 and g2 and g1 in ganzhi_set and g2 in ganzhi_set:
            # Skip if duplicate
            exists = db.query(Guanxi).filter(
                Guanxi.ganzhi1 == g1,
                Guanxi.ganzhi2 == g2,
                Guanxi.relation_type == relation
            ).first()

            if not exists:
                g = Guanxi(
                    ganzhi1=g1,
                    ganzhi2=g2,
                    relation_type=relation,
                    remark=note
                )
                guanxi_list.append(g)

    # Add some basic relationships based on the 60 jiazi sequence
    # Same tian gan (同天干)
    tg_ganzhi = {}
    for g in all_ganzhi:
        if g.tiangan not in tg_ganzhi:
            tg_ganzhi[g.tiangan] = []
        tg_ganzhi[g.tiangan].append(g.ganzhi)

    for tg, g_list in tg_ganzhi.items():
        for i in range(len(g_list)):
            for j in range(i+1, len(g_list)):
                # Check if not already exists
                exists = db.query(Guanxi).filter(
                    Guanxi.ganzhi1 == g_list[i],
                    Guanxi.ganzhi2 == g_list[j],
                    Guanxi.relation_type == '同天干'
                ).first()
                if not exists:
                    g = Guanxi(
                        ganzhi1=g_list[i],
                        ganzhi2=g_list[j],
                        relation_type='同天干',
                        remark=''
                    )
                    guanxi_list.append(g)

    # Same di zhi (同地支)
    dz_ganzhi = {}
    for g in all_ganzhi:
        if g.dizhi not in dz_ganzhi:
            dz_ganzhi[g.dizhi] = []
        dz_ganzhi[g.dizhi].append(g.ganzhi)

    for dz, g_list in dz_ganzhi.items():
        for i in range(len(g_list)):
            for j in range(i+1, len(g_list)):
                exists = db.query(Guanxi).filter(
                    Guanxi.ganzhi1 == g_list[i],
                    Guanxi.ganzhi2 == g_list[j],
                    Guanxi.relation_type == '同地支'
                ).first()
                if not exists:
                    g = Guanxi(
                        ganzhi1=g_list[i],
                        ganzhi2=g_list[j],
                        relation_type='同地支',
                        remark=''
                    )
                    guanxi_list.append(g)

    db.add_all(guanxi_list)
    db.commit()
    print(f"  Imported {len(guanxi_list)} guanxi records")


def convert_jiazi_key(key):
    """Convert jiazi key from JSON format to Chinese ganzhi."""
    mapping = {
        'jia_zi': '甲子', 'yi_chou': '乙丑', 'bing_yin': '丙寅', 'ding_mao': '丁卯',
        'wu_chen': '戊辰', 'ji_si': '己巳', 'geng_wu': '庚午', 'xin_wei': '辛未',
        'ren_shen': '壬申', 'gui_you': '癸酉', 'jia_xu': '甲戌', 'yi_hai': '乙亥',
        'bing_zi': '丙子', 'ding_chou': '丁丑', 'wu_yin': '戊寅', 'ji_mao': '己卯',
        'geng_chen': '庚辰', 'xin_si': '辛巳', 'ren_wu': '壬午', 'gui_wei': '癸未',
        'jia_shen': '甲申', 'yi_you': '乙酉', 'bing_xu': '丙戌', 'ding_hai': '丁亥',
        'wu_zi': '戊子', 'ji_chou': '己丑', 'geng_yin': '庚寅', 'xin_mao': '辛卯',
        'ren_chen': '壬辰', 'gui_si': '癸巳', 'jia_wu': '甲午', 'yi_wei': '乙未',
        'bing_shen': '丙申', 'ding_you': '丁酉', 'wu_xu': '戊戌', 'ji_hai': '己亥',
        'geng_zi': '庚子', 'xin_chou': '辛丑', 'ren_yin': '壬寅', 'gui_mao': '癸卯',
        'jia_chen': '甲辰', 'yi_si': '乙巳', 'bing_wu': '丙午', 'ding_wei': '丁未',
        'wu_shen': '戊申', 'ji_you': '己酉', 'geng_xu': '庚戌', 'xin_hai': '辛亥',
        'ren_zi': '壬子', 'gui_chou': '癸丑', 'jia_yin': '甲寅', 'yi_mao': '乙卯',
        'bing_chen': '丙辰', 'ding_si': '丁巳', 'wu_wu': '戊午', 'ji_wei': '己未',
        'geng_shen': '庚申', 'xin_you': '辛酉', 'ren_xu': '壬戌', 'gui_hai': '癸亥'
    }
    return mapping.get(key, key)


def main():
    """Main import function."""
    global SHI_TIAN_GAN_DATA, SHI_ER_DI_ZHI_DATA, XIANGYI_DATA, KG_DATA

    print("=" * 50)
    print("Data Import Script")
    print("=" * 50)

    # Load data files
    print("\nLoading data files...")

    # Get project root (go up 3 levels from app/import_data.py to reach project root)
    # app/import_data.py -> app/ -> backend/ -> project root
    current_file = os.path.abspath(__file__)
    app_dir = os.path.dirname(current_file)
    backend_dir = os.path.dirname(app_dir)
    project_root = os.path.dirname(backend_dir)
    xiangyi_path = os.path.join(project_root, 'xiangyi.json')
    kg_path = os.path.join(project_root, 'KG_logic.json')

    with open(xiangyi_path, 'r', encoding='utf-8') as f:
        XIANGYI_DATA = json.load(f)

    with open(kg_path, 'r', encoding='utf-8') as f:
        KG_DATA = json.load(f)

    SHI_TIAN_GAN_DATA = XIANGYI_DATA.get('shi_tian_gan', {})
    SHI_ER_DI_ZHI_DATA = XIANGYI_DATA.get('shi_er_di_zhi', {})

    print(f"  Loaded xiangyi.json with {len(SHI_TIAN_GAN_DATA)} tian gan, {len(SHI_ER_DI_ZHI_DATA)} di zhi")
    print(f"  Loaded KG_logic.json with {len(KG_DATA.get('knowledge_graph', {}).get('nodes', []))} nodes")

    # Initialize database
    print("\nInitializing database...")
    init_db()

    # Create database session
    db = SessionLocal()

    try:
        # Import data
        import_ganzhi(db)
        import_nayin(db)
        import_xiangyi(db)
        import_shensha(db)
        import_xiji(db)
        import_guanxi(db)

        print("\n" + "=" * 50)
        print("Data import completed!")
        print("=" * 50)

        # Print summary
        print("\nSummary:")
        print(f"  Ganzhi: {db.query(Ganzhi).count()} records")
        print(f"  Nayin: {db.query(Nayin).count()} records")
        print(f"  Xiangyi: {db.query(Xiangyi).count()} records")
        print(f"  Shensha: {db.query(Shensha).count()} records")
        print(f"  GanzhiShensha: {db.query(GanzhiShensha).count()} records")
        print(f"  Xiji: {db.query(Xiji).count()} records")
        print(f"  Guanxi: {db.query(Guanxi).count()} records")

    except Exception as e:
        print(f"\nError: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()
