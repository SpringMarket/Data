from faker import Faker
import bcrypt
import random
import pandas as pd
import config

from sqlalchemy import create_engine
import sqlalchemy as db

fake = Faker('ko_KR') # locale 정보 설정
Faker.seed() # 초기 seed 설정
num = 1000000

# 유저 id
userId = [i for i in range(1, num+1)]

# 이메일
email = [fake.free_email() for i in range(0, num)]

# 비밀번호
# words = [fake.word() for i in range(num)]
# hashedPassword = [bcrypt.hashpw(i.encode('utf-8'), bcrypt.gensalt(rounds=10, prefix=b"2a")) for i in words]
# print(hashedPassword)

# 연령대
age = [random.choice(['10대','20대','30대','40대 이상']) for i in range(num)]

# 관리자
authority = ["ROLE_USER"] * num

created_at = [fake.date_time_between(start_date = '-4y', end_date ='now') for i in range(num)]

df = pd.DataFrame()
df['user_id'] = userId
df['email'] = email
df['password'] = userId
df['age'] = age
df['authority'] = authority

records = df.to_dict(orient='records')


port = config.port
username = config.username
password = config.password
host = config.host
dbname = config.dbname

engine = create_engine(f"mysql://{username}:{password}@{host}:{port}/{dbname}?charset=utf8mb4")

with engine.connect() as conn:
    metadata = db.MetaData()
    table = db.Table('user', metadata, autoload=True, autoload_with=engine)
    query = db.insert(table).values(records)
    result_proxy = conn.execute(query)

