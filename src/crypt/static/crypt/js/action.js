$(document).ready(function () {
    let text_input = $('textarea');
    text_input.hide();
    text_input.removeAttr('required');

    $('select').change(function () {
        if ($(this).val() === "encryption") {
            text_input.show().prop('required', true);
        } else {
            text_input.hide().removeAttr('required');
        }
    });

});