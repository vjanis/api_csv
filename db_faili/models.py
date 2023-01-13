
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date, Float, Boolean, JSON

Base = declarative_base()


class Book(Base):
    __tablename__ = 'sadale'
    id = Column(Integer, primary_key=True)
    tips = Column(String)
    atvk = Column(String)
    nosaukums = Column(String)
    gads = Column(String)
    periods = Column(String)
    datums = Column(String)
    sadalits = Column(Float)
    pfif = Column(Float)

#    pages = Column(Integer)
#    published = Column(Date)

    def __repr__(self):
        return "<Book(tips='{}', atvk='{}', nosaukums={}, gads={}, periods={}, datums={}, sadalits={}, pfif={})>" \
            .format(self.tips, self.atvk, self.nosaukums, self.gads,
                    self.periods, self.datums, self.sadalits, self.pfif)


class Csv_faili(Base):
    __tablename__ = 'csv_faili'
    id = Column(Integer, primary_key=True)
    csv_file_name = Column(String)
    atvk = Column(String)
    gads = Column(String)
    datums = Column(String)
    json_text = Column(JSONB)
    created = Column(Date)
    is_active = Column(Boolean, unique=False, default=True)

    def __repr__(self):
        return "<Csv_faili(id='{}', csv_file_name='{}', atvk={}, gads={}, " \
               "datums={}, json_text={}, created={}, is_active={})>" \
            .format(self.id, self.csv_file_name, self.atvk, self.gads,
                    self.datums, self.json_text, self.created, self.is_active)
