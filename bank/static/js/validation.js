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
        } 
        
        if (valid == true) {
            $(".login-form").submit();
        }
    });

});
