$(document).ready(function() {

    $('#password-clear').show();
    $('#id_password').hide();

    $('#password-clear').focus(function() {
        $('#password-clear').hide();
        $('#id_password').show();
        $('#id_password').focus();
    });
    $('#id_password').blur(function() {
        if($('#id_password').val() == '') {
            $('#password-clear').show();
            $('#id_password').hide();
        }
    });
    /* Defaults inputs */
    $('.accounts-register-form-field').each(function() {
        var default_value = this.value;
        $(this).focus(function() {
            if(this.value == default_value) {
                this.value = '';
            }
        });
        $(this).blur(function() {
            if(this.value == '') {
                this.value = default_value;
            }
        });
    });

    $('.evento-date-form-field').each(function() {
        var default_value = this.value;
        $(this).focus(function() {
            if(this.value == default_value) {
                this.value = '';
            }
        });
        $(this).blur(function() {
            if(this.value == '') {
                this.value = default_value;
            }
        });
    });

    $('.header-seach-form-field').each(function() {
        var default_value = this.value;
        $(this).focus(function() {
            if(this.value == default_value) {
                this.value = '';
            }
        });
        $(this).blur(function() {
            if(this.value == '') {
                this.value = default_value;
            }
        });
    });

    $('.comment-text-add').each(function() {
        var default_value = this.value;
        $(this).focus(function() {
            if(this.value == default_value) {
                this.value = '';
            }
        });
        $(this).blur(function() {
            if(this.value == '') {
                this.value = default_value;
            }
        });
    });
});
