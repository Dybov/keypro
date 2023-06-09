const map = L.map("map");
const popup = L.popup();
const markers = {};

L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
}).addTo(map);

// Center at Joensuu
map.setView([62.60118, 29.76316], 13);
map.on('click', onMapClick);

// Create markers for each Point
for (const mrkr of points.features) {
    const [long, lat] = mrkr.geometry.coordinates
    createMarkerByParams(mrkr.properties.pk, lat, long, mrkr.properties.owned_by == user_id)
}

/**
 * Event handler for map click that opens popup for Marker creation.
 * @param {Event} e - The click event.
 */
function onMapClick(e) {
    const {lat, lng} = e.latlng;
    popup
        .setLatLng(e.latlng)
        .setContent(`
            <p>You clicked the Map at ${e.latlng.toString()}</p>
            <button onclick="createNewMarker(${lat}, ${lng})">Create Point</button>
        `)
        .openOn(map);
}

let RESPONSE;
/**
 * Create a new Point at backend and Marker in case of success.
 */
async function createNewMarker(latitude, longitude) {
    let response;
    let error_message = "Could not create this Point";
    try {
        response = await fetch('/create/', options={
            method: "POST",
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                latitude: latitude,
                longitude: longitude
            })
        });
    } catch (error) {
        error_message = "Could not create Point because of error " + error;
    }

    if (response && response.ok) {
        let {id} = await response.json();
        RESPONSE = response
        const marker = createMarkerByParams(id, latitude, longitude, true);
        popup.close();
    } else {
        alert(error_message);
    }
}

/**
 * Create a marker on map with the given parameters.
 * @param {string} id - The Point ID.
 * @param {number} latitude - The latitude coordinate.
 * @param {number} longitude - The longitude coordinate.
 * @param {boolean} is_owner - Whether the marker is owned by the user.
 * @returns {Object} The created marker object.
 */
function createMarkerByParams(id, latitude, longitude, is_owner) {
    const icon = L.divIcon({
        iconAnchor: [0, 24],
        labelAnchor: [-6, 0],
        popupAnchor: [0, -36],
        html: `<span class="point point-${ is_owner ? "own" : 'other'}"/>`
    })

    const marker = L.marker([latitude, longitude], {draggable: is_owner, icon: icon}).addTo(map);
    marker.id = id;
    // Save coordinates for rollback
    marker.savedLatLng = marker.getLatLng();
    marker.on('moveend', onMarkerMoveEnd);
    bindMarkerPopup(marker);
    markers[id] = marker;
    return marker;
}

/**
 * Bind a popup with delete button to the marker.
 * @param {Object} marker - The marker object.
 */
function bindMarkerPopup(marker) {
    marker.bindPopup(`
    <div>
        <p>This Point coordinates are ${marker.getLatLng().toString()}</p>
        <button onclick="deleteMarker(${marker.id})">Delete</button>
    </div>`)
}

/**
 * Event handler for marker move end that open popup with save and cancel buttons.
 * @param {Event} e - The moveend
 */
function onMarkerMoveEnd(e) {
    const marker = e.target;
    const position = marker.getLatLng();
    const popupContent = `
    <div>
        <p>You moved the Point from ${marker.savedLatLng.toString()} to ${position.toString()}</p>
        <button onclick="updateMarker(${marker.id})">Save</button>
        <button onclick="cancelMove(${marker.id})">Cancel</button>
    </div>`
    marker.bindPopup(popupContent).openPopup();
    marker.getPopup().on('remove', function () {
        cancelMove(marker.id)
    });
}

/**
 * Update the marker's info after attempt to update the Point at backend 
 * @param {string} id - The marker ID.
 */
async function updateMarker(id) {
    let response;
    let error_message = "You cannot move this point";
    const marker = markers[id];
    // Prevent from dragging until changes applied
    marker.dragging.disable();
    // Prevent from clicking on map
    await new Promise(r => setTimeout(r, 100));
    marker.getPopup().off('remove').setContent("Processing...")

    const position = marker.getLatLng();

    try {
        response = await fetch('/update/' + marker.id + "/", {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                latitude: position.lat,
                longitude: position.lng
            })
        });
    } catch (error) {
        error_message = "Error on request " + error;
    }

    if (response && response.ok) {
        marker.setLatLng(position);
        marker.savedLatLng = position
        bindMarkerPopup(marker);
    } else {
        alert(error_message);
        cancelMove(id);
    }
    marker.dragging.enable();
}

/**
 * Cancel the marker movement and restore its original (saved) position.
 * @param {string} id - The marker ID.
 */
async function cancelMove(id) {
    // Prevent from clicking on map
    await new Promise(r => setTimeout(r, 100));
    const marker = markers[id];
    marker.closePopup();
    marker.setLatLng(marker.savedLatLng);
    bindMarkerPopup(marker);
}

/**
 * Delete a marker with the specified ID.
 * 
 * @param {string} id - The ID of the marker to delete.
 */
async function deleteMarker(id) {

    let response;
    let error_message = "You cannot delete this point";
    const marker = markers[id];
    // Prevent from dragging until changes applied
    marker.dragging.disable();
    // Prevent from clicking on map
    await new Promise(r => setTimeout(r, 100));
    marker.getPopup().off('remove').setContent("Deleting...")

    try {
        response = await fetch('/delete/' + marker.id + "/", {
            method: 'DELETE',
        });
    } catch (error) {
        error_message = "Error on request " + error;
    }

    if (response && response.ok) {
        map.removeLayer(marker)
        delete markers[id]; 
    } else {
        alert(error_message);
        marker.dragging.enable();
        bindMarkerPopup(marker);
    }
}