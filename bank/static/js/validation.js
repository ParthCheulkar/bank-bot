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

    $('#amount_transfer_money').keypress(function (event) {
        var keycode = event.which;
        if (!(event.shiftKey == false && (keycode == 46 || keycode == 8 || keycode == 37 || keycode == 39 || (keycode >= 48 && keycode <= 57)))) {
            event.preventDefault();
        }

        if ($('#amount_transfer_money').val().length >= 10) {
            event.preventDefault();
        }

    });

    $("#transfer-money-btn").click(function (e) {
        e.preventDefault();
        var rname = $("#rname").val();
        var accountno = $("#accountno").val();
        var amount = $("#amount_transfer_money").val();
        var remark = $("#remark").val();
        var valid = true;
        $(".error").remove();

        if (accountno.length < 1)
        {
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

        if (rname.length < 1) {
            $("#rname").before(
                '<span class="error">This field is required</span>'
            );
            valid = false;
        }

        if (amount.length < 1) {
            $("#amount_transfer_money").before(
                '<span class="error">Please enter amount</span>'
            );
            valid = false;
        }
        if (remark.length < 1) {
            $("#remark").before(
                '<span class="error">Enter reason for transaction</span>'
            );
            valid = false;
        }
        
        if (valid == true) {
            $(".transfer-money-form").submit();
        }
    });


});
