//product_details page button configuration

$('#btnCart').click(function (e) { 
    e.preventDefault();
    
    var product_id = $('#pid').val();
    var product_qty = $('#txtQty').val();
    var token = $('input[name=csrfmiddlewaretoken]').val();

    $.ajax({
        method: "POST",
        url: "/addtocart",
        data: {
            'product_id':product_id,
            'product_qty':product_qty,
            csrfmiddlewaretoken:token
        },
        success: function (response) {
            console.log(response)
            alertify.success(response.status)
            //alert(success['status'])
        }
    });
});

$('#Remove_btn').click(function (e) { 
    e.preventDefault();
    var product_id = $('#pid').val();
    var token = $('input[name=csrfmiddlewaretoken]').val();

    $.ajax({
        method: "POST",
        url: "/remove_cart",
        data: {
            'product_id':product_id,
            csrfmiddlewaretoken:token
        },
        success: function (response) {
            console.log(response)
            alertify.success(response.status)
            //alert(success['status'])
            $('.cart_data_refresh_page').load(location.href + ".cart_data_refresh_page");
        }
    });
});

document.addEventListener('DOMContentLoaded',function(event){
    const btnPlus = document.getElementById('btnPlus');
    const btnMinus = document.getElementById('btnMinus');
    const txtQty = document.getElementById('txtQty');

    btnPlus.addEventListener('click',function(){
        let qty = parseInt(txtQty.value,10);
        qty = isNaN(qty)?0:qty;
        if(qty<10){
            qty++;
            txtQty.value = qty;
        }
    });

    btnMinus.addEventListener('click',function(){
        let qty = parseInt(txtQty.value,10);
        qty = isNaN(qty)?0:qty;
        if(qty>1){
            qty--;
            txtQty.value = qty;
        }
    });
});
