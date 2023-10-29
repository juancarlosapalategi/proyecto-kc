from flask import render_template, request, redirect, flash
from .models import DBManager
from datetime import datetime
from . import app

@app.route('/')
def inicio():
    db = DBManager('balance/data/balance.db')
    sql = 'SELECT * FROM movimientos'
    movimientos = db.consultaSQL(sql)

    return render_template('inicio.html', movs=movimientos, menu=1)

@app.route('/compra')
def compra():
    return render_template('compra.html', menu=2)

@app.route('/estado')
def estado():
    db = DBManager('balance/data/balance.db')
    consulta = "SELECT SUM(from_quantity) as CantidadOrigen FROM movimientos WHERE from_currency = 'EUR'"
    datos = db.consultaSQL(consulta)
    
    return render_template('estado.html', data=datos, menu=3)

@app.route('/nuevo', methods=['POST'])
def nuevo():
    from_currency = request.form['from_currency']
    from_quantity = request.form['from_quantity']
    to_currency = request.form['to_currency']
    to_quantity = request.form['to_quantity']
    value_to_convert_hidden = request.form['value_to_convert_hidden']
    error = None

    if from_quantity == value_to_convert_hidden:
        db = DBManager('balance/data/balance.db')
        consulta = 'INSERT INTO movimientos (fecha, hora, from_currency, from_quantity, to_currency, to_quantity) VALUES (?, ?, ?, ?, ?, ?)'
        dateNow = datetime.now()
        valores  = (dateNow.strftime("%d/%m/%Y"), dateNow.strftime("%H:%M:%S"), from_currency, from_quantity, to_currency, to_quantity)

        conexion, cursor = db.conectar()
        cursor.execute(consulta, valores)
        conexion.commit()

        flash("Nuevo registro insertado correctamente", "message")
        return redirect('/')
    else:
        flash("Hemos detectado que el valor a invertir no se corresponde con el introducido al calcular. Por favor, corrígelo y vuelve a probar.", "error")
        return redirect('/compra')