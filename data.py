import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify
)

from db import get_db

bp = Blueprint('data', __name__, url_prefix='/data')


def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv


@bp.route('/all_user')
def all_user():
    data = 'username\tpassword\n'
    for user in query_db('select * from user'):
        data += f"{user['username']}\t\t{user['password']}\n"
    return (render_template('content.html', text=data))


@bp.route('/all_sensor')
def all_sensor():
    data = 'username\ttemperature\thumidity\tsoil moisture\tlamp state\tpump state\n'
    for user in query_db('select * from sensor'):
        data += f"{user['username']}\t\t{user['temperature']}\t\t{user['humidity']}\t\t{user['soil_moist']}\t\t{user['lamp']}\t\t{user['pump']}\n"
    return (render_template('content.html', text=data))


@bp.route('/user=<username>')
def single_user(username):
    data = {}
    user = query_db('select * from sensor where username = ?',
                    [username], one=True)
    data['username'] = user['username']
    data['temperature'] = user['temperature']
    data['humidity'] = user['humidity']
    data['soilMoisture'] = user['soil_moist']
    return jsonify(data)
