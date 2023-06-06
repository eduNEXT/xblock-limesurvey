/* Javascript for LimeSurveyXBlock. */
function LimeSurveyXBlock(runtime, element) {

    function setUrl(result) {
        $('.survey-url', element).text(result.survey_url);
        $('.survey-url', element).attr('href', result.survey_url);
        $('.access-code', element).text(result.access_code);
    }

    var handlerUrl = runtime.handlerUrl(element, 'get_survey_url');

    $('.get-survey-button', element).click(function(eventObject) {
        $.ajax({
            type: "POST",
            url: handlerUrl,
            data: JSON.stringify({"result": "success"}),
            success: setUrl
        });
    });
}
