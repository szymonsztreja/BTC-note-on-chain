function checkPayment() {
    //const url = 'http://172.19.100.16:5000/note/get_utxo'
    const url = '/note/get_utxo' 
    fetch(url, {
      headers : {
           'Content-Type' : 'application/json'
       },
       method : 'GET',
    })
    .then(response => response.json())  
    .then(json => {
        console.log(json);
        //const amount =  document.getElementById("amount").innerText
        const amountToPay = parseFloat(document.getElementById("amount").innerText.split(' ')[0]);
        let payRecived = json.total_recived
        console.log(amountToPay)
        if (payRecived <= amountToPay && payRecived > 0) {
            document.getElementById("status").innerText = "Payment received!";
            // redirect to a success page
            window.location.replace("/note/success");
        } else {
            document.getElementById("status").innerText = "Payment not yet received.";
        }
     })
    .catch(error => console.error('Error:', error));
}

document.getElementById("check-payment-status").addEventListener("click", function() {
    checkPayment();
});

