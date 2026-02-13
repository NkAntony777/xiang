from sqlalchemy import Column, Integer, String, Text, Float, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class Ganzhi(Base):
    """干支表"""
    __tablename__ = "ganzhi"

    id = Column(Integer, primary_key=True, index=True)
    tiangan = Column(String(2), nullable=False)
    dizhi = Column(String(2), nullable=False)
    ganzhi = Column(String(4), unique=True, nullable=False, index=True)
    tiangan_wuxing = Column(String(2))
    dizhi_wuxing = Column(String(2))
    yinyang = Column(String(2))
    fangwei = Column(String(4))
    jijie = Column(String(4))
    tiangan_yuanshiming = Column(String(8))
    dizhi_yuanshiming = Column(String(8))
    special_desc = Column(Text)

    # Relationships
    nayin = relationship("Nayin", back_populates="ganzhi", uselist=False)
    xiangyi_list = relationship("Xiangyi", back_populates="ganzhi")
    xiji_list = relationship("Xiji", back_populates="ganzhi")
    shensha_list = relationship("GanzhiShensha", back_populates="ganzhi")


class Nayin(Base):
    """纳音表"""
    __tablename__ = "nayin"

    id = Column(Integer, primary_key=True, index=True)
    ganzhi_id = Column(Integer, ForeignKey("ganzhi.id"), unique=True)
    nayin_name = Column(String(20))
    nayin_wuxing = Column(String(2))
    zhuangtai = Column(String(4))
    shengda_xiaoruo = Column(String(4))
    zhuangtai_desc = Column(Text)

    # Relationships
    ganzhi = relationship("Ganzhi", back_populates="nayin")


class Xiangyi(Base):
    """象意表"""
    __tablename__ = "xiangyi"

    id = Column(Integer, primary_key=True, index=True)
    ganzhi_id = Column(Integer, ForeignKey("ganzhi.id"))
    type = Column(String(10))  # 核心、细分、组合
    category = Column(String(20))  # 天文气象、地理建筑、人物伦常、性情、身体、事物、植物、器物
    content = Column(String(100))
    description = Column(Text)
    source = Column(String(10))  # 原文/推理
    confidence = Column(Float)

    # Relationships
    ganzhi = relationship("Ganzhi", back_populates="xiangyi_list")


class Shensha(Base):
    """神煞表"""
    __tablename__ = "shensha"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(30), unique=True, index=True)
    type = Column(String(10))  # 字形神煞/组合神煞
    check_method = Column(Text)
    jixiong = Column(String(4))  # 吉/凶/平
    yuanwen = Column(Text)
    modern_desc = Column(Text)
    remark = Column(Text)

    # Relationships
    ganzhi_list = relationship("GanzhiShensha", back_populates="shensha")


class GanzhiShensha(Base):
    """干支-神煞关联表"""
    __tablename__ = "ganzhi_shensha"

    id = Column(Integer, primary_key=True, index=True)
    ganzhi_id = Column(Integer, ForeignKey("ganzhi.id"))
    shensha_id = Column(Integer, ForeignKey("shensha.id"))
    is_zixing = Column(Boolean, default=False)

    # Relationships
    ganzhi = relationship("Ganzhi", back_populates="shensha_list")
    shensha = relationship("Shensha", back_populates="ganzhi_list")


class Xiji(Base):
    """喜忌表"""
    __tablename__ = "xiji"

    id = Column(Integer, primary_key=True, index=True)
    ganzhi_id = Column(Integer, ForeignKey("ganzhi.id"))
    type = Column(String(4))  # 喜/忌
    target_type = Column(String(10))  # 五行、季节、地支
    target_value = Column(String(20))
    remark = Column(Text)

    # Relationships
    ganzhi = relationship("Ganzhi", back_populates="xiji_list")


class Guanxi(Base):
    """干支关系表"""
    __tablename__ = "guanxi"

    id = Column(Integer, primary_key=True, index=True)
    ganzhi1 = Column(String(4), index=True)
    ganzhi2 = Column(String(4), index=True)
    relation_type = Column(String(20), index=True)  # 六合、三合、半合、六冲、六害、三刑、自刑、同位、隔八生子
    remark = Column(Text)
