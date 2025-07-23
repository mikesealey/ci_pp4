$(document).ready(function(){
    $("#hide_out_of_stock").on("change", function(){
        $(this).closest("form").submit()
    })
    $("#sorting").on("change", function(){
        $(this).closest("form").submit()
    })
})