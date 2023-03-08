function renderShadows() {
    map.on('load', () => {
        const shadeMap = new ShadeMap({
          date: new Date(),    // display shadows for current date
          color: '#01112f',    // shade color
          opacity: 0.7,        // opacity of shade color
          apiKey: "eyJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6ImRvbmd5b3VuZy5saW0uMjJAdWNsLmFjLnVrIiwiY3JlYXRlZCI6MTY3NzUwNDk1Mjc3NCwiaWF0IjoxNjc3NTA0OTUyfQ.8sxIY7MfKPrgfrTI_UMb4q07ofbT6yvLrOyGVro940o",
          terrainSource: {
            tileSize: 256,       // DEM tile size
            maxZoom: 15,         // Maximum zoom of DEM tile set
            getSourceUrl: ({ x, y, z }) => {
              // return DEM tile url for given x,y,z coordinates
              return `https://s3.amazonaws.com/elevation-tiles-prod/terrarium/${z}/${x}/${y}.png`
            },
            getElevation: ({ r, g, b, a }) => {
              // return elevation in meters for a given DEM tile pixel
              return (r * 256 + g + b / 256) - 32768
            }
          },
          debug: (msg) => { console.log(new Date().toISOString(), msg) },
        }).addTo(map);
      
        // advance shade by 1 hour
        shadeMap.setDate(new Date(Date.now() + 1000 * 60 * 60)); 
      
        // sometime later
        // ...remove layer
        shadeMap.remove();
      });
}