var map = L.map('map').setView([0, 0], 0);
var layer = new L.StamenTileLayer("toner");
map.addLayer(layer);

var events = {};

function addEvent(event_id, latitude, longitude) {
    var marker = new L.CircleMarker(
        L.latLng(latitude, longitude), {
            radius: 10,
            color: "#ff0000"
    });
    marker.status = "--";
    map.addLayer(marker);

    events[event_id] = {
        "marker": marker,
        "latitude": latitude,
        "longitude": longitude};

    setMarkerInactive({marker: marker});
}


function removeAllEvents() {
    _.forEach(events, function(value, key) {
        map.removeLayer(value.marker);
    });
    events = {};
}


function setMarkerActive(value) {
    if (value.marker.status != "active") {
        value.marker.setStyle({color: "#DB3340"});
        value.marker.status = "active";
    }
}


function setMarkerInactive(value) {
    if (value.marker.status != "passive") {
        value.marker.setStyle({color: "#659872"});
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
