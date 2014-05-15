var cart = {};
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        var i;
        for (i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
};
var csrftoken = getCookie('csrftoken');
cart.add = function(el, content_type_id, object_id, price){
    var quantity = $('.count-product').val();

    if (quantity == null){
        quantity = 1;
    }
	var event = jQuery.Event("before_add.basket");
	event.el= el;
	$(document).trigger(event);

	$.ajax({
		'type': 'POST',
		'url': cart.add_url,
		'data': {
            'add':true,
            'csrfmiddlewaretoken': csrftoken,
			'content_type': content_type_id,
			'object_id': object_id,
            'quantity':quantity
		},
		'dataType': 'json',
		'success': function(data, textStatus) {
//            console.log(data);
//            console.log(textStatus);
			var event = jQuery.Event("add_success.basket");
			event.el = el;
            console.log(el);
			event.status = textStatus;
			$(document).trigger(event, data);
             $('#table-cart').html(data.html);
		},
		'error': function(XMLHttpRequest, textStatus, errorThrown) {
			var event = jQuery.Event("add_error.basket");
			event.el = el;
			event.request = XMLHttpRequest;
			event.status = textStatus;
			$(document).trigger(event, errorThrown);
		}}
	);
	return false;
};
cart.update = function(el, item_id, quantity){
//    var variant=$('#variants').find('select option').filter(":selected").text();
//    var name = el.parent('.pro-list-count').find('.count-product');
//    console.log(name);
//    var quantity = $(name).val();
//    console.log('quantity',quantity);
    if (!quantity){
        quantity = 1;
    }
	var event = jQuery.Event("before_add.basket");
	event.el= el;
	$(document).trigger(event);

	$.ajax({
		'type': 'POST',
		'url': cart.upd_url,
		'data': {
            'update':true,
            'csrfmiddlewaretoken': csrftoken,
//			'content_type': content_type_id,
//			'object_id': object_id,
            'item_id':item_id,
            'quantity':quantity
		},
		'dataType': 'json',
		'success': function(data, textStatus) {
			var event = jQuery.Event("add_success.basket");
			event.el = el;
			event.status = textStatus;
			$(document).trigger(event, data);
//            $('table.shopping-cart').html(data.html);
             $('#table-cart').html(data.html);
		},
		'error': function(XMLHttpRequest, textStatus, errorThrown) {
			var event = jQuery.Event("add_error.basket");
			event.el = el;
			event.request = XMLHttpRequest;
			event.status = textStatus;
			$(document).trigger(event, errorThrown);
		}}
	);
	return false;
};

cart.del = function(el, item_id) {
//cart.del = function(el, content_type_id, object_id, item_id) {
	var event = jQuery.Event("before_del.basket");
	event.el= el;
	this.do_delete = true;
	$(document).trigger(event);
	
	if (this.do_delete) {
		$.ajax({
			'type': 'POST',
			'url': cart.del_url,
			'data': {
                'remove':true,
                'csrfmiddlewaretoken': csrftoken,
                'item_id':item_id
//				'content_type': content_type_id,
//				'object_id': object_id
			},
			'dataType': 'json',
			'success': function(data, textStatus) {
				var event = jQuery.Event("del_success.basket");
				event.el = el;
				event.status = textStatus;
				$(document).trigger(event, data);
//                $('.block-cart').html(data.panel_html);
//                $('table.shopping-cart').html(data.html);
                $('#table-cart').html(data.html);
			},
			'error': function(XMLHttpRequest, textStatus, errorThrown) {
				var event = jQuery.Event("del_error.basket");
				event.el = el;
				event.request = XMLHttpRequest;
				event.status = textStatus;
				$(document).trigger(event, errorThrown);
			}}
		);
	}
	return false;
}

$('html').ajaxSend(function(event, xhr, settings) {
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            var i;
            for (i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
        // Only send the token to relative URLs i.e. locally.
        xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
    }
});
