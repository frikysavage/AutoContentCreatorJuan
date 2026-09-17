import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Account(Base):
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    categoria_default = Column(String)
    idioma_default = Column(String)
    duracion_default = Column(Integer)
    formato_default = Column(String)

    character_sheets = relationship("CharacterSheet", back_populates="account")
    video_jobs = relationship("VideoJob", back_populates="account")
    video_history = relationship("VideoHistory", back_populates="account")

class CharacterSheet(Base):
    __tablename__ = "character_sheets"

    id = Column(Integer, primary_key=True, index=True)
    account_id = Column(Integer, ForeignKey("accounts.id"))
    estilo = Column(String)
    rasgos_fijos = Column(String)
    paleta = Column(String)
    vestuario_base = Column(String)
    creado_en = Column(DateTime, default=datetime.datetime.utcnow)

    account = relationship("Account", back_populates="character_sheets")

class VideoJob(Base):
    __tablename__ = "video_jobs"

    id = Column(Integer, primary_key=True, index=True)
    account_id = Column(Integer, ForeignKey("accounts.id"))
    tema = Column(String)
    guion = Column(String)
    titulo_seo = Column(String)
    resumen_para_historial = Column(String)
    duracion_segundos = Column(Integer)
    musica = Column(String)
    subtitulos = Column(Boolean, default=True)
    synthetic_content = Column(Boolean, default=True)
    video_id_youtube = Column(String, nullable=True)
    review_token = Column(String, unique=True, index=True, nullable=True)
    estado = Column(String, default="pendiente")
    creado_en = Column(DateTime, default=datetime.datetime.utcnow)

    account = relationship("Account", back_populates="video_jobs")

class VideoHistory(Base):
    __tablename__ = "video_history"

    id = Column(Integer, primary_key=True, index=True)
    account_id = Column(Integer, ForeignKey("accounts.id"))
    resumen_para_historial = Column(String)
    creado_en = Column(DateTime, default=datetime.datetime.utcnow)

    account = relationship("Account", back_populates="video_history")
