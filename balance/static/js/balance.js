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