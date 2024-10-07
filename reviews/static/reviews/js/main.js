// main.js

// Lazy loading with debounce function
function debounce(func, delay) {
    let debounceTimer;
    return function () {
        const context = this;
        const args = arguments;
        clearTimeout(debounceTimer);
        debounceTimer = setTimeout(() => func.apply(context, args), delay);
    };
}

$(window).on('scroll', debounce(function () {
    // Check if pagination elements exist before executing the logic
    if ($('#current-page').length > 0 && $('#has-more').length > 0) {
        var scrollHeight = $(document).height();
        var scrollPos = $(window).height() + $(window).scrollTop();
        var loadMoreUrl = window.location.href.split('?')[0] + '?page=' + (parseInt($('#current-page').val()) + 1);

        if (scrollPos >= scrollHeight - 200) { // Adjust the threshold as needed
            if ($('#has-more').val() == "True") { // Check if there's more content to load

                $.ajax({
                    url: loadMoreUrl,
                    dataType: 'json',
                    success: function (data) {
                        $('#reviews-container').append(data.html); // Append new reviews
                        $('#current-page').val(parseInt($('#current-page').val()) + 1);
                        if (!data.has_next) {
                            $('#has-more').val("false");
                        }
                    }
                });
            }
        }
    }
}, 200)); // Adjust the debounce delay as needed
