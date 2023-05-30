var map = L.map("map");
L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
}).addTo(map);

// Center at Joensuu
map.setView([62.60118, 29.76316], 13);


var popup = L.popup();

function onMapClick(e) {
    popup
        .setLatLng(e.latlng)
        .setContent("You clicked the MAP at " + e.latlng.toString())
        .openOn(map);
}

function onMarkerClick(e) {
    popup
        .setLatLng(e.latlng)
        .setContent("You clicked the MARKER at " + e.latlng.toString())
        .openOn(map);
}

map.on('click', onMapClick);


var marker = L.marker([62.60118, 29.76316], {draggable: true}).addTo(map);
marker.on('click', onMarkerClick);
