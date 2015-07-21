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


var events = {};

function addEvent(event_id, latitude, longitude) {
    var marker = new L.CircleMarker(
        L.latLng(latitude, longitude), {
            radius: 10,
            color: "#ff0000"
    });
    map.addLayer(marker);


    events[event_id] = {
        "marker": marker,
        "latitude": latitude,
        "longitude": longitude};

    marker.status = "--";
    setMarkerInactive({marker: marker});
}


function setMarkerActive(value) {
    if (value.marker.status != "active") {
        var pos = map.latLngToLayerPoint(value.marker.getLatLng()).round();
        value.marker.setStyle({color: "#DB3340"});
        value.marker.setZIndexOffset(101 - pos.y);
        value.marker.status = "active";
    }
}


function setMarkerInactive(value) {
    if (value.marker.status != "passive") {
        var pos = map.latLngToLayerPoint(value.marker.getLatLng()).round();
        value.marker.setStyle({color: "#659872"});
        value.marker.setZIndexOffset(100 - pos.y);
        value.marker.status = "passive";
    }
}


function setAllInactive() {
    _.forEach(events, function(value, key) {
        setMarkerInactive(value);
    });
}


function highlightEvent(event_id) {
    setAllInactive();
    var value = events[event_id];
    setMarkerActive(value)
}
