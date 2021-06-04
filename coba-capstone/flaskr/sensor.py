import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db

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
            return

        flash(error)

    return request.form
