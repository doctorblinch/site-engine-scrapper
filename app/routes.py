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


def compare_users_histories(history1, history2):
    engines1 = set()
    engines2 = set()
    for i in history1:
        engines1.add(i[7])
    for i in history2:
        engines2.add(i[7])

    #print(engines1, engines2)
    common_engines = engines1.intersection(engines2)

    result = {}
    queries1 = set()
    queries2 = set()
    for engine in common_engines:
        common_querries = set()
        different_querries = set()
        for i in history1:
            if i[7] == engine:
                queries1.add(i[2])
        for i in history2:
            if i[7] == engine:
                queries2.add(i[2])

        common_querries = queries1.intersection(queries2)
        different_querries = queries1.union(queries2).difference(common_querries)
        tmp = {'common': common_querries,'different': different_querries}
        print(engine)
        result.update({engine : tmp})
    return result



@app.route('/compare/<id1>/<id2>')
def compare(id1, id2):
    user1 = read_user_from_db(id=id1)
    history1 = scrapes_of_user(id=id1)
    user2 = read_user_from_db(id=id2)
    history2 = scrapes_of_user(id=id2)


    comparation = compare_users_histories(history1, history2)
    print('UFFFFFFFFFFFFFFFFFF=',comparation)

    return render_template('compare.html', user1 = user1, user2 = user2, history1 = history1, history2 = history2, cmp = comparation)
