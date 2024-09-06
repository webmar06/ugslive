$(document).on('click','.cashoutnow',function(){
    $('#cashoutnowmodal').modal('show')
})



$('#cashOutform').on('submit', function(e) {
    e.preventDefault();
    var cashout   = document.getElementById("cashout").value;
    var balance   = document.getElementById("balance").value;
    const outbutton = document.getElementById('outbtn');
    cshout = parseFloat(cashout)
    balances = parseFloat(balance)
    if (balances >= cshout) {
        if (cashout!="" && cashout > 0) {
            Swal.fire({
                title: "Process cash out?",
                text: "Process now",
                icon: "question",
                showCancelButton: true,
                confirmButtonColor: "#3085d6",
                cancelButtonColor: "#d33",
                confirmButtonText: "Proceed!"
            }).then((result) => {
                if (result.isConfirmed) {
                    outbutton.disabled = true;
                    $.ajax({
                        method: 'POST',
                        url:'cashoutwallet',
                        data:{cashout:cashout},
                        success: function(res) {
                            outbutton.disabled = false;
                            if (res.data === 'ok') {
                                toastr["success"]("Cashout request successfully sent!");
                                document.getElementById('points').innerHTML=res.newPoints;
                                document.getElementById('walletview').innerHTML=res.newPoints;
                                document.getElementById('newtotalout').innerHTML=res.newtotalout;
                                document.getElementById('walletbal').innerHTML=res.newPoints;
                                
                                document.getElementById('balance').value=res.newPoints;
                                document.getElementById('cashout').value='';
                                $("#import_new_table").load('loadCashOutTbl');
                                $('#cashoutnowmodal').modal('hide')
                            }else if (res.data === 'insufficient') {
                                toastr["error"]("Insufficient points balance");  
                                
                            }else if (res.data === 'invalid') {
                                toastr["error"]("Invalid inputs!");  
                                
                            }else if (res.data === 'tryagain') {
                                toastr["error"]("Please try again after a few seconds.");  
                                
                            } else {
                                toastr["warning"]("Error: " + JSON.stringify(res.errors));
                            }
                        }
                    });
                }
            });
        } else {
            Swal.fire({
                title: "Invalid inputs!",
                icon: "error"
            });
        }
    }else{
        Swal.fire({
            title: "Insufficient Points Balance!",
            icon: "error"
        });
    }
});

var cashout = document.getElementById('cashout');
cashout.addEventListener("keydown", function(e) {
    if (invalidChars.includes(e.key)) {
        e.preventDefault();
    }
});