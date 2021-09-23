$(document).ready(function () {

    $("#login-btn").click(function (e) {
        e.preventDefault();
        var username = $("#username").val();
        var password = $("#crn").val();
        var valid = true;

        $(".error").remove();

        if (username.length < 1) {
            $("#username").before(
                '<span class="error">Username is required</span>'
            );
            valid = false;
        }
        
        if (password.length < 1) {
            $("#crn").before(
                '<span class="error">CRN is required</span>'
            );
            valid = false;
        } else {
            var CRNRegex = /^[0-9]+$/;
            var validBottomPhone = CRNRegex.test(password);
            if (!validBottomPhone) {
                $("#crn").before('<span class="error">Enter a valid CRN</span>');
                valid = false;
            }
        }
        
        if (password.length > 8) {
            $("#crn").before(
                '<span class="error">CRN is 8-digit number</span>'
            );
            valid = false;
        }

        
        if (valid == true) {
            $(".login-form").submit();
        }
    });

    // account-no-btn
    $("#account-no-btn").click(function (e) {
        e.preventDefault();
        var accountno = $("#accountno").val();
        var valid = true;
        $(".error").remove();

        if (accountno.length < 1) {
            $("#accountno").before(
                '<span class="error">Account no is required</span>'
            );
            valid = false;
        }
        if (accountno.length > 10) {
            $("#accountno").before(
                '<span class="error">Enter valid account no</span>'
            );
            valid = false;
        }

        if (valid == true) {
            $(".account_no-form").submit();
        }
    });

});
