/* Javascript for LimeSurveyXBlock. */
function LimeSurveyXBlock(runtime, element) {

    $(element).find('.save-button').bind('click', function() {
        var handlerUrl = runtime.handlerUrl(element, 'studio_submit');
        var data = {
            display_name: $(element).find('input[name=limesurvey_display_name]').val(),
            survey_id: $(element).find('input[name=limesurvey_survey_id]').val(),
            limesurvey_url: $(element).find('input[name=limesurvey_url]').val(),
            anonymous_survey: Number($(element).find('select[name=limesurvey_anonymous_survey]').val()),
            open_access_mode: Number($(element).find('select[name=limesurvey_open_access_mode]').val()),
        };
        $.post(handlerUrl, JSON.stringify(data)).done(function(response) {
          window.location.reload(false);
        });
      });

    $(element).find('.cancel-button').bind('click', function() {
        runtime.notify('cancel', {});
    });
}
