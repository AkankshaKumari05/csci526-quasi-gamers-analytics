function onload(){
    $(document).keydown(function(event) {
        if ($("#searchText").is(":focus") && (event.key === 13 || event.key == "Enter")) {
            getStockDetails();
        }
    });
    $("#searchText").val('');
}

