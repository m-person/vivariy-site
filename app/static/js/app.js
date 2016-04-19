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
        catalogCategoryPanel.on('shown.bs.collapse', updateMainChildrenHeight);
        catalogCategoryPanel.on('show.bs.collapse', categoryPanelShow);
        catalogCategoryPanel.on('hide.bs.collapse', categoryPanelHide);
        $('.product-ask-btn').on('click', addToCart);
        $('.cart-item-remove-btn').on('click', delFromCart);

        expandCurrentCategory();

    }
);

$(window).load(function () {
    // set up gray backgrounds
    setMainBlockHeight();
    setSideBkgWidth();
    $(window).resize(setMainBlockHeight);
    $(window).resize(setSideBkgWidth);
});


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
function addToCart(evt) {
    evt.preventDefault();
    $.post(window.location.pathname,
        {},
        function (data, textStatus) {
            if (data['result'] != 'ok') {
                popup('Ошибка добавления товара в запрос.', 'error');
            } else {
                //popup('Товар добавлен.', 'success');
                update_cart();
                $(evt.target).addClass("disabled");
            }
        }).fail(function (err) {
        popup('Ошибка добавления товара в запрос.', 'error');
    });
}


/**
 * remove items from request cart using ajax
 * product identifier take from 'data-slug' attribute
 */
function delFromCart(evt) {
    evt.preventDefault();
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
            update_cart();
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
    var height = $('main').height(),
        article_tags_panel = $('.article-tags-panel'),
        contacts_div = $('.contacts-page div.contacts');

    if ($(window).width() >= 992) {
        contacts_div.height(height);
        $('.aside-bkg').height(height);
        article_tags_panel.height(height);
    } else {
        $('.aside-bkg').height(0);
        if (article_tags_panel.length) {
            article_tags_panel.height(article_tags_panel.find('div')[0].scrollHeight + 300);
        }
        if (contacts_div.length) {
            contacts_div.height(contacts_div.find('div')[0].scrollHeight + 60);
        }
    }
    if ($(window).width() >= 768) {
        $('.catalog-aside').height(height);
    }
}

/*
 * set width for side background element '.aside-bkg' (it fills empty space on some pages)
 */
function setSideBkgWidth() {
    var bkg = $('.aside-bkg');
    if (!bkg.length) {
        return
    }
    if ($(window).width() < 992) {
        bkg.width(0); // we need a side background only on wide screens
        return;
    }

    if (location.pathname.indexOf('/catalog/') >= 0) {
        var catalog_menu = $('.catalog-aside');
        bkg.width(catalog_menu.offset().left + 10);
    }

    if (location.pathname.indexOf('/articles/') >= 0) {
        var side_menu = $('.article-tags-panel');
        bkg.width(window.innerWidth - side_menu.offset().left - 40);
    }

    if (location.pathname.indexOf('/contacts/') >= 0) {
        bkg.width(window.innerWidth / 2 - 20);
    }
}


function categoryPanelShow() {
    var panel_id = $(this).attr('id');
    Cookies.set('current_category', panel_id);

    // allow to open only one category at a time
    $('.catalog-category .collapse').collapse('hide');

    $(this).find('.glyphicon').removeClass('glyphicon-plus-sign').addClass('glyphicon-minus-sign');

    $(this).parents().find('.panel-heading h3').removeClass('active');
    $(this).find('.panel-heading h3').addClass('active');
}

function categoryPanelHide() {
    var panel_id = $(this).attr('id');

    if (panel_id == Cookies.get('current_category')) {
        Cookies.set('current_category', null);
    }

    $(this).find('.glyphicon').removeClass('glyphicon-minus-sign').addClass('glyphicon-plus-sign');

    $(this).find('.panel-heading h3').removeClass('active');
    $(this).parents().find('.panel-heading h3').removeClass('active');
}

/*
 * expands last selected category panel in catalog
 */
function expandCurrentCategory() {
    if (location.pathname.indexOf('/catalog/') == -1) {
        return
    }
    var current_category = Cookies.get('current_category'),
        panel = $('#' + current_category);
    console.log(current_category, panel);
    if (panel) {
        console.log(panel.find('a.collapse'));
        panel.find('.collapse').collapse('show');
    }
}

/*
 * update request cart representation (visibility & items count)
 */
function update_cart() {
    var cart = $('.request-basket-btn'),
        count_elem = cart.find('span:last-of-type');

    $.get('/xhr/cart_count/', function (data) {
        if (data == 0) {
            cart.addClass('hidden');
        } else {
            cart.removeClass("hidden");
            count_elem.html("(" + data + ")");
        }
    })
}

