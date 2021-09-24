var input = document.getElementById("input-name");
var display = document.getElementById("card-owner");

input.addEventListener("keydown", function(e){
    display.innerHTML = input.value;
})