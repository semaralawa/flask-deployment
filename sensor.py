import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify
)
from werkzeug.security import check_password_hash, generate_password_hash

from db import get_db

bp = Blueprint('sensor', __name__, url_prefix='/sensor')


@bp.route('/update', methods=('GET', 'POST'))
def update():

    if request.method == 'POST':
        # get every sensor variable
        username = request.form['username']
        temperature = request.form['temperature']
        humidity = request.form['humidity']
        soil_moist = request.form['soil_moist']

        db = get_db()
        error = None

        if db.execute(
            'SELECT id FROM user WHERE username = ?', (username,)
        ).fetchone() is None:
            error = f"User {username} is not registered."

        if error is None:
            # update database with new sensor value
            db.execute(
                'UPDATE sensor SET temperature = ? WHERE username = ?',
                (temperature, username)
            )
            db.execute(
                'UPDATE sensor SET humidity = ? WHERE username = ?',
                (humidity, username)
            )
            db.execute(
                'UPDATE sensor SET soil_moist = ? WHERE username = ?',
                (soil_moist, username)
            )
            db.commit()
            return '5'
        else:
            return error
        # flash(error)


def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv


@bp.route('/button', methods=('GET', 'POST'))
def button():
    if request.method == 'POST':
        username = request.form['username']
        button = request.form['button']
        state = request.form['state']

        db = get_db()
        error = None

        if db.execute(
            'SELECT id FROM user WHERE username = ?', (username,)
        ).fetchone() is None:
            error = f"User {username} is not registered."

        if button != 'lamp' and button != 'pump':
            error = 'wrong button'

        if error is None:
            # update database with new sensor value
            if button == 'lamp':
                db.execute(
                    'UPDATE sensor SET lamp = ? WHERE username = ?',
                    (state, username)
                )
            elif button == 'pump':
                db.execute(
                    'UPDATE sensor SET pump = ? WHERE username = ?',
                    (state, username)
                )
            db.commit()
            return '5'
        else:
            return error


@bp.route('/button/user=<username>&button=<button>&state=<state>')
def button_params(username, button, state):
    db = get_db()
    error = None

    if db.execute(
        'SELECT id FROM user WHERE username = ?', (username,)
    ).fetchone() is None:
        error = f"User {username} is not registered."

    if button != 'lamp' and button != 'pump':
        error = 'wrong button'
    if state != 'on' and state != 'off':
        error = 'wrong state'

    if error is None:
        # update database with new sensor value
        if button == 'lamp':
            db.execute(
                'UPDATE sensor SET lamp = ? WHERE username = ?',
                (state, username)
            )
        elif button == 'pump':
            db.execute(
                'UPDATE sensor SET pump = ? WHERE username = ?',
                (state, username)
            )
        db.commit()
        return 'data sent'
    else:
        return error


@bp.route('/get-button/user=<username>/button=<button>')
def get_one_button(username, button):
    user = query_db('select * from sensor where username = ?',
                    [username], one=True)
    data = user[button]
    return data

@bp.route('/get-button/user=<username>')
def get_button(username):
    data = {}
    user = query_db('select * from sensor where username = ?',
                    [username], one=True)
    data['lamp'] = user['lamp']
    data['pump'] = user['pump']
    return jsonify(data)
