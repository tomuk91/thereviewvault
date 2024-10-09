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
        var nextPage = parseInt($('#current-page').val()) + 1;
        var loadMoreUrl = window.location.href.split('?')[0] + '?page=' + nextPage;

        if (scrollPos >= scrollHeight - 200) { // Adjust the threshold as needed
            if ($('#has-more').val() === "True" && !$('#reviews-container').data('loading')) { // Check if there's more content to load and not already loading
                $('#reviews-container').data('loading', true); // Prevent multiple AJAX calls
                $.ajax({
                    url: loadMoreUrl,
                    dataType: 'json',
                    success: function (data) {
                        if (data.html) {
                            $('#reviews-container').append(data.html); // Append new reviews
                            $('#current-page').val(nextPage);
                        }
                        if (!data.has_next) {
                            $('#has-more').val("false");
                        }
                        $('#reviews-container').data('loading', false); // Allow further AJAX calls after success
                    },
                    error: function () {
                        $('#reviews-container').data('loading', false); // Reset loading flag on error
                    }
                });
            }
        }
    }
}, 200)); // Adjust the debounce delay as needed
