


$('.single-post-link').click( function(e) {
    var item_id = e.target.id;
    var clicked_items = Cookies.get('clicked_items') ? Cookies.get('clicked_items') : '';
    Cookies.set('clicked_items', clicked_items + item_id + ',');
    return true;
} );
