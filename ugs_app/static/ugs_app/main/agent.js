
$(document).on('click','.btn-actvateplyr',function(){
    accid=$(this).attr('accid')
    acc=$(this).attr('acct')
    comrate=$(this).attr('comrate')
    usertype=$(this).attr('plstat')
    
    if(usertype == 'PLAYER'){
        document.getElementById('commission').readOnly  = true;
        document.getElementById('commission').value = '0.00';
        $('#nfcommission').text('Commissions are applicable only to agent accounts.')
    }else{
        document.getElementById('commission').readOnly  = false;
        document.getElementById('commission').value = comrate;
        $('#nfcommission').text('')
    }
    $('.acct_id').val(accid)
    $('.unames').text(acc)
    $('.adduser_err').html('')
    $('#activateplyr').modal('show')
})







$(document).on('submit','#activate_form',function(e){
    e.preventDefault()
    var plstatus   = document.getElementById("plstatus").value;
    var commission = document.getElementById("commission").value;
    var acct_id    = document.getElementById("acct_id").value;
    var commirate    = document.getElementById("commirate").value;
    
    if(plstatus!=""){
        document.getElementById("nfplstatus").innerHTML = '';
        if(commission!=""){
            document.getElementById("nfcommission").innerHTML = '';
            if(acct_id!=""){
                document.getElementById("notifid").innerHTML = '';
                
                var comrate = parseFloat(commirate);
                var comm = parseFloat(commission);
                
                if(comrate >= comm){
                    data=$(this).serializeArray()
                    $.ajax({
                        method:'POST',
                        url:'upplyrstat',
                        data:data,
                        success:function(res){
                            if(res.data == 'ok'){
                                document.getElementById("commirate").value = res.nwcommi; 
                                document.getElementById("commis").innerHTML = res.nwcommi; 
                                toastr["success"]("Successfully done.");
                                document.getElementById("commission").value='';
                                $('#activateplyr').modal('hide')
                                $("#import_raw_table").load('load_new_user');
                            }else{
                                toastr["error"]("Error processing request!");  
                            }
                        }
                    })
                }else{
                    toastr["error"]("Current commission is not enough!");
                }
            }else{document.getElementById("notifid").innerHTML = 'Required!'; $("#acct_id").focus();}
        }else{document.getElementById("nfcommission").innerHTML = 'Required!'; $("#commission").focus();}
    }else{document.getElementById("nfplstatus").innerHTML = 'Required!'; $("#plstatus").focus();}
})
















