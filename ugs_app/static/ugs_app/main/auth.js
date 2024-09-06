$(document).ready(function(){
    // ///////////////////////////////
    
    $("form").attr('autocomplete', 'off');
    
    // Player Registration

    $('#register').on('submit',function(e){
        e.preventDefault()
        err='<div class="alert alert-danger alert-dismissible fade show" role="alert">\
        <strong>Invalid Username!</strong> Try Again!\
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>\
        </div>'
        data=$(this).serializeArray()
        pass1=$('.pass1').val()
        pass2=$('.pass2').val()
        $('.message').html('')
        if(pass1 != pass2){
            Swal.fire({
                title: "Password Not Matched!",
                text:'Validate Your Password',
                icon: "error"
                });

        }else{
            $.ajax({
                method:"POST",
                url:"../../player_reg",
                data:data,
                success:function(res){
                    if(res.data == 'ok'){
                        window.location.href='../../'
                    }else{
                        $('.message').append(err)
                    }
                    console.log(res.data)
                }
            })
        }
        

    })

    // LOGIN SUBMIT
    $('#auth').on('submit',function(e){
        e.preventDefault()
        err='<div class="alert alert-danger alert-dismissible fade show" role="alert">\
        <strong>Authentication Error!</strong> Invalid Credentials!\
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>\
        </div>'
       inact='<div class="alert alert-danger alert-dismissible fade show" role="alert">\
        <strong>Inactive Account!</strong> Please Try Again!\
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>\
        </div>'
        data=$(this).serializeArray()
        
        $.ajax({
            method:'POST',
            url:'auth_user',
            data:data,
            success:function(res){
               
               if(res.data == 'err'){
                Swal.fire({
                    title: "Invalid Credentials!",
                    icon: "error"
                    });
                    $(this).trigger('reset')
                   
               }else if(res.data == 'inactive'){
                Swal.fire({
                    title: "Account is not Activated",
                    icon: "erro"
                    });
                    $(this).trigger('reset')

               }else{   
                window.location.href = 'homepage';
              
               }
               
            }
        })
        
    })
    
    // /////////////////////////////////
   
    
    // //////////////////////////////////
    })