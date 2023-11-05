from datetime import datetime
from dotenv import load_dotenv
from flask import render_template, request, redirect, flash
import os
import requests
import sys


from . import app
from .models import DBManager


load_dotenv()

db = DBManager('balance/data/balance.db')
apikey = os.getenv('apiKey')

@app.route('/')
def inicio():
    sql = 'SELECT * FROM movimientos'
    movimientos = db.consultaSQL(sql)

    return render_template('inicio.html', movs=movimientos, menu=1)

@app.route('/compra')
def compra():
    movimientos = "SELECT * FROM movimientos"
    movs = db.consultaSQL(movimientos)

    return render_template('compra.html', movements=movs, menu=2)

@app.route('/estado')
def estado():
    consulta = "SELECT SUM(from_quantity) as CantidadOrigen FROM movimientos WHERE from_currency = 'EUR'"
    valorTotal = db.consultaSQL(consulta)
    
    return render_template('estado.html', data=valorTotal, menu=3)

@app.route('/estado2')
def estado2():
    originCurrenciesQuery = f"SELECT DISTINCT from_currency as MonedaOrigen FROM movimientos"
    destinyCurrenciesQuery = f"SELECT DISTINCT to_currency as MonedaDestino FROM movimientos"
    originCurrencies = db.consultaSQL(originCurrenciesQuery)
    destinyCurrencies = db.consultaSQL(destinyCurrenciesQuery)
    listOriginCurrencies = []
    listDestinyCurrencies = []
    listOriginQuantity = []
    originQuantity = 0.0
    destinyQuantity = 0.0

    for monedaOrigen in originCurrencies:
        listOriginCurrencies.append(monedaOrigen["MonedaOrigen"])

    for monedaDestino in destinyCurrencies:
        listDestinyCurrencies.append(monedaDestino["MonedaDestino"])

    listMergedCurrencies = list(set(listOriginCurrencies) & set(listDestinyCurrencies))
    listMergedCurrenciesStr = ', '.join([f"'{item}'" for item in listMergedCurrencies])
    listMergedCurrenciesQuery = f"SELECT from_currency as MonedaOrigen, SUM(from_quantity) as SumaMonedaOrigen, to_currency as MonedaDestino, SUM(to_quantity) as SumaMonedaDestino FROM movimientos WHERE from_currency IN ({listMergedCurrenciesStr}) GROUP BY from_currency, to_currency"
    listMergedResult = db.consultaSQL(listMergedCurrenciesQuery)

    for listMergedResultItem in listMergedResult:
        if listMergedResultItem["MonedaOrigen"] == "EUR":
            destinyQuantity = float(listMergedResultItem["SumaMonedaDestino"])
        else:
            apiKey = apikey
            endpoint = f"https://rest.coinapi.io/v1/exchangerate/EUR?filter_asset_id={listMergedResultItem['MonedaOrigen']}&apikey={apiKey}"
            response = requests.request("GET", endpoint)
            jsonResponse = response.json()

            if response.status_code == 200:
                for r in jsonResponse["rates"]:
                    rate = r["rate"]
                    rateToCurrency = float(listMergedResultItem["SumaMonedaDestino"]) * float(rate) 
                    print(rateToCurrency)

                    listOriginQuantity.append(rateToCurrency)

    originQuantity = float(sum(listOriginQuantity))

    eurosInvertidos = "SELECT SUM(from_quantity) as CantidadOrigen FROM movimientos WHERE from_currency = 'EUR'"
    euros = db.consultaSQL(eurosInvertidos)

    for e in euros:
        resultadoActual = float(e["CantidadOrigen"]) - float(originQuantity)
        print(float(e["CantidadOrigen"]))
        print(originQuantity)
        finalResult = float(destinyQuantity) - float(resultadoActual)
        return redirect('/estado')

    return render_template('estado.html', Sum=finalResult, menu=3)

        

@app.route('/nuevo', methods=['POST'])
def nuevo():
    from_currency = request.form['from_currency']
    from_quantity = request.form['from_quantity']
    to_currency = request.form['to_currency']
    to_quantity = request.form['to_quantity']
    value_to_convert_hidden = request.form['value_to_convert_hidden']

    checkDbMoneda = f"SELECT to_currency FROM movimientos WHERE to_currency = '{from_currency}'"
    monedas = db.consultaSQL(checkDbMoneda)

    valoresSumaOrigen = f"SELECT SUM(from_quantity) as SumaMonedaOrigen FROM movimientos WHERE from_currency = '{from_currency}'"
    valoresSumaDestino = f"SELECT SUM(to_quantity) as SumaMonedaDestino FROM movimientos WHERE to_currency = '{from_currency}'"
    valorSumaOrigen = db.consultaSQL(valoresSumaOrigen)
    valorSumaDestino = db.consultaSQL(valoresSumaDestino)

    if from_currency != 'EUR':
        for sumaOrigen in valorSumaOrigen:
            for sumaDestino in valorSumaDestino:
                if sumaOrigen["SumaMonedaOrigen"] != None and sumaDestino["SumaMonedaDestino"] != None:
                    print(f"Origen: {valorSumaOrigen}")
                    print(f"Destino: {valorSumaDestino}")
                    if float(sumaOrigen["SumaMonedaOrigen"] + float(from_quantity)) >= float(sumaDestino["SumaMonedaDestino"]):
                        flash(f"No tienes permitido gastarte tantos {from_currency}. Asegúrate que metes una cantidad correcta.", "error")
                        return redirect('/compra')
        if monedas == []:
            flash(f"No existe el valor '{from_currency}' en la base de datos. Inserta una moneda en el campo origen que sepas que ya has invertido", "error")
            return redirect('/compra')
        for sumaDestino in valorSumaDestino:
            if sumaDestino["SumaMonedaDestino"] != None:
                if float(from_quantity) >= float(sumaDestino["SumaMonedaDestino"]):
                    flash(f"El valor invertido '{from_quantity}' es mayor a la suma de las cantidades anteriores invertidas '{sumaDestino['SumaMoneda']}'. Por favor, introduce un valor menor.", "error")
                    return redirect('/compra')

    if from_quantity == value_to_convert_hidden:
        # valoresMaximos = "SELECT to_currency as Moneda, MAX(to_quantity) as MaximoMoneda, SUM(to_quantity) as SumaMoneda FROM movimientos WHERE to_currency IN('EUR', 'BTC', 'ETH', 'ADA', 'SOL', 'DOT') GROUP BY to_currency"
        # valores = db.consultaSQL(valoresMaximos)

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