/**
 * Custom application logic
 */

$(document).ready(
    function () {

        // init image gallery on product page
        var product_gallery = $("#product-gallery");
        if (product_gallery.length) {
            product_gallery.lightSlider({
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


        //init tabbed navigation on product page
        //var product_tabs = $(".product_tabs a");
        //if (product_tabs.length) {
        //    product_tabs.click(function(evt) {
        //        alert('OO');
        //        evt.preventDefault();
        //        $(this).tab('show');
        //    });
        //}
    }
);

