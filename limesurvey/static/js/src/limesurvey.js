/* Javascript for LimeSurveyXBlock. */
function LimeSurveyXBlock(runtime, element) {

    function updateCount(result) {
        $('.surveys', element).text(result.surveys);
    }

    var handlerUrl = runtime.handlerUrl(element, 'auth_limesurvey');

    $('p', element).click(function(eventObject) {
        $.ajax({
            type: "POST",
            url: handlerUrl,
            data: JSON.stringify({"status": "Success"}),
            success: updateCount
        });
    });

    $(function ($) {
        /*
        Use `gettext` provided by django-statici18n for static translations

        var gettext = LimeSurveyXBlocki18n.gettext;
        */

        /* Here's where you'd do things on page load. */
    });
}
