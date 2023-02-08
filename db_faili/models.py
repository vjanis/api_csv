
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date, Float, Boolean, JSON, ForeignKey, DateTime, Index
from sqlalchemy.orm import relationship

import datetime

Base = declarative_base()


# class Book(Base):
#     __tablename__ = 'sadale'
#     id = Column(Integer, primary_key=True)
#     tips = Column(String)
#     atvk = Column(String)
#     nosaukums = Column(String)
#     gads = Column(String)
#     periods = Column(String)
#     datums = Column(String)
#     sadalits = Column(Float)
#     pfif = Column(Float)
#
# #    pages = Column(Integer)
# #    published = Column(Date)
#
#     def __repr__(self):
#         return "<Book(tips='{}', atvk='{}', nosaukums={}, gads={}, periods={}, datums={}, sadalits={}, pfif={})>" \
#             .format(self.tips, self.atvk, self.nosaukums, self.gads,
#                     self.periods, self.datums, self.sadalits, self.pfif)

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
    id = Column(Integer, primary_key=True)
    laiks = Column(DateTime, default=datetime.datetime.utcnow)
    darbiba = Column(String)
    parametri = Column(String)
    json_text = Column(JSONB)
    autorizacijas_lvl = Column(String)
    statuss = Column(String)

    def __repr__(self):
        return "<Auditacija(id='{}', laiks='{}', darbiba={}, parametri={}, json_text={}, " \
               "autorizacijas_lvl={}, statuss={})>" \
            .format(self.id, self.laiks, self.darbiba, self.parametri, self.json_text,
                    self.autorizacijas_lvl, self.statuss)


class Kofiguracija(Base):
    __tablename__ = 'kofiguracija'
    id = Column(Integer, primary_key=True)
    api = Column(String)
    kumulativs = Column(Boolean, unique=False, default=False)
    atdalitajs = Column(String)
    dati = Column(String)
    json_text = Column(JSONB)

    def __repr__(self):
        return "<Konfiguracija(id='{}', api='{}', kumulativs={}, atdalitajs={}, dati={}, json_text={})>" \
            .format(self.id, self.api, self.kumulativs, self.atdalitajs, self.dati, self.json_text)

class Metrikas(Base):
    __tablename__ = 'metrikas'
    id = Column(Integer, primary_key=True)
    metrika = Column(String)
    vertiba = Column(String)
    seciba = Column(Integer)
    statuss = Column(Boolean, unique=False, default=True)

    def __repr__(self):
        return "<kofiguracija(id='{}', metrika='{}', vertiba={}, seciba={}, statuss={})>" \
            .format(self.id, self.metrika, self.vertiba, self.seciba, self.statuss)
