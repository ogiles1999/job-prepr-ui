import sqlalchemy
from utils.db_connect import create_pool
from utils.db_password import hash_password, check_password
import json
import datetime

def create_new_user(email: str, password: str) -> None:
    """
    Creates a new user in the users table. Returns error message if email is already associated with an account.
    """
    pool = create_pool()

    salt, hashed_password = hash_password(password)

    with pool.connect() as db_conn:
        try:
            db_conn.execute("INSERT INTO users (email, password, salt) VALUES (%s,%s,%s)", (email, hashed_password, salt))
        except:
            return "Email is already taken"

    return "Account created!"

def login_user(email: str, password: str) -> bool:
    """"
    Authenticates a user's login credentials.
    """
    pool = create_pool()

    with pool.connect() as db_conn:
        result = db_conn.execute("SELECT password, salt FROM users WHERE email = %s", (email)).fetchall()

    if len(result) == 0:
        return "Invalid email or password"

    hashed_password, salt = result[0]

    if check_password(password, salt, hashed_password):
        return 'Login Successful'

    return "Invalid email or password"

def save_results(user_id: int, results: json) -> None:
    """
    Saves the results of a question response as a json object.
    """
    pool = create_pool()

    with pool.connect() as db_conn:
        db_conn.execute("INSERT INTO results VALUES (%s, %s, %s)", (user_id, datetime.now(), results))

    return None

def read_results(user_id: int):
    """
    Returns a user's results history
    """
    pool = create_pool()

    with pool.connect() as db_conn:
        result = db_conn.execute("SELECT tstamp, results FROM results WHERE user_id = %s", (user_id)).fetchall()

    return result
