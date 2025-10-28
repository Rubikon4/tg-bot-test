from sqlalchemy import Column, Integer, BigInteger, String
from Database.data import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    tg_id = Column(BigInteger, unique=True)
    username = Column(String(30), nullable=False)
    lucky_number = Column(Integer, nullable=False)

    def reg_log(self):
        return f"User(id={self.id}, tg_id={self.tg_id}, username='{self.username}', lucky_number={self.lucky_number})"