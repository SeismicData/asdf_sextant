var map = L.map('map').setView([0, 0], 0);
var layer = new L.StamenTileLayer("toner");
map.addLayer(layer);

var activeIcon = L.divIcon({
    className: 'svg-marker',
    html: '<svg xmlns="http://www.w3.org/2000/svg" version="1.1" style="margin: 0 auto; width: 20px; height:20px;"><polygon style="fill:#3D8EC9; stroke:#666666; stroke-width:2; stroke-opacity:0.5"points="0,0 20,0 10,20"/></svg>',
    iconSize: L.point(20, 20),
    iconAnchor: L.point(10, 20)
});

var passiveIcon = L.divIcon({
    className: 'svg-marker',
    html: '<svg xmlns="http://www.w3.org/2000/svg" version="1.1" style="margin: 0 auto; width: 20px; height:20px;"><polygon style="fill:#999999; stroke:#666666; stroke-width:2; stroke-opacity:0.5"points="0,0 20,0 10,20"/></svg>',
    iconSize: L.point(20, 20),
    iconAnchor: L.point(10, 20)
});


var stations = {};

function addStation(station_id, latitude, longitude) {
    var marker = L.marker([latitude, longitude], {
        icon: passiveIcon
    }).addTo(map);

    stations[station_id] = {
        "marker": marker,
        "latitude": latitude,
        "longitude": longitude};
}


function setMarkerActive(value) {
    var pos = map.latLngToLayerPoint(value.marker.getLatLng()).round();
    value.marker.setIcon(activeIcon);
    value.marker.setZIndexOffset(101 - pos.y);
}


function setMarkerInactive(value) {
    var pos = map.latLngToLayerPoint(value.marker.getLatLng()).round();
    value.marker.setIcon(passiveIcon);
    value.marker.setZIndexOffset(100 - pos.y);
}


function setAllInactive() {
    _.forEach(stations, function(value, key) {
        setMarkerInactive(value);
    });
}


function highlightNetwork(network_id) {
    _.forEach(stations, function(value, key) {
        if (_.startsWith(key, network_id + '.')) {
            setMarkerActive(value)
        }
        //else {
            //setMarkerInactive(value)
        //}
    });
}

function highlightStation(station_id) {
    var value = station[station_id];
    setMarkerActive(value)

