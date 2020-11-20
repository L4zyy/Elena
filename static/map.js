var isPath = document.getElementById('isPath').getAttribute('d');
/**
 * @type {dictionary}
 */
var mapOptions
/**
 * @type {boolean}
 */
var startSelected = false;
/**
 * @type {boolean}
 */
var endSelected = false;
/**
 * Creating map options
 */
if (isPath == 'true'){
    mapOptions = {
    center: [Number(document.getElementById('mapcenter1').getAttribute('d')), Number(document.getElementById('mapcenter2').getAttribute('d'))],
    zoom: Number(document.getElementById('zoom1').getAttribute('d'))
    } 
    document.getElementById("startlocation").value = document.getElementById('cacheStart').getAttribute('d');
    document.getElementById("endlocation").value = document.getElementById('cacheEnd').getAttribute('d');
    startSelected = true;
    endSelected = true;
}else{
    mapOptions = {
    center: [42.378076, -72.519946],
    zoom: 16
}
}

/**
 * @type {<Map|LayerGroup> map}
 */
var map = new L.map('map', mapOptions);
var line = null;

/**
 * @type {<Layer> layer}
 */
var layer = new L.TileLayer('http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png');

/**
 * Adding layer to the map
 */
map.addLayer(layer);
/**
 * enable the mousemove interaction
 */
map.addEventListener('mousemove', function(ev) {
    document.getElementById("mapcenter").value = map.getCenter().toString();
    document.getElementById("zoom").value = map.getZoom().toString();
});
/**
 * enable the wheel interaction
 */
map.addEventListener('wheel', function(ev) {
    document.getElementById("mapcenter").value = map.getCenter().toString();
    document.getElementById("zoom").value = map.getZoom().toString();
});
/**
 * enable the mapcenter interaction
 */
document.getElementById("mapcenter").value = map.getCenter().toString();
/**
 * enable the zoom
 */
document.getElementById("zoom").value = map.getZoom().toString();
/**
 * @type {marker}
 */
var popup = L.popup();
/**
 * @type {number}
 */
var count = 0; 
/**
 * @type {marker}
 */
var but1 = null; 
/**
 * @type {marker}
 */
var but2 = null; 

/**
 * @type {icon}
 */
var greenIcon = new L.Icon({
  iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-red.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
  iconSize: [25, 41],
  iconAnchor: [12, 41],
  popupAnchor: [1, -34],
  shadowSize: [41, 41]
});

/**
 * onMapClick(e) will display the coordinate of the clicked location and add maarkers in the location. 
 * There will be only two marker in the map, which is the start and end. Therefore, after the second click, 
 * onMapClick(e) will clear the end marker and add end marker to the new location. 
 * 
 * @param {string} e - The click action
 *
 */
function onMapClick(e) { 
    document.getElementById("mapcenter").value = map.getCenter().toString();
    document.getElementById("zoom").value = map.getZoom().toString();

    popup
        .setLatLng(e.latlng)
        .setContent("You clicked the map at " + e.latlng.toString())
        .openOn(map);
        
    if (e.latlng['lat'] > 42.428183|| e.latlng['lat'] < 42.305842 || e.latlng['lng'] < -72.540402 ||e.latlng['lng'] > -72.466113) {
        window.alert("The location you selected is outside of Amherst area. Please reselect it. ");
    }
    
    else if (startSelected == false){ 
        but1 = L.marker(e.latlng).addTo(map);
        but1.addTo(map);
        document.getElementById("startlocation").value = e.latlng.toString();
        startSelected = true;
    }
    else{ 
        if (endSelected == true){
            map.removeLayer(but2)
        }
        but2 = L.marker(e.latlng, {icon: greenIcon}).addTo(map);
        but2.addTo(map);
        document.getElementById("endlocation").value = e.latlng.toString();
        endSelected = true;
    }
}

/**
 * reselect() will clear all the marker and start and end location on the map. 
 *
 */
function reselect(){
    startSelected = false;
    endSelected = false;
    document.getElementById("startlocation").value = "";
    document.getElementById("endlocation").value = "";
    
    if (but1 != null){
        map.removeLayer(but1)
        but1 = null
    }
    if (but2 != null){
        map.removeLayer(but2)
        but2 = null
    }

    if (line != null){
        map.removeLayer(line);
        line = null
    }
}

map.on('click', onMapClick);

/**
 * connectTheDots(path) will connect the dots based on given path array. 
 * 
 * @param {int[]} path - a int[] to restore all the dots on the map. 
 *
 */
function connectTheDots(path){
    var c = [];
    for(i in path) {
        var x = path[i]['lat'];
        var y = path[i]['lng'];
        c.push([x, y]);
    }
    return c;
}

if (isPath == 'true'){
    var path = document.getElementById('path').getAttribute('d');
    var pathList = JSON.parse(path);
    coords = connectTheDots(pathList);
    line = L.polyline(coords).addTo(map);

    document.getElementById("topnavbar3").style.display=""
}
else{
    document.getElementById("topnavbar3").style.display="none"
}


/**
 * backToOrigin() will return the map to the center of Amherst. 
 */
function backToOrigin(){
    map.setView([42.378076, -72.519946], 16);
}