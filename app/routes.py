from flask import render_template

from app import app
from app.db import read_users_from_db, read_user_from_db, scrapes_of_user

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/bots')
def all_bots():
    users = read_users_from_db()
    return render_template('all_users.html', users=users)

@app.route('/bot/<id>')
def bot_page(id):
    user = read_user_from_db(id=id)
    users = read_users_from_db()
    history = scrapes_of_user(id=id)
    return render_template('bot.html', user = user, history = history, users = users)

@app.route('/compare/<id1>/<id2>')
def compare(id1, id2):
    user1 = read_user_from_db(id=id1)
    history1 = scrapes_of_user(id=id1)
    user2 = read_user_from_db(id=id2)
    history2 = scrapes_of_user(id=id2)
    return render_template('compare.html', user1 = user1, user2 = user2, history1 = history1, history2 = history2)
