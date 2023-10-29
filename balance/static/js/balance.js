function loadCurrencies() {
    var request = new XMLHttpRequest();
    var apikey = "E32AC0F0-3997-41B6-990F-19606ECC33ED";
    var from = document.getElementById('currency-from').value;
    var to = document.getElementById('currency-to').value;
    var valueToConvert = document.getElementById('value-to-convert');
    document.getElementById("value-to-convert-hidden").value = valueToConvert.value;

    if (valueToConvert.value == "") {
        alert("Disculpa, pero para calcular la conversión de " + from + " a " + to + " tienes que rellenar el campo 'Valor a invertir'");
        valueToConvert.focus();
        return;
    }

    if (from.toLowerCase() == to.toLowerCase()) {
        alert("Lo siento, pero de " + from + " a " + to + " no me puedes convertir. Por favor, selecciona dos monedas diferentes");
        return;
    }
    else {
        request.open('GET', 'https://rest.coinapi.io/v1/exchangerate/' + from + '/' + to + '?apikey=' + apikey, false);
        request.send();

        var result = JSON.parse(request.responseText);
        var rate = result.rate;
        var quantity = parseFloat(valueToConvert.value) * parseFloat(rate);
        var unitPrice = parseFloat(valueToConvert.value) / parseFloat(quantity);
        document.getElementById("quantity").value = quantity;
        document.getElementById("unitPrice").value = unitPrice.toFixed(2);
    }
}

// function savePurchaseData() {
//     alert("entra")
//     var from = document.getElementById('currency-from').value;
//     var to = document.getElementById('currency-to').value;
//     var valueToConvert = document.getElementById('value-to-convert');

//     const sqlite3 = require('sqlite3').verbose();

//     // Create/connect to the database
//     const db = new sqlite3.Database('balance.db');

//     // Insert data
//     const insertQuery = `INSERT INTO movimientos (fecha, hora, From_currency, From_quantity, To_currency, To_quantity) VALUES (?, ?, ?, ?, ?, ?)`;
//     var fecha = dateFormatted();
//     var hora = hourFormatted();
//     var From_currency = from;
//     var From_quantity = valueToConvert;
//     var To_currency = to;
//     var To_quantity = document.getElementById("quantity").value;

//     db.run(insertQuery, [fecha, hora, From_currency, From_quantity, To_currency, To_quantity], function (err) {
//         if (err) {
//             console.error(err.message);
//         } else {
//             alert(`Data with new ID ${this.lastID} has been inserted`);
//             console.log(`Inserted data with id ${this.lastID}`);
//         }
//     });

//     // Close the database connection
//     db.close();
// }

// function dateFormatted() {
//     const date = new Date();
//     let currentDay = String(date.getDate()).padStart(2, '0');
//     let currentMonth = String(date.getMonth() + 1).padStart(2, "0");
//     let currentYear = date.getFullYear();
//     let currentDate = `${currentDay}/${currentMonth}/${currentYear}`;

//     return currentDate;
// }

// function hourFormatted() {
//     const date = new Date();
//     let hour = String(date.getHours()).padStart(2, '0');
//     let minutes = String(date.getMinutes()).padStart(2, '0');
//     let currentHour = `${hour}:${minutes}`;

//     return currentHour;
// }