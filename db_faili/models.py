
from sqlalchemy.dialects.postgresql import JSONB
#from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date, Float, Boolean, JSON, ForeignKey, DateTime, Index, Sequence
from sqlalchemy.orm import relationship
from sqlalchemy.orm import DeclarativeBase

import datetime

class Base(DeclarativeBase):
     pass


class Csv_faili(Base):
    __tablename__ = 'csv_faili'
    id = Column(Integer, primary_key=True)
    api = Column(String)
    csv_file_name = Column(String)
    created = Column(DateTime, default=datetime.datetime.utcnow)
    is_active = Column(Boolean, unique=False, default=True)

    def __repr__(self):
        return "<Csv_faili(id='{}', api='{}', csv_file_name={}, created={}, is_active={})>" \
            .format(self.id, self.api, self.csv_file_name, self.created, self.is_active)

class Csv_faili_json(Base):
    __tablename__ = 'csv_faili_json'
    id = Column(Integer, primary_key=True)
    json_text = Column(JSONB)
    csv_faili_id = Column(Integer, ForeignKey("csv_faili.id"), index=True)

    csv_faili = relationship("Csv_faili", back_populates="csv_faili_json")

    def __repr__(self):
        return "<Csv_faili_json(id='{}', json_text={})>" \
            .format(self.id, self.json_text)

    Csv_faili.csv_faili_json = relationship("Csv_faili_json", order_by=Csv_faili.id, back_populates="csv_faili")

class Auditacija(Base):
    __tablename__ = 'auditacija'
    id = Column(Integer, Sequence('auditacija_id_seq'), primary_key=True)
    laiks = Column(DateTime, default=datetime.datetime.utcnow)
    darbiba = Column(String)
    parametri = Column(String)
    json_text = Column(JSONB)
    autorizacijas_lvl = Column(String)
    statuss = Column(String)
    metrika = Column(Integer)

    def __repr__(self):
        return "<Auditacija(id='{}', laiks='{}', darbiba={}, parametri={}, json_text={}, " \
               "autorizacijas_lvl={}, statuss={}, metrika={})>" \
            .format(self.id, self.laiks, self.darbiba, self.parametri, self.json_text,
                    self.autorizacijas_lvl, self.statuss, self.metrika)


class Kofiguracija(Base):
    __tablename__ = 'kofiguracija'
    id = Column(Integer, primary_key=True)
    api = Column(String)
    kumulativs = Column(Boolean, unique=False, default=False)
    atdalitajs = Column(String)
    dati = Column(String)
    json_text = Column(JSONB)
    statuss = Column(Boolean, unique=False, default=True)

    def __repr__(self):
        return "<Konfiguracija(id='{}', api='{}', kumulativs={}, atdalitajs={}, dati={}, json_text={}, statuss={})>" \
            .format(self.id, self.api, self.kumulativs, self.atdalitajs, self.dati, self.json_text, self.statuss)

class Metrikas(Base):
    __tablename__ = 'metrikas'
    id = Column(Integer, Sequence('metrikas_id_seq'), primary_key=True)
    metrika = Column(Integer, unique=True)
    vertiba = Column(Integer, default=0)
    param = Column(String)
    apraksts = Column(String)
    seciba = Column(Integer)
    statuss = Column(Boolean, unique=False, default=True)

    def __repr__(self):
        return "<kofiguracija(id='{}', metrika='{}', vertiba={}, param={}, apraksts={}, seciba={}, statuss={})>" \
            .format(self.id, self.metrika, self.vertiba, self.param, self.apraksts, self.seciba, self.statuss)
