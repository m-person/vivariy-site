/**
 * Custom application logic
 */

$(document).ready(
    function () {

        // init image gallery on product page
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

    }
);


