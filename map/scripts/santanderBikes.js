var bikeMarkers = [];

function loadBikes() {
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function () {
    if (this.readyState == 4 && this.status == 200) {
      addMarkers(this);
    }
  };
  xhttp.open(
    "GET",
    "https://tfl.gov.uk/tfl/syndication/feeds/cycle-hire/livecyclehireupdates.xml"
  );
  xhttp.send();
}

function addMarkers(xml) {
  var i;
  var xmlDoc = xml.responseXML;
  var x = xmlDoc.getElementsByTagName("station");
  for (i = 0; i < x.length; i++) {
    // These are the ids for the bike stations around the Olympic Park
    var ids = ["785", "786", "787", "788", "789", "790"];
    var currentID =
      x[i].getElementsByTagName("id")[0].childNodes[0].nodeValue;

    if (ids.includes(currentID)) {
      var nbBikes =
        x[i].getElementsByTagName("nbBikes")[0].childNodes[0].nodeValue;
      var popup = new mapboxgl.Popup().setText(nbBikes).addTo(map);

      var long =
        x[i].getElementsByTagName("long")[0].childNodes[0].nodeValue;
      var lat =
        x[i].getElementsByTagName("lat")[0].childNodes[0].nodeValue;

      // create a HTML element for each feature
      const el = document.createElement('div');
      el.className = 'bike-marker';

      // Create a new marker.
      const marker = new mapboxgl.Marker(el)
        .setLngLat([long, lat])
        .addTo(map)
        .setPopup(popup);
      
      bikeMarkers.push(marker);
    }
  }
}

function removeBikes() {
  bikeMarkers.forEach(bike => {
    bike.remove();
  });
  bikeMarkers = [];
}