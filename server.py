from hashlib import sha256
from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

engine = create_engine("sqlite:///banco_server.db")
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()
NUMBER_OF_TOKENS = 5

class User(Base):
    __tablename__ = "Users"
    name = Column(String, primary_key=True)
    seed = Column(String, nullable=False)
    time_last_token = Column(String)
    index_last_token = Column(Integer, default = NUMBER_OF_TOKENS)

def add_user(name, seed_hash, salt_hash):
    new_user = User(name=name, seed = seed_hash + salt_hash)
    session.add(new_user)
    try:
        session.commit()
        print("Usuário criado com sucesso! Favor fazer login. ")

    except Exception as e:
        session.rollback()
        print("Erro: O usuário com essa seed já está registrado. Por favor, escolha outra semente.")

def user_registered(name):
    return session.get(User, name) is not None

def hash_to_6_digits_int(string):
    hashed_string = sha256(string.encode()).hexdigest()
    hash_int = int(hashed_string, 16)
    hash_6_digits = hash_int % 900000 + 100000
    return hashed_string, hash_6_digits

def generate_tokens(name):
    token_list = []
    user = session.get(User, name)
    date_now = datetime.now().strftime("%Y%m%d%H%M")
    string_to_hash = user.seed + date_now
    for _ in range(NUMBER_OF_TOKENS):
        hashed_string, hash_6_digits = hash_to_6_digits_int(string_to_hash)
        token_list.append(hash_6_digits)
        string_to_hash = hashed_string

    if user.time_last_token != date_now:
        update_user_time_last_token(name, date_now)
        token_index = NUMBER_OF_TOKENS

    else:
        token_index = user.index_last_token
    
    return token_list[:token_index]  

def update_user_time_last_token(name, time):
    user = session.get(User, name)
    if user:
        user.time_last_token = time
        session.commit()

def update_user_index_last_token(name, index):
    user = session.get(User, name)
    if user:
        user.index_last_token = index
        session.commit()

def main():
    Base.metadata.create_all(engine)
    salt = sha256()
    salt.update(b"Juro que isso eh aleatorio e um salt totalmente valido")

    while(True):
        user_name = input("Qual o nome de usuário? ")
        if user_registered(user_name):
            token = int(input("Seja bem vindo de volta! Qual seu token numérico de 6 dígitos? "))
            token_list = generate_tokens(user_name)
            print("DEBUG: Os tokens válidos são:", ', '.join(str(num) for num in token_list))

            if token not in token_list:
                print("Token inválido. Tente novamente.")
            
            else:
                print("Token válido. Login feito com sucesso.")
                update_user_index_last_token(user_name, token_list.index(token))
                
        else:
            seed = sha256()
            seed.update(input("Qual a senha semente para a criação da conta? ").encode())
            add_user(user_name, seed.hexdigest(), salt.hexdigest())

if __name__ == '__main__':
    main()