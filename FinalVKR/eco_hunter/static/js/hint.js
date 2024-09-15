$(document).ready(function () {
    var token = '4a2976e0520ddf4f107a0546009db5772a0de0d4'
    $(".address").suggestions({
        token: token,
        type: "ADDRESS",
        count: 5,
        addon: "none",

        onSelect: function(suggestion) {
            console.log(suggestion);
            var geo_lat = suggestion.data.geo_lat; 
            var geo_lon = suggestion.data.geo_lon; 
            console.log(geo_lat, geo_lon);
            $('#latitude').val(geo_lat);
            $('#longitude').val(geo_lon);      
        }
    });   
});
