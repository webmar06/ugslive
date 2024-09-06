$(document).ready(function(){

    // /////////////////////
    
    function load_users(){
        $.ajax({
            method:'POST',
            url:'getusers',
            success:function(res){
                $('#acc_tbl').html('')
                for(d in res.data){
                    if(res.data[d].type != 'SUPER ADMIN'){
                        if(res.data[d].status == 'ACTIVE'){
                            stat=' <button type="button" class="btn btn-success btn-sm mb-2 me-2 btn-stat" acc="'+res.data[d].user+'" aid="'+res.data[d].uid+'"  st="'+res.data[d].status+'" comirate="'+res.data[d].comrate+'">ACTIVE</button>'
                        }else if(res.data[d].status == 'INACTIVE'){
                            stat=' <button type="button" class="btn btn-warning btn-sm mb-2 me-2 btn-stat" acc="'+res.data[d].user+'" aid="'+res.data[d].uid+'"  st="'+res.data[d].status+'" comirate="'+res.data[d].comrate+'">INACTIVE</button>'
                        }else if(res.data[d].status == 'BANNED'){
                            stat=' <button type="button" class="btn btn-danger btn-sm mb-2 me-2 btn-stat" acc="'+res.data[d].user+'" aid="'+res.data[d].uid+'"  st="'+res.data[d].status+'" comirate="'+res.data[d].comrate+'">BANNED</button>'
                        }
                        
                        data='<tr>\
                     <td>'+res.data[d].datejoin+'</td>\
                    <td class="text-white fs-4" style="text-transform: capitalize;">'+res.data[d].user+'</td>\
                     <td>'+res.data[d].type+'</td>\
                    <td>'+res.data[d].wallet+'</td>\
                    <td>'+res.data[d].comrate+'</td>\
                    <td style="text-transform: capitalize;" class="fw-bolder">'+res.data[d].agent+'</td>\
                     <td>'+stat+'</td>\
                    <td><button type="button" class="btn btn-secondary btn-sm mb-2 me-2 btn-preview" acc="'+res.data[d].user+'" aid="'+res.data[d].uid+'" st="'+res.data[d].status+'"><i class="fa fa-eye"></i> View</button></td>\
                    </tr>'
                        
                        
                        $('#acc_tbl').append(data)
                    }
                }
                
            }
        })
    }

    // $(document).on('click','.btn-stat',function(){
    //     st=$(this).attr('st')
    //     acc=$(this).attr('acc')
    //     aid=$(this).attr('aid')
    //     $('.acc_stat').val(st)
    //     $('.acc_id').val(aid)
    //     $('.uname').text(acc)
    //     $('.adduser_err').html('')
    //     $('#upuser').modal('show')
        
    // })
    $(document).on('click','.btn-stat',function(){
        alert('xxx')
        st=$(this).attr('st')
        acc=$(this).attr('acc')
        aid=$(this).attr('aid')
        comrate=$(this).attr('comirate')
        
        $('.acc_stat').val(st)
        $('.acc_id').val(aid)
        $('.uname').text(acc)
        $('#agentcommi').val(comrate)
        $('.adduser_err').html('')
        $('#upuser').modal('show')
        
        var commission = document.getElementById('agentcommi');
        commission.addEventListener("keydown", function(e) {
            if (invalidChars.includes(e.key)) {
                e.preventDefault();
            }
        });
        
    })

    $(document).on('submit','#upuser_frm',function(e){
        e.preventDefault()
        var agntacc_stat  = document.getElementById("agntacc_stat").value;
        var agentcommi    = document.getElementById("agentcommi").value;
        if(agntacc_stat!=""){
            document.getElementById("nfacc_stat").innerHTML = '';
            if(agentcommi!=""){
                if(agentcommi <=0.12){
                    document.getElementById("nfadmincommi").innerHTML = '';
                    data=$(this).serializeArray()
                    $.ajax({
                        method:'POST',
                        url:'upstat',
                        data:data,
                        success:function(res){
                            console.log(JSON.stringify(res))
                            if(res.data == 'ok'){
                                toastr["success"]("Successfully done.");
                                document.getElementById("agentcommi").value='';
                                $('#upuser').modal('hide')
                                load_users()
                            }else{
                                toastr["error"]("Error processing request!");  
                            }
                        }
                    })
                }else{document.getElementById("nfadmincommi").innerHTML = 'Commission rate should not be exceeded in 12% only!'; $("#agentcommi").focus();}   
            }else{document.getElementById("nfadmincommi").innerHTML = 'Required!'; $("#agentcommi").focus();}
        }else{document.getElementById("nfacc_stat").innerHTML = 'Required!'; $("#agntacc_stat").focus();}
    })

    $('#account_reg').on('submit',function(e){
        e.preventDefault()
        $('.adduser_err').html('')
        data=$(this).serializeArray()
        if($('.pass1').val() != $('.pass2').val()){
        $('.adduser_err').append('<div class="alert alert-danger alert-dismissible fade show" role="alert">\
        <strong>Password Not Matched!</strong>\
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>\
        </div>')
        }else{
            
            $.ajax({
                method:'POST',
                url:'account_reg',
                data:data,
                success:function(res){
                    if(res.data == 'ok'){
                      $('#account_reg').trigger('reset')
                      load_users()
                        $('.adduser_err').append('<div class="alert alert-success alert-dismissible fade show" role="alert">\
                        <strong>Account was Created!</strong>\
                        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>\
                        </div>')
                    }
                }
            })
    
        }
    
        
    })


   

    // ////////////////

    // //////////////////
})