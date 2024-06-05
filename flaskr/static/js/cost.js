function calculateCost(note) {
    const url = 'http://172.19.100.16:5000/note/tx_cost'
    fetch(url, {
      headers : {
           'Content-Type' : 'application/json'
       },
       method : 'POST',
       body : JSON.stringify( {
           'note' : note,
       })
    })
    .then(response => response.json())  
    .then(json => {
        console.log(json);
        let transactionCost = json.tx_cost.toFixed(8)
        document.getElementById("transaction-cost").innerHTML = transactionCost
        document.getElementById("transaction-cost-hidden").value = transactionCost
    })
    .catch(error => console.error('Error:', error));
}

document.getElementById("note").addEventListener("input", function() {
    calculateCost(this.value);
});
