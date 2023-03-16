
// function initDemoMap(){

//     var Esri_WorldImagery = L.tileLayer('http://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', {
//         attribution: 'Tiles &copy; Esri &mdash; Source: Esri, i-cubed, USDA, USGS, ' +
//         'AEX, GeoEye, Getmapping, Aerogrid, IGN, IGP, UPR-EGP, and the GIS User Community'
//     });

//     var Esri_DarkGreyCanvas = L.tileLayer(
//         "http://{s}.sm.mapstack.stamen.com/" +
//         "(toner-lite,$fff[difference],$fff[@23],$fff[hsl-saturation@20])/" +
//         "{z}/{x}/{y}.png",
//         {
//             attribution: 'Tiles &copy; Esri &mdash; Esri, DeLorme, NAVTEQ, TomTom, Intermap, iPC, USGS, FAO, ' +
//             'NPS, NRCAN, GeoBase, Kadaster NL, Ordnance Survey, Esri Japan, METI, Esri China (Hong Kong), and the GIS User Community'
//         }
//     );

//     var baseLayers = {
//         "Satellite": Esri_WorldImagery,
//         "Grey Canvas": Esri_DarkGreyCanvas
//     };

//     var map = L.map('map', {
//         layers: [ Esri_WorldImagery ]
//     });

//     var layerControl = L.control.layers(baseLayers, null, {collapsed:false});
//     layerControl.addTo(map);
//     map.setView([51.5442, 0.0159], 14);

//     return {
//         map: map,
//         layerControl: layerControl
//     };
// }

var map = L.map('map').setView([51.5442, 0.0159], 14);

L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);

var baseLayer = L.tileLayer(
    'http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',{
      attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="http://cloudmade.com">CloudMade</a>',
      maxZoom: 18
    }
  );
  var overlays = {"Clear": baseLayer};
  var layerControl = L.control.layers(overlays, null, {collapsed:false}).addTo(map);

// demo map
// var mapStuff = initDemoMap();
// var map = mapStuff.map;
//var layerControl = map.layerControl;
var handleError = function(err){
    console.log('handleError...');
    console.log(err);
};

WindJSLeaflet.init({
	localMode: true,
	map: map,
	layerControl: layerControl,
	useNearest: false,
	timeISO: null,
	nearestDaysLimit: 7,
	displayValues: true,
	displayOptions: {
		displayPosition: 'bottomleft',
		displayEmptyString: 'No wind data'
	},
	overlayName: 'wind',

	//https://github.com/danwild/wind-js-server
	pingUrl: 'http://localhost:7000/alive',
	latestUrl: 'http://localhost:7000/latest',
	nearestUrl: 'http://localhost:7000/nearest',
	errorCallback: handleError
});