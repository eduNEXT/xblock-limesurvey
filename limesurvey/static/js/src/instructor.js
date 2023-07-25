$(function () {

    const cssUrl = "https://cdn.jsdelivr.net/npm/@edx/paragon@20.45.5/dist/paragon.min.css";

    $('<link>').attr({
        href: cssUrl,
        rel: "stylesheet"
    }).appendTo('head');

    $('.limesurvey-instructor-wrapper').hide();
    $('.admin-panel').click(function (e) {
        e.preventDefault();
        $('.limesurvey-instructor-wrapper').show();
        const url = $(this).attr('href');
        $('.limesurvey-instructor-wrapper').append(`
            <a href="" class="go-back">← Back</a>
            <div>
                <iframe
                    class="limesurvey-admin-iframe"
                    frameborder="0"
                    src="${url}">
                </iframe>
            </div>
        `);
        $('.paragon-styles').hide();
        $('.go-back').click(function (e) {
            e.preventDefault();
            $('.paragon-styles').show();
            $('.limesurvey-instructor-wrapper').html('');
            $(this).hide();
        });
    })
});
