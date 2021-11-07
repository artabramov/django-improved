window.onload = function() {

    // remove product from the cart
    $('.basket-list').on('click', 'input[type="number"]', function(event) {
        let t_href = event.target;

        $.ajax({
            url: '/baskets/edit/' + t_href.name + '/' + t_href.value + '/',
            success: function(data) {
                $('.basket-list').html(data.result)
            },
            error: function(xhr, status, error) {
                console.log(error)
            },
        });
    });
    
    // add product to the cart
    $('.card-footer a').click(function(event) {
        event.preventDefault();
        let t_href = event.target;
        let product_id = t_href.getAttribute('data-id')

        $.ajax({
            url: '/baskets/add/' + product_id + '/',
            success: function(data) {
                console.log('success')
            },
            error: function(xhr, status, error) {
                console.log(error)
            },
        });
    });
}