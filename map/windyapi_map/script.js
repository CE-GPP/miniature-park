const options = {
    // Required: API key
    key: 'P8sisijK4XrEGhI9p3y35RgPPo0fZAwe', // REPLACE WITH YOUR KEY !!!

    // Put additional console output
    verbose: true,

    englishLabels: true,

    // Optional: Initial state of the map
    lat: 51.5442,
    lon: 0.0159,
    zoom: 11, //max zoom level
};

// Initialize Windy API
windyInit(options, windyAPI => {
    // windyAPI is ready, and contain 'map', 'store',
    // 'picker' and other usefull stuff
    const { store } = windyAPI;
    // All the params are stored in windyAPI.store

    const { map } = windyAPI;
    // .map is instance of Leaflet map

    // L.popup()
    //     .setLatLng([51.5442, 0.0159])
    //     //.setContent('Hello World')
    //     .openOn(map);
});
