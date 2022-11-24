const map = L.map('map', {
    noWrap: true,
    minZoom: 1.75,
    zoomSnap: 0.25,
    maxZoom: 6,
}).fitWorld();

//L.control.scale().addTo(map);
// setInterval(function(){
//      map.setView([0, 0]);
//      setTimeout(function(){
//          map.setView([0, 0]);
//      }, 0);
//  }, 0);

// permet d'afficher le zoom :
 const ZoomViewer = L.Control.extend({
    onAdd: function () {
        const gauge = L.DomUtil.create('div');
        gauge.style.width = '200px';
        gauge.style.background = 'rgba(255,255,255,0.5)';
        gauge.style.textAlign = 'left';
        map.on('zoomstart zoom zoomend', function (ev) {
            gauge.innerHTML = 'Zoom level: ' + map.getZoom();
        });
        return gauge;
    }
});
const zoomViewer = (new ZoomViewer()).addTo(map);

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);

