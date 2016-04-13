$(document).ready(
    function () {

        // init image gallery plugin on product page
        var productGallery = $("#product-gallery");
        if (productGallery.length) {
            productGallery.lightSlider({
                gallery: true,
                item: 1,
                loop: true,
                thumbItem: 5,
                slideMargin: 1,
                enableDrag: true,
                currentPagerPosition: 'left',
                slideMove: 1,
                useCSS: true,
                mode: 'slide',
                controls: true,
                galleryMargin: 1,
                thumbMargin: 1
            });
        }


        var csrftoken = getCookie('csrftoken');
        $.ajaxSetup({
            beforeSend: function (xhr, settings) {
                if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                }
            }
        });


        var catalogCategoryPanel = $('.catalog-category .panel');
        setMainBlockHeight();
        $(window).resize(setMainBlockHeight);
        catalogCategoryPanel.on('shown.bs.collapse', updateMainChildrenHeight);
        catalogCategoryPanel.on('show.bs.collapse', categoryPanelShow);
        catalogCategoryPanel.on('hide.bs.collapse', categoryPanelHide);
        $('.product-ask-btn').on('click', addToCart);
        $('.cart-item-remove-btn').on('click', delFromCart);
    }
);


/**
 * dynamically create notification popup with autohiding in 5sec.
 * @param: msg: message to show
 * @param: type=success|info|warning|error: message type
 */
function popup(msg, type) {
    var alert_type = type || 'error';
    alert_type = 'alert-' + alert_type;
    $('body').append('<div id="alert-popup" class="alert ' + alert_type + ' alert-dismissible fade in" role="alert">\
                      <button type="button" class="close" data-dismiss="alert" aria-label="Close">\
                      <span aria-hidden="true">&times;</span></button>' + msg + '</div>');
    setTimeout(function () {
        $('#alert-popup').remove();
    }, 5000);
}


/**
 * add items to request cart via ajax
 * product identifier is taken from current page url
 */
function addToCart() {
    $.post(window.location.pathname,
        {},
        function (data, textStatus) {
            if (data['result'] != 'ok') {
                popup('Ошибка добавления товара в запрос.', 'error');
            } else {
                popup('Товар добавлен.', 'success')
            }
        }).fail(function (err) {
        popup('Ошибка добавления товара в запрос.', 'error');
    });
}


/**
 * remove items from request cart using ajax
 * product identifier take from 'data-slug' attribute
 */
function delFromCart() {
    var self = $(this);

    $.ajax({
        url: '/products/' + self.data('slug'),
        method: 'DELETE',
        success: function (data, status, xhr) {
            if (data['result'] != 'ok') {
                popup('Ошибка удаления товара из списка.', 'error');
                return
            }

            self.parents('li.cart-item').remove();

            if (!$('.cart-placeholder .cart-item').length) {
                var cp = $('.cart-placeholder');
                cp.empty();
                cp.append('<div class="cart-empty-msg">Список пуст.<br>Добавить товар к запросу можно на странице товара в каталоге.</div>');
            }
        },
        error: function (xhr, status, error) {
            popup('Ошибка удаления товара из списка.', 'error');
        }
    });
}


/**
 * retrieve cookie by its name. Copy-paste from django docs
 */
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

/**
 * these HTTP methods do not require CSRF protection
 */
function csrfSafeMethod(method) {
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}


/**
 * set height for content block.
 * It's called when page loaded or window resized.
 * I use js because I'm give up to implement using css the following: footer, flushed to bottom and fixed-width bootstraps
 *   containers with some columns, that expands to screen edge. Note: it's easy to do with flexbox, but old IE doesn't support it.
 */
function setMainBlockHeight() {
    var footerHeight = $('footer').outerHeight(),
        headerHeight = $('header').outerHeight(),
        viewportHeight = $(window).height(),
        mainBlock = $('main'),
        contentHeight = viewportHeight - footerHeight - headerHeight;

    mainBlock.css("minHeight", contentHeight);
    updateMainChildrenHeight();
}

/**
 * set height of side menus and its backgrounds.
 * call it every time the "main" block height changed
 */
function updateMainChildrenHeight() {
    var height = $('main').height();

    $('.aside-bkg').height(height);
    $('.catalog-aside').height(height);
    $('.article-tags-panel').height(height);
}

function categoryPanelShow() {
    $(this).parents().find('.panel-heading h3').removeClass('active');
    $(this).find('.panel-heading h3').addClass('active');
}

function categoryPanelHide() {
    $(this).find('.panel-heading h3').removeClass('active');
    $(this).parents().find('.panel-heading h3').removeClass('active');
}

