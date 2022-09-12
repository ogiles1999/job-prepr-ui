import sqlalchemy
from db_connect import create_pool
from db_password import hash_password, check_password

def create_new_user(email: str, password: str) -> None:

    pool = create_pool()

    salt, hashed_password = hash_password(password)

    with pool.connect() as db_conn:
        try:
            db_conn.execute("INSERT INTO users (email, password, salt) VALUES (%s,%s,%s)", (email, hashed_password, salt))
        except:
            return "Email is already taken"

    return "Account created!"

def login_user(email: str, password: str) -> bool:

    pool = create_pool()

    with pool.connect() as db_conn:
        result = db_conn.execute("SELECT password, salt FROM users WHERE email = %s", (email)).fetchall()

    if len(result) == 0:
        return "Invalid email or password"

    hashed_password, salt = result[0]

    if check_password(password, salt, hashed_password):
        return 'Login Successful'

    return "Invalid email or password"
