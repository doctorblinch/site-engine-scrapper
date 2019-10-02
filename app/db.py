import urllib.parse as up
import psycopg2

from app.user_async import UserAsync
import os

up.uses_netloc.append("postgres")
url = up.urlparse(os.environ.get('db_url'))


connection = psycopg2.connect(database=url.path[1:],
                              user=url.username,
                              password=url.password,
                              host=url.hostname,
                              port=url.port)


def read_user_from_db(id=None, name=None):
    cursor = connection.cursor()

    if id is not None:
        query = f"SELECT * FROM users WHERE (id = \'{id}\') ORDER BY id DESC LIMIT 1"
        cursor.execute(query)
    elif name is not None:
        query = f"SELECT * FROM users WHERE (name LIKE \'{name}\') ORDER BY id DESC LIMIT 1"
        cursor.execute(query)
    else:
        return

    record = cursor.fetchone()

    user = UserAsync(record[1])
    user.agent = {'User-Agent': record[2]}
    user.id_in_db = record[0]
    #user.cookies = read_cookies_from_file('data/' + record[3])

    return user

def scrapes_of_user(id):
    cursor = connection.cursor()

    if id is not None:
        query = f"SELECT * FROM scrapes WHERE (user_id = \'{id}\') ORDER BY id DESC"
        cursor.execute(query)
    else:
        return

    records = cursor.fetchall()
    return records

def read_users_from_db(quantity='all'):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users ORDER BY id DESC;")
    record = cursor.fetchall()
    if quantity == 'all':
        return record
    return record[-quantity:]
