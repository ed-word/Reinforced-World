var map;
var directionDisplay;
var directionsService;
var stepDisplay;
var markerArray = [];
var position;
var marker = null;
var polyline = null;
var poly2 = null;
var speed = 0.000005, wait = 1;
var infowindow = null;

var myPano;
var panoClient;
var nextPanoId;
var timerHandle = null;

function createMarker(latlng, label, html) {
    // alert("createMarker("+latlng+","+label+","+html+","+color+")");
    var contentString = '<b>' + label + '</b><br>' + html;
    var marker = new google.maps.Marker({
        position: latlng,
        map: map,
        title: label,
        zIndex: Math.round(latlng.lat() * -100000) << 5,
        icon: '/static/images/truck2.png',
    });
    marker.myname = label;
    // gmarkers.push(marker);

    google.maps.event.addListener(marker, 'click', function () {
        infowindow.setContent(contentString);
        infowindow.open(map, marker);
    });
    return marker;
}


function initialize() {
    infowindow = new google.maps.InfoWindow(
        {
            size: new google.maps.Size(150, 50)
        });
    // Instantiate a directions service.
    directionsService = new google.maps.DirectionsService();

    // Create a map and center it on Manhattan.
    var myOptions = {
        zoom: 13,
        mapTypeId: google.maps.MapTypeId.ROADMAP
    }
    map = new google.maps.Map(document.getElementById("map_canvas"), myOptions);

    address = 'London, UK'
    geocoder = new google.maps.Geocoder();
    geocoder.geocode({ 'address': address }, function (results, status) {
        map.setCenter(results[0].geometry.location);
    });

    // Create a renderer for directions and bind it to the map.
    var rendererOptions = {
        map: map
    }

    directionsDisplay = new google.maps.DirectionsRenderer(rendererOptions);

    // Instantiate an info window to hold step text.
    stepDisplay = new google.maps.InfoWindow();

    polyline = new google.maps.Polyline({
        path: [],
        strokeColor: '#FF0000',
        strokeWeight: 3
    });

    poly2 = new google.maps.Polyline({
        path: [],
        strokeColor: '#000000',
        strokeWeight: 3
    });
}



var steps = []

function calcRoute(start, end) {

    if (timerHandle) { clearTimeout(timerHandle); }
    if (marker) { marker.setMap(null); }

    polyline.setMap(null);
    poly2.setMap(null);
    directionsDisplay.setMap(null);

    polyline = new google.maps.Polyline({
        path: [],
        strokeColor: '#FF0000',
        strokeWeight: 3
    });

    poly2 = new google.maps.Polyline({
        path: [],
        strokeColor: '#FF0000',
        strokeWeight: 3
    });

    // Create a renderer for directions and bind it to the map.
    var rendererOptions = {
        map: map
    }

    directionsDisplay = new google.maps.DirectionsRenderer(rendererOptions);

    // var start = document.getElementById("start").value;
    // var end = document.getElementById("end").value;
    var travelMode = google.maps.DirectionsTravelMode.DRIVING

    // start = {'lat': 53.78622758423599, 'lng': -1.4048032457346316}
    // end = {'lat': 53.855145116552386, 'lng': -1.5911074611466254}

    var request = {
        origin: start,
        destination: end,
        travelMode: travelMode
    };

    // Route the directions and pass the response to a
    // function to create markers for each step.
    directionsService.route(request, function (response, status) {
        if (status == google.maps.DirectionsStatus.OK) {
            directionsDisplay.setDirections(response);

            var bounds = new google.maps.LatLngBounds();
            var route = response.routes[0];
            startLocation = new Object();
            endLocation = new Object();

            // For each route, display summary information.
            var path = response.routes[0].overview_path;
            var legs = response.routes[0].legs;
            for (i = 0; i < legs.length; i++) {
                if (i == 0) {
                    startLocation.latlng = legs[i].start_location;
                    startLocation.address = legs[i].start_address;
                    // marker = google.maps.Marker({map:map,position: startLocation.latlng});
                    console.log(legs[i].start_location)
                    marker = createMarker(legs[i].start_location, "start", legs[i].start_address, "green");
                }
                endLocation.latlng = legs[i].end_location;
                endLocation.address = legs[i].end_address;
                var steps = legs[i].steps;
                for (j = 0; j < steps.length; j++) {
                    var nextSegment = steps[j].path;
                    for (k = 0; k < nextSegment.length; k++) {
                        polyline.getPath().push(nextSegment[k]);
                        bounds.extend(nextSegment[k]);
                    }
                }
            }

            polyline.setMap(map);

            // map.fitBounds(bounds);

            //        createMarker(endLocation.latlng,"end",endLocation.address,"red");
            // map.setZoom(18);
            startAnimation();
        }
    });
}



var step = 150; // 5; // metres
var tick = 100; // milliseconds
var eol;
var k = 0;
var stepnum = 0;
var speed = "";
var lastVertex = 1;
var current_position = { 'lat': 53.80622758423599, 'lng': -1.4038032457346316 };


//=============== animation functions ======================
function updatePoly(d) {
    // Spawn a new polyline every 20 vertices, because updating a 100-vertex poly is too slow
    if (poly2.getPath().getLength() > 20) {
        poly2 = new google.maps.Polyline([polyline.getPath().getAt(lastVertex - 1)]);
        // map.addOverlay(poly2)
    }

    if (polyline.GetIndexAtDistance(d) < lastVertex + 2) {
        if (poly2.getPath().getLength() > 1) {
            poly2.getPath().removeAt(poly2.getPath().getLength() - 1)
        }
        poly2.getPath().insertAt(poly2.getPath().getLength(), polyline.GetPointAtDistance(d));
    } else {
        poly2.getPath().insertAt(poly2.getPath().getLength(), endLocation.latlng);
    }
}


function animate(d) {
    // alert("animate("+d+")");
    if (d > eol) {
        map.panTo(endLocation.latlng);
        marker.setPosition(endLocation.latlng);
        return;
    }
    var p = polyline.GetPointAtDistance(d);
    map.panTo(p);
    marker.setPosition(p);
    current_position = p
    updatePoly(d);
    timerHandle = setTimeout("animate(" + (d + step) + ")", tick);
}


function startAnimation() {
    eol = polyline.Distance();
    // map.setCenter(polyline.getPath().getAt(0));
    // map.addOverlay(new google.maps.Marker(polyline.getAt(0),G_START_ICON));
    // map.addOverlay(new GMarker(polyline.getVertex(polyline.getVertexCount()-1),G_END_ICON));
    // marker = new google.maps.Marker({location:polyline.getPath().getAt(0)} /* ,{icon:car} */);
    // map.addOverlay(marker);
    poly2 = new google.maps.Polyline({ path: [polyline.getPath().getAt(0)], strokeColor: "#0000FF", strokeWeight: 10 });
    // map.addOverlay(poly2);
    setTimeout("animate(50)", 50);  // Allow time for the initial map display
}


//=============== ~animation funcitons =====================

var lat_long = Array(), goto = Array(), severity = Array(), time = Array()
var first_time = -1

function getcsv() {
    qwest.get('/static/final.csv')
        .then(function (xhr, res) {
            var sp_res = res.split('\n')

            for (var i = 1; i < sp_res.length; i++) {
                var ssp_res = sp_res[i].split(',')

                lat_long.push({ 'lat': parseFloat(ssp_res[2]), 'lng': parseFloat(ssp_res[3]) })

                goto.push(ssp_res[1] == 'True')

                if (first_time == -1) {
                    first_time = parseFloat(ssp_res[5])
                }

                time.push(parseFloat(ssp_res[5]) - first_time)
            }

            console.log(time)
        })
}

getcsv()


var start_time = -1
var counter = 0
var active_markers = Array()
var last_counter = -1, new_last_counter = -1

function animationStep() {
    var timestamp = (new Date()).getTime()

    if (start_time === -1) {
        start_time = timestamp
    }

    var elapsed = timestamp - start_time

    console.log(timestamp, start_time, elapsed)

    while (time[counter] * 700 < elapsed) {
        active_markers.push({
            'marker': new google.maps.Marker(
                {
                    position: lat_long[counter],
                    map: map,
                }),
            'added': timestamp,
        })

        if (goto[counter]) {
            new_last_counter = counter
        }

        let last_removed = 0
        for (var i in active_markers) {
            if (active_markers[i].added - timestamp > 3000) {
                active_markers[i].marker.setMap(null)
                last_removed = i;
            }
        }

        i = 0
        while (i <= last_removed) {
            active_markers.pop()
            i++
        }

        counter++
    }

    if (last_counter !== new_last_counter) {
        last_counter = new_last_counter
        calcRoute(current_position, lat_long[last_counter])
    }

    setTimeout(animationStep, 100)
}


function startStuff() {
    setTimeout(animationStep, 100)
}

$(document).ready(function(){
    initialize()

    $('#click-this').on('click', function(){
        startStuff()
    })
})