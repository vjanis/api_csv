from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date, Float

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


