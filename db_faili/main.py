from datetime import datetime

from crud import *
from models import *

if __name__ == '__main__':
    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    s = Session()
    book = Book(

        tips='iin',
        atvk='0001000',
        nosaukums='Rīga',
        gads='2022',
        periods='01',
        sadalits=2.1,
        pfif=2.0
    )
    s.add(book)
    s.commit()
    s.close()
