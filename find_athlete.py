import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import datetime
from datetime import datetime
from users import User

DB_PATH = "sqlite:///sochi_athletes.sqlite3"
Base = declarative_base()

def connect_db():
    """
    Устанавливает соединение к базе данных, создает таблицы, если их еще нет и возвращает объект сессии 
    """
    # создаем соединение к базе данных
    engine = sa.create_engine(DB_PATH)
    # создаем описанные таблицы
    Base.metadata.create_all(engine)
    # создаем фабрику сессию
    session = sessionmaker(engine)
    # возвращаем сессию
    return session()

class Athelete(Base):
    """
    Описывает структуру таблицы athelete для хранения регистрационных данных пользователей
    """
    # задаем название таблицы
    __tablename__ = 'athelete'
    # идентификатор пользователя, первичный ключ
    id = sa.Column(sa.String(36), primary_key=True)
    # возраст атлета
    age = sa.Column(sa.INTEGER)
    # дата рождения атлета
    birthdate = sa.Column(sa.TEXT)
    # пол атлета
    gender = sa.Column(sa.TEXT)
    # рост атлета
    height = sa.Column(sa.REAL)
    # имя атлета
    name = sa.Column(sa.TEXT)
    # вес атлета
    weight = sa.Column(sa.INTEGER)
    # количество золотых медалей
    gold_medals = sa.Column(sa.INTEGER)
    # количество серебряных медалей
    silver_medals = sa.Column(sa.INTEGER)
    # количество бронзовых медалей
    bronze_medals = sa.Column(sa.INTEGER)
    # количество медалей всех достоинств
    total_medals = sa.Column(sa.INTEGER)
    # вид спорта
    sport = sa.Column(sa.TEXT)
    # страна проживания
    country = sa.Column(sa.TEXT)

def check_id():
    # Проверка на существование пользователя
    str_id = input("Введиите идентификатор пользователя (уже в табл. '331102', '696529', '801466'): ")
    int_id = int(str_id)
    session = connect_db()
    user = session.query(User).filter(User.id == int_id).first()
    if user:
        print('Пользователь найден!')
    else:
        print('Такого пользователя не существует.')
    return user

def compare_height(user):
    session = connect_db() 
    if user:
        heigth_dif = -1.0
        for athelete in session.query(Athelete).all():
            if athelete.height:
                current_difference = abs(athelete.height - user.height)
                if heigth_dif < 0:
                    heigth_dif = current_difference
                    nearest_athlete = athelete
                if heigth_dif > current_difference:
                    heigth_dif = current_difference
                    nearest_athlete = athelete
        return nearest_athlete
        

def compare_birthdate(user):
    session = connect_db()
    date_difference = None
    if user:
        for athelete in session.query(Athelete).all():
            if athelete.birthdate:
                birth_ath = datetime.strptime(athelete.birthdate, "%Y-%m-%d")
                birth_user = datetime.strptime(user.birthdate, "%d-%m-%Y")
                if date_difference:
                    if date_difference > abs(datetime.date(birth_ath) - datetime.date(birth_user)):
                        date_difference = abs(datetime.date(birth_ath) - datetime.date(birth_user))
                        nearest_athelete = athelete
                else:
                    date_difference = abs(datetime.date(birth_ath) - datetime.date(birth_user)) 
                    nearest_athelete = athelete
        return nearest_athelete

def main():
    user = check_id()
    if user:
        height_ath = compare_height(user)
        birthdate_ath = compare_birthdate(user)
        print("Близжайший по росту атлет: {name}, его/ее рост равен: {height}".format(name = height_ath.name, height = height_ath.height))
        print("Близжайший по дате рождения атлет: {name}, он/а родился/ась: {birthdate}".format(name = birthdate_ath.name, birthdate = birthdate_ath.birthdate))

if __name__ == '__main__':
    main()
