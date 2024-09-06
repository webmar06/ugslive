$(document).ready(function(){
    $(document).on('click','.nxtfight',function(){
        fight=$(this).attr('game')
        game=$(this).attr('id')
        multi=$('.bmulti').val()
        
        Swal.fire({
            title: 'Next Fight?',
            text: "Please confirm your Action!",
            icon: "warning",
            showCancelButton: true,
            confirmButtonColor: "#3085d6",
            cancelButtonColor: "#d33",
            confirmButtonText: "Proceed!"
        }).then((result) => {
            if (result.isConfirmed) {                
                $.ajax({
                    method:'POST',
                    url:'../../nxtfight',
                    data:{fight:fight,game:game,multi,multi},
                    success:function(res){
                        get_fight(game)
                        
                    }
                })
            }
        });
    })
    
    
    
    
    
    
    $(document).on('click','.disburse_btn',function(){
        fight=$(this).attr('game')
        Swal.fire({
            title: 'Disburse Payment?',
            text: "Please confirm your Action!",
            icon: "warning",
            showCancelButton: true,
            confirmButtonColor: "#3085d6",
            cancelButtonColor: "#d33",
            confirmButtonText: "Revert!"
        }).then((result) => {
            if (result.isConfirmed) {
                $.ajax({
                    method:'POST',
                    url:'../../disburse',
                    data:{fight:fight},
                    success:function(res){
                        socket.send(JSON.stringify({
                            'bet_stat': 'DONE',
                            'amount': 0,
                            'betin':'',
                            'fight_no':'',
                            
                        }))                        
                    }
                })
            }
        });
    })
    
    
    
    
    
    
    
    $(document).on('click','.revert_btn',function(){
        fight=$(this).attr('game')
        Swal.fire({
            title: 'Revert Declaration?',
            text: "Please confirm your Action!",
            icon: "warning",
            showCancelButton: true,
            confirmButtonColor: "#3085d6",
            cancelButtonColor: "#d33",
            confirmButtonText: "Revert!"
        }).then((result) => {
            if (result.isConfirmed) {                
                $.ajax({
                    method:'POST',
                    url:'../../revert',
                    data:{fight:fight},
                    success:function(res){
                        socket.send(JSON.stringify({
                            'bet_stat': 'CLOSE',
                            'amount': 0,
                            'betin':'',
                            'fight_no':'',
                        }))
                    }
                })
            }
        });
    })
    
    
    
    
    
    
    $(document).on('click','.betwin',function(res){
        winner=$(this).attr('id')
        fight=$(this).attr('game')
        gameid=$(this).attr('gameid')
        
        if(winner != 'DRAW'){
            msg=winner+' WINS?'
        }else{
            msg='DRAW FIGHT?'
        }
        Swal.fire({
            title: msg,
            text: "Please confirm your Actiona!",
            icon: "warning",
            showCancelButton: true,
            confirmButtonColor: "#3085d6",
            cancelButtonColor: "#d33",
            confirmButtonText: winner+" WINS!"
        }).then((result) => {
            if (result.isConfirmed) {
                $.ajax({
                    method:'POST',
                    url:'../../setwinner',
                    data:{fight:fight,winner:winner,gameid:gameid},
                    success:function(res){
                        socket.send(JSON.stringify({
                            'bet_stat': 'DECLARED',
                            'amount': 0,
                            'betin':'',
                            'fight_no':'',
                            
                            
                        }))
                    }
                })
            }
        });
    })
    
    
    
    
    
    
    
    
    $(document).on('click','.longbetwin',function(res){
        winner=$(this).attr('id')
        fight=$(this).attr('game')
        gameid=$(this).attr('gameid')
        
        msg='LONGEST FIGHT?'
        Swal.fire({
            title: msg,
            text: "Please confirm your action!",
            icon: "warning",
            input: 'number',
            inputPlaceholder: 'Enter fight number',
            showCancelButton: true,
            confirmButtonColor: "#3085d6",
            cancelButtonColor: "#d33",
            confirmButtonText: "LONGEST FIGHT!",
            preConfirm: (fvalue) => {
                if (!fvalue) {
                    Swal.showValidationMessage('You need to enter fight number!'); 
                }
                return fvalue;
            }
            
        }).then((result) => {
            if (result.isConfirmed) {
                const fvalue = result.value;
                $.ajax({
                    method:'POST',
                    url:'../../setlongwin',
                    data:{fight:fight,winner:winner,gameid:gameid,fightnum:fvalue},
                    success:function(res){
                        if(res.data == 'ok'){
                            Swal.fire({
                                title: "Successfully disburse!",
                                icon: "success"
                            });
                        }else{
                            Swal.fire({
                                title: "No bets found in longest fight!",
                                icon: "error"
                            });
                        }
                        socket.send(JSON.stringify({
                            'bet_stat': 'DECLARED',
                            'amount': 0,
                            'betin':'',
                            'fight_no':'',
                        }))
                    }
                })
            }
        });
    })
    
    
    
    
    
    
    
    $(document).on('click','.addfight',function(){
        gfid=$(this).attr('id')
        get_fight(gfid)
        $('#fightsetting').modal('toggle')
    })
    
    
    
    // Fight SUBMIT
    $(document).on('submit','#fsetting',function(e){
        e.preventDefault()
        data=$(this).serializeArray()
        gfid=$('#gid').val()
        fnum=$('.fight_no').val()
        fmulti=$('.fmulti').val()
        if( $('.sub_type').is(':checked') ){
            typ='UPDATE ONGOING FIGHT?'
        }
        else{
            typ='CREATE NEW FIGHT?'
        }
        
        Swal.fire({
            title: typ,
            text: "Please confirm your Action!",
            icon: "warning",
            showCancelButton: true,
            confirmButtonColor: "#3085d6",
            cancelButtonColor: "#d33",
            confirmButtonText: "Proceed!"
        }).then((result) => {
            if (result.isConfirmed) {
                // ///////////////////////////
                if(fnum == 0 || fmulti == 0){
                    Swal.fire({
                        title: "Please Input a Valid Entry!",
                        icon: "error"
                    });
                }else{
                    
                    $.ajax({
                        method:'POST',
                        url:'../../addfight',
                        data:data,
                        success:function(res){
                            get_fight(gfid)
                            if(res.data == 'update'){
                                Swal.fire({
                                    title: "Update Successfully!",
                                    icon: "success"
                                });
                                $('#fightsetting').modal('hide')
                            }else if(res.data == 'insert' ){
                                Swal.fire({
                                    title: "Create New Fight Success!",
                                    icon: "success"
                                });
                                $('#fightsetting').modal('hide')
                            }else if(res.data == 'exist' ){
                                Swal.fire({
                                    title: "Fight Number Exist!",
                                    icon: "error"
                                });
                                
                            }else{
                                Swal.fire({
                                    title: "Error Command!",
                                    icon: "error"
                                });
                            }
                        }
                    })
                    
                }
                
                // //////////////////////////
            }
        });
        
        
        
    })
    
    // Fight sub
    $('.sub_type').on('change',function(){
        
        if( $(this).is(':checked') ){
            $('.fsubmit').text('Update Current Fight?')
            $('.ftype').text('Update Existing Fight?')
        }
        else{
            $('.fsubmit').text('Create New Fight?')
            $('.ftype').text('Create New Fight?')
        }
        
        
    })
    
    //  load_games()
    function load_games(){
        $.ajax({
            url:'load_games',
            type:'POST',
            success:function(res){
                st=''
                $('#games_tbl').html('')
                for(g in res){  
                    if(res[g].fields.g_status == 'CLOSED'){
                        st='<span class="badge text-bg-danger">CLOSED</span>'
                    }else if(res[g].fields.g_status == 'OPEN'){
                        st='<span class="badge text-bg-success">OPEN</span>'
                    }
                    
                    data='<tr>\
                <td>'+moment(res[g].fields.g_created).format('YYYY-MM-DD hh:m a')+'</td>\
                 <td class="text-white fw-bolder fs-4">'+res[g].fields.g_name+'</td>\
                 <td>'+res[g].fields.g_category+'</td>\
                 <td class="text-white fw-bolder fs-4">'+res[g].fields.g_plasada+'</td>\
                 <td>'+st+'</td>\
                 <td class="text-center"><button type="button" class="btn btn-outline-warning mb-2 me-2 g_update" id="'+res[g].pk+'"><i class="fa fa-edit"></i> Update</button>\
                 <a type="button" class="btn btn-outline-primary mb-2 me-2 g_preview" href="decla/arena/'+res[g].pk+'" %}" id="'+res[g].pk+'"><i class="fa fa-eye"></i> Preview</a>\
                 <button type="button" class="btn btn-outline-danger mb-2 me-2 del_games" id="'+res[g].pk+'" ><i class="icon_close_alt2"></i> Remove</button>\
                </tr>'
                    
                    $('#games_tbl').append(data)
                }
            }
        })
        
        
    }
    // /////////////// add fight modal
    
    
    // ///////////////del games
    
    $(document).on('click','.del_games',function(){
        did=$(this).attr('id')
        
        Swal.fire({
            title: "REMOVE GAMES ?",
            text: "You're to close Delete Games!",
            icon: "warning",
            showCancelButton: true,
            confirmButtonColor: "#3085d6",
            cancelButtonColor: "#d33",
            confirmButtonText: "Proceed!"
        }).then((result) => {
            if (result.isConfirmed) {
                // ///////////////////////////
                $.ajax({
                    method:'POST',
                    url:'delgame',
                    data:{did:did},
                    success:function(res){
                        if(res.data == 'ok'){
                            load_games()
                        }
                    }
                })
                
                // //////////////////////////
            }
        });
        
    })
    // //////////////////// add games
    $('#addgame').on('submit',function(e){
        e.preventDefault()
        $('.msg').html('')
        
        $.ajax({
            url: "add_games",
            type: "POST",
            data: new FormData(this),
            cenctype: 'multipart/form-data',
            processData: false,
            contentType: false,   
            success: function(res){
                load_games()
                if(res.data == 'ok'){
                    $('.msg').append('<div class="alert alert-success alert-dismissible fade show" role="alert">\
                <strong>Game was Created!</strong>\
                <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>\
                </div>')
                        $('#addgame').trigger('reset')
                        
                    }
                },
                error: function(){
                    alert(res.data)
                }
            });
        })
        
        // ///////////////// update game
        function get_fight(gfid){
            cgame=$('.gname').text()
            $.ajax({
                method:'POST',
                url:'../../gfight',
                data:{gfid:gfid},
                success:function(res){
                    $('.fight_no').val(res.data.fnum)
                    $('.fmulti').val(res.data.fmulti)
                    $('.bmulti').val(res.data.fmulti)
                    $('.f_game').val(res.data.game)
                    $('.fid').val(res.data.fight)
                    $('.fstat').val(res.data.fstat)
                    $('.f_winner').val(res.data.fwin)
                    $('.f_longest').val(res.data.flong)
                    $('.fnum_dis').text(res.data.fnum)
                    $('.fgame').val(cgame)
                    
                    $('.notif').html('')
                    $('.controls').html('')
                    
                    
                    socket.send(JSON.stringify({
                        'bet_stat': 'OPEN',
                        'amount': 0,
                        'betin':'',
                        'fight_no':res.data.fnum,
                        
                        
                    }))
                    
                    
                }
            })
        }
        
        $('#updategame').on('submit',function(e){
            e.preventDefault()
            $('.msg').html('')
            $.ajax({
                url: "update_games",
                type: "POST",
                data: new FormData(this),
                cenctype: 'multipart/form-data',
                processData: false,
                contentType: false,   
                success: function(res){
                    Swal.fire({
                        title: "Update Successfull",
                        icon: "success"
                    });
                    $('#updategames').modal('hide')
                    load_games()
                    
                },
                error: function(){
                    alert(res.data)
                }
            });
        })
        // //////////////////
        
        // /////////////// UPDATE
        $(document).on('click','.g_update',function(){
            gid=$(this).attr('id')
            
            $.ajax({
                method:'POST',
                url:'getgame',
                data:{gid:gid},
                success:function(res){
                    for(r in res){
                        $('.g_id').val(gid)
                        $('.g_name').val(res[r].gname)
                        $('.g_redname').val(res[r].meron)
                        $('.g_bluename').val(res[r].wala)
                        $('.g_plasada').val(res[r].plasada)
                        $('.g_desc').val(res[r].desc)
                        $('.g_category').val(res[r].category)
                        $('.g_link').val(res[r].link)
                        $('.gimage').val(res[r].image)
                        $('.g_status').val(res[r].status)
                        // ('.g_image').val(res[r].image)
                        $('.img_preview').attr('src',res[r].image)
                    }   
                    $('#updategames').modal('show')
                }
            })
        })
        
        // /////////// control btn
        $(document).on('click','.callbtn',function(){
            gfid=$('#gid').val()
            typ=$(this).attr('typ')
            fid=$(this).attr('game')
            bmulti=$('.bmulti').val()
            if(bmulti == 0){
                Swal.fire({
                    title: "Bet Multiplier Required!",
                    icon: "error"
                });
            }else{
                Swal.fire({
                    title: ""+typ+" BET ?",
                    text: "You're about to update Fight!",
                    icon: "warning",
                    showCancelButton: true,
                    confirmButtonColor: "#3085d6",
                    cancelButtonColor: "#d33",
                    confirmButtonText: "Proceed!"
                }).then((result) => {
                    if (result.isConfirmed) {
                        // ///////////////////////////
                        $.ajax({
                            method:'POST',
                            url:'../../fight_stat',
                            data:{fid:fid,typ:typ},
                            success:function(res){
                                if(res.data == 1){
                                    get_fight(gfid)
                                }
                            }
                        })
                        
                        // //////////////////////////
                    }
                });
                
            }
            
            
            
        })
        
        // /////////// WEBSOCKET
        const ongame=JSON.parse(document.getElementById('arena_game').textContent)
        var socket= new WebSocket('ws://'+window.location.host+'/ws/arena/'+ongame);
        
        
        socket.onmessage =function(e){    
            // ON MESSAGE
            result=JSON.parse(e.data)
            $('.notif').html('')
            $('.controls').html('')
            
            if(result.winner == 'MERON'){
                $('.meron_box').addClass('meron-win')
                $('.wala_box').removeClass('wala-win')
                $('.draw_box').removeClass('draw-win')
                $('#meron-win').attr('hidden',false)
                $('#wala-win').attr('hidden',true)
                $('#draw-win').attr('hidden',true)
            }else if(result.winner == 'WALA'){
                $('.meron_box').removeClass('meron-win')
                $('.draw_box').removeClass('draw-win')
                $('.wala_box').addClass('wala-win')
                $('#meron-win').attr('hidden',true)
                $('#wala-win').attr('hidden',false)
                $('#draw-win').attr('hidden',true)
            }else if(result.winner == 'DRAW'){
                $('.draw_box').addClass('draw-win')
                $('.meron_box').removeClass('meron-win')
                $('.wala_box').removeClass('wala-win')
                $('#meron-win').attr('hidden',true)
                $('#wala-win').attr('hidden',true)
                $('#draw-win').attr('hidden',false)
            }else if(result.winner == ''){
                $('.meron_box').removeClass('meron-win')
                $('.wala_box').removeClass('wala-win')
                $('.draw_box').removeClass('draw-win')
                $('#meron-win').attr('hidden',true)
                $('#wala-win').attr('hidden',true)
                $('#draw-win').attr('hidden',true)
            }
            
            
            notif=''
            if(result.bet_status == 'OPEN'){
                ctr='<button class="btn btn-warning callbtn col-12 fs-2 mb-2 " typ="LAST CALL" game="'+result.fightid+'">LAST CALL BET</button>'
                notif='<span class="badge bg-success fw-bolder fs-4 closenotif" >OPEN</span>'
            }else if(result.bet_status == 'LAST CALL'){
                ctr='<button class="btn btn-danger callbtn col-12 fs-2 mb-2 " typ="CLOSING" game="'+result.fightid+'">CLOSE BET</button>'
                notif='<span class="badge bg-warning text-danger fw-bolder fs-4  blink callnotif" >LAST CALL</span>'
                
            }else if(result.bet_status == 'CLOSING'){
                ctr='<div class="row"> <div class="col-6 mt-2">\
             <button class="btn btn-danger fs-2 w-100 betwin" game="'+result.fightid+'"  id="MERON" gameid="'+result.game_id+'">MERON WIN?</button></div>\
             <div class="col-6 mt-2">\
               <button class="btn btn-primary fs-2 w-100 betwin" game="'+result.fightid+'" id="WALA" gameid="'+result.game_id+'">WALA WIN?</button>\
               </div><div class="col-6 mt-2">\
                <button class="btn btn-success fs-2 w-100 betwin" game="'+result.fightid+'" id="DRAW" gameid="'+result.game_id+'">DRAW WIN?</button>\
              </div><div class="col-6 mt-2">\
               <button class="btn btn-secondary fs-2 w-100 betwin"  game="'+result.fightid+'" id="CANCELLED" gameid="'+result.game_id+'">CANCEL FIGHT?</button>\
                    </div></div>\
                <br>\
               <button class="btn btn-warning fs-2 w-100 longbetwin"  game="'+result.fightid+'" id="LONGEST" gameid="'+result.game_id+'">LONGEST FIGHT?</button>'
                
                notif=' <span class="badge bg-danger fw-bolder fs-4    closenotif" >CLOSED</span>'
                
            }else if(result.bet_status == 'DECLARED'){
                notif=' <span class="badge bg-danger fw-bolder fs-4    closenotif" >CLOSED</span>'
                ctr='<div class="row"><div class="col-12 mt-2">\
              <button class="btn btn-secondary fs-2 w-100 revert_btn"  game="'+result.fightid+'" >REVERT?</button>\
               </div> <div class="col-12 mt-2">\
                <button class="btn btn-danger fs-2 w-100 disburse_btn"  game="'+result.fightid+'"  >DISBURSE </button>\
               </div></div>\
               <br>\
               <button class="btn btn-warning fs-2 w-100 longbetwin"  game="'+result.fightid+'" id="LONGEST" gameid="'+result.game_id+'">LONGEST FIGHT?</button>'
                
                
                
            }else if(result.bet_status == 'CLOSED'){
                notif=' <span class="badge bg-danger fw-bolder fs-4    closenotif" >CLOSED</span>'
                ctr='<button class="btn btn-success callbtn col-12 fs-2 mb-2 " typ="OPEN" game="'+result.fightid+'">OPEN BET</button>'
            }else if(result.bet_status == 'DONE'){
                notif=' <span class="badge bg-danger fw-bolder fs-4    closenotif" >CLOSED</span>'
                ctr='<button class="btn btn-success nxtfight col-12 fs-2 mb-2  " id="'+result.game_id+'" typ="NEW"  game="'+result.fightid+'" > NEW FIGHT?</button>'
                $('.meron_box').removeClass('meron-win')
                $('.wala_box').removeClass('wala-win')
                $('.draw_box').removeClass('draw-win')
                $('#meron-win').attr('hidden',true)
                $('#wala-win').attr('hidden',true)
                $('#draw-win').attr('hidden',true)
            }
            else if(result.bet_status == ''){
                notif=' <span class="badge bg-danger fw-bolder fs-4    closenotif" >CLOSED</span>'
                ctr='<button class="btn btn-secondary addfight col-12 fs-2 mb-2  " id="'+result.game_id+'" typ="NEW"  game="'+result.fightid+'" >CREATE NEW FIGHT?</button>'
            }
            
            $('.notif').append(notif)
            $('.controls').append(ctr)
            
            dmeron = $('.dmeron-val').val()
            $('.dmeron_bet').text(result.dmeron)
            $('.dmeron-val').val(result.dmeron)
            
            $('.dmeron_bet').each(function () {
                $(this).prop('Counter',dmeron).animate({
                    Counter: $(this).text()
                }, {
                    
                    //chnage count up speed here
                    duration: 1000,
                    easing: 'swing',
                    step: function (now) {
                        $(this).text(Math.ceil(now).toLocaleString('en'));
                        
                    }
                    
                })
            });
            
            dwala = $('.dwala-val').val()
            $('.dwala_bet').text(result.dwala)
            $('.dwala-val').val(result.dwala)
            
            $('.dwala_bet').each(function () {
                $(this).prop('Counter',dwala).animate({
                    Counter: $(this).text()
                }, {
                    
                    //chnage count up speed here
                    duration: 1000,
                    easing: 'swing',
                    step: function (now) {
                        $(this).text(Math.ceil(now).toLocaleString('en'));
                        
                    }
                    
                })
            });
            
            meron = $('.meron-val').val()
            $('.meron_bet').text(result.meron)
            $('.meron-val').val(result.meron)
            
            $('.meron_bet').each(function () {
                $(this).prop('Counter',meron).animate({
                    Counter: $(this).text()
                }, {
                    
                    //chnage count up speed here
                    duration: 1000,
                    easing: 'swing',
                    step: function (now) {
                        $(this).text(Math.ceil(now).toLocaleString('en'));
                        
                    }
                    
                })
            });
            
            wala = $('.wala-val').val()
            $('.wala_bet').text(result.wala)
            $('.wala-val').val(result.wala)
            
            $('.wala_bet').each(function () {
                $(this).prop('Counter',wala).animate({
                    Counter: $(this).text()
                }, {
                    
                    //chnage count up speed here
                    duration: 1000,
                    easing: 'swing',
                    step: function (now) {
                        $(this).text(Math.ceil(now).toLocaleString('en'));
                        
                    }
                    
                })
            });
            
            draw = $('.draw-val').val()
            $('.draw_bet').text(result.draw)
            $('.draw-val').val(result.draw)
            
            $('.draw_bet').each(function () {
                $(this).prop('Counter',draw).animate({
                    Counter: $(this).text()
                }, {
                    
                    //chnage count up speed here
                    duration: 1000,
                    easing: 'swing',
                    step: function (now) {
                        $(this).text(Math.ceil(now).toLocaleString('en'));
                        
                    }
                    
                })
            });
            
            long = $('.long-val').val()
            $('.long_bet').text(result.longest)
            $('.long-val').val(result.longest)
            
            $('.long_bet').each(function () {
                $(this).prop('Counter',long).animate({
                    Counter: $(this).text()
                }, {
                    
                    //chnage count up speed here
                    duration: 1000,
                    easing: 'swing',
                    step: function (now) {
                        $(this).text(Math.ceil(now).toLocaleString('en'));
                        
                    }
                    
                })
            });
            
            $('.meronpayout').text(result.meronpayout.toFixed(2))
            $('.walapayout').text(result.walapayout.toFixed(2))
            
            // $('.draw_bet').text(result.draw.toFixed(2))
            // $('.long_bet').text(result.long.toFixed(2))
            
            // END MESSAGE
        }
        
        // ////////////////
    })