from hashlib import sha256
from sqlalchemy import create_engine, Column, String
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

engine = create_engine("sqlite:///banco_client.db")
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()
NUMBER_OF_TOKENS = 5

class User(Base):
    __tablename__ = "Users"
    name = Column(String, primary_key=True)
    local_password = Column(String)
    seed = Column(String, nullable=False)

def add_user(name, local_password_hash, seed_hash, salt_hash):
    new_user = User(name=name, local_password = local_password_hash, seed = seed_hash + salt_hash)
    session.add(new_user)
    try:
        session.commit()
        print("Usuário criado com sucesso! Favor fazer login. ")

    except Exception as e:
        session.rollback()
        print("Erro: O usuário com essa seed já está registrado. Por favor, escolha outra semente.")


def is_password_correct(name, local_password_hash):
    user = session.get(User, name)
    if user.local_password == local_password_hash:
        return True
    
    return False

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

    return token_list

def main():
    Base.metadata.create_all(engine)
    salt = sha256()
    salt.update(b"Juro que isso eh aleatorio e um salt totalmente valido")

    while(True):
        user_name = input("Qual o nome de usuário? ")
        if user_registered(user_name):
            local_password = sha256()
            local_password.update(input("Seja bem vindo de volta! Qual sua senha local? ").encode())
            if is_password_correct(user_name, local_password.hexdigest()):
                more_tokens = "1"

                while(more_tokens == "1"):
                    token_list = generate_tokens(user_name)
                    print("Seus tokens são:", ', '.join(str(num) for num in token_list))
                    input("Digite '1' se desejar mais tokens: ")
                
        else:
            seed = sha256()
            seed.update(input("Qual a senha semente para a criação da conta? ").encode())
            
            local_password = sha256()
            local_password.update(input("Qual a senha local para acesso ao app? ").encode())
            add_user(user_name, local_password.hexdigest(), seed.hexdigest(), salt.hexdigest())

if __name__ == '__main__':
    main()