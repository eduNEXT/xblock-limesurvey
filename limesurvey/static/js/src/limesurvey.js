/* Javascript for LimeSurveyXBlock. */
function LimeSurveyXBlock(runtime, element) {

    function setUrl(result) {
        $('.access-code', element).text(result.access_code);
        $('.survey-url', element).text(result.survey_url);
        $('.survey-url', element).attr('href', result.survey_url);
        $('.survey-iframe', element).attr('src', result.survey_url);
    }

    var handlerUrl = runtime.handlerUrl(element, 'get_survey');

    $('.get-survey-button', element).click(function(eventObject) {
        $.ajax({
            type: "POST",
            url: handlerUrl,
            data: JSON.stringify({"result": "success"}),
            success: setUrl
        });
    });
}
