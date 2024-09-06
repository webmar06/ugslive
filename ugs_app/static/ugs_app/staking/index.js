$(document).on('click','.stake_btn',function(){
    var typ=$(this).attr('id')
    var rate=$(this).attr('rate')

    $('.stake_name').val(typ)
    $('.stake_rate').val(rate)
    $('#stake_modal').modal('show')
})


$('#stake_frm').on('submit',function(e){
    e.preventDefault()
    data=$(this).serializeArray()

    $.ajax({
        method:'POST',
        url:'save_stake',
        data:data,
        success:function(res){
            console.log(res)
        }
    })
})