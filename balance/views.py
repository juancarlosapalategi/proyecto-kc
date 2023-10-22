from flask import render_template
from .models import DBManager

from . import app

@app.route('/')
def inicio():
    db = DBManager('balance/data/balance.db')
    sql = 'SELECT * FROM movimientos'
    movimientos = db.consultaSQL(sql)

    return render_template('inicio.html', movs=movimientos)

@app.route('/compra')
def compra():
    return render_template('compra.html')

@app.route('/status')
def status():
    return render_template('estado.html')

@app.route('/movimiento')
def movimiento():
    return 'movimiento'




































