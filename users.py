import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import random

DB_PATH = "sqlite:///sochi_athletes.sqlite3"
Base = declarative_base()

class User(Base):
    """
    Описывает структуру таблицы user для хранения регистрационных данных пользователей
    """
    # задаем название таблицы
    __tablename__ = 'user'
    # идентификатор пользователя, первичный ключ
    id = sa.Column(sa.INTEGER, primary_key=True)
    # имя пользователя
    first_name = sa.Column(sa.TEXT)
    # фамилия пользователя
    last_name = sa.Column(sa.TEXT)
    # пол атлета
    gender = sa.Column(sa.TEXT)
    # адрес электронной почты поль
    email = sa.Column(sa.TEXT)
     # возраст атлета
    birthdate = sa.Column(sa.TEXT)
    # рост атлета
    height = sa.Column(sa.REAL)

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

def request_data():
    """
    Запрашивает у пользователя данные и добавляет их в список users
    """
    # выводим приветствие
    print("Привет! Я запишу твои данные!")
    # запрашиваем у пользователя данные
    first_name = input("Введи своё имя: ")
    last_name = input("А теперь фамилию: ")
    gender = input("Твой пол (М/Ж): ")
    email = input("Мне еще понадобится адрес твоей электронной почты: ")
    birthdate = input("Дата твоего рождения (дд-мм-гггг): ")
    height = input("Также нужен твой рост (м.см): ")
    # генерируем идентификатор пользователя
    user_id = add_id()
    # создаем нового пользователя
    user = User(
        id=user_id,
        first_name=first_name,
        last_name=last_name,
        gender = gender,
        email=email,
        birthdate = birthdate,
        height = height
    )
    # возвращаем созданного пользователя
    return user

def add_id():
    """
     Генерируем идентификатор пользователя и проверяем на повторение
     """
    id = random.randint(0, 1000000)
    session = connect_db()
    while session.query(User).filter(User.id == id).first():
        id = random.randint(0, 1000000)
    return id

def main():
    """
    Осуществляет взаимодействие с пользователем, обрабатывает пользовательский ввод
    """
    session = connect_db()
    # запрашиваем данные пользоватлея
    user = request_data()
    # добавляем нового пользователя в сессию
    session.add(user)
    # сохраняем все изменения, накопленные в сессии
    session.commit()
    print("Спасибо, данные сохранены!")

if __name__ == '__main__':
    main()