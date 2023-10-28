from flask import render_template, request, redirect
from .models import DBManager
from datetime import datetime

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

@app.route('/nuevo', methods=['POST'])
def nuevo():
    from_currency = request.form['from_currency']
    from_quantity = request.form['from_quantity']
    to_currency = request.form['to_currency']
    to_quantity = request.form['to_quantity']

    db = DBManager('balance/data/balance.db')
    consulta = 'INSERT INTO movimientos (fecha, hora, from_currency, from_quantity, to_currency, to_quantity) VALUES (?, ?, ?, ?, ?, ?)'
    dateNow = datetime.now()
    valores  = (dateNow.strftime("%d/%m/%Y"), dateNow.strftime("%H:%M:%S"), from_currency, from_quantity, to_currency, to_quantity)

    conexion, cursor = db.conectar()
    cursor.execute(consulta, valores)
    conexion.commit()
    return redirect('/')





































