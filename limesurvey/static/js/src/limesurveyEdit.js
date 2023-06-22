/* Javascript for LimeSurveyXBlock. */
function LimeSurveyXBlock(runtime, element) {

    $(element).find('.save-button').bind('click', function() {
        var handlerUrl = runtime.handlerUrl(element, 'studio_submit');
        var data = {
            display_name: $(element).find('input[name=limesurvey_display_name]').val(),
            survey_id: $(element).find('input[name=limesurvey_survey_id]').val(),
        };
        $.post(handlerUrl, JSON.stringify(data)).done(function(response) {
          window.location.reload(false);
        });
      });

    $(element).find('.cancel-button').bind('click', function() {
        runtime.notify('cancel', {});
    });
}
