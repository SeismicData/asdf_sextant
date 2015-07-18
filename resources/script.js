var map = L.map('map').setView([0, 0], 0);
var layer = new L.StamenTileLayer("toner");
map.addLayer(layer);



var stations = {};

function addStation(station_id, latitude, longitude) {
    stations[station_id] = {
        "latitude": latitude,
        "longitude": longitude};

    var myIcon = L.divIcon({
        className: 'svg-marker',
        html: '<svg xmlns="http://www.w3.org/2000/svg" version="1.1" style="margin: 0 auto; width: 20px; height:20px;"><polygon style="fill:#98d02e; stroke:#666666; stroke-width:2; stroke-opacity:0.5"points="0,0 20,0 10,20"/></svg>',
        iconSize: L.point(20, 20),
        iconAnchor: L.point(10, 20)
    });

    L.marker([latitude, longitude], {
        icon: myIcon
    }).addTo(map);
}
