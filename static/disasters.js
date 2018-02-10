function initMap(disasters) {
    console.log('init map');

    let map = new google.maps.Map(document.getElementById('disaster-map'), {
        center: {lat: 39, lng: -98},
        scrollwheel: true,
        zoom: 4,
        zoomControl: true,
        panControl: false,
        streetViewControl: false,
        styles: MAPSTYLES,
        mapTypeId: google.maps.MapTypeId.TERRAIN
    });


    let infoWindow = new google.maps.InfoWindow({ width: 150 });

      // attach markers to each disaster in returned JSON

        let disaster, marker, info;

        // scale marker size relative to counts
        let max_count =  disasters['counts'].slice(-1)[0];
        
        for (let key in disasters) {
            
            disaster = disasters[key]; 


            // create marker
                let marker = new google.maps.Marker({
                    position: new google.maps.LatLng(disaster['stateLat'], disaster['stateLong']),
                    map: map,
                    title: 'Disaster Count: ' + disaster['count'],
                    icon: { path: google.maps.SymbolPath.CIRCLE,
                            fillColor: disaster['color'],
                            fillOpacity: 0.6,
                            scale: 35 * (disaster['count']/max_count),
                            strokeWeight: 1
                           }
                });
            
            // create disaster info for the infoWindow
            info = (
              '<div class="window-content">' + 
                    '<p><b>State: </b>' + disaster['state'] + '</p>' +
                    '<p><b># of ' + disaster['incidentType'] + ' Incidents: </b>' + disaster['count'] + '</p>' +
                    '<p><b>Between: </b>' + disaster['start'] + ' and ' + disaster['end']+ '</p>' +
              '</div>');

            
            // bind marker and info to infoWindow
            bindInfoWindow(marker, map, infoWindow, info);
      }

    ;

    function bindInfoWindow(marker, map, infoWindow, info) {
        google.maps.event.addListener(marker, 'click', function () {
            infoWindow.close();
            infoWindow.setContent(info);
            infoWindow.open(map, marker);
        });
    }
}

google.maps.event.addDomListener(window, 'load', initMap);


function getFilters(evt) {
    evt.preventDefault();
    
    let url = '/disasters.json';

    let formInput = { 'incident_type': $('#select-type').val(),
                      'min_date': $('#min-date').val(),
                      'max_date': $('#max-date').val(),
                    };
    $.get(url, formInput, initMap)
}

// set default dates
document.getElementById('min-date').valueAsDate = new Date('1953-05-02T01:00:00+01:00');
document.getElementById('max-date').valueAsDate = new Date();

$('#form').on('submit', getFilters);