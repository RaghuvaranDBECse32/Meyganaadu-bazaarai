async function loadData(){

let response = await fetch("http://127.0.0.1:8000/forecast")

let data = await response.json()

let table = document.getElementById("table")

data.forecast.forEach(item => {

let row = table.insertRow()

row.insertCell(0).innerHTML = item.product
row.insertCell(1).innerHTML = item.sales
row.insertCell(2).innerHTML = item.price
row.insertCell(3).innerHTML = item.forecast

})

}
