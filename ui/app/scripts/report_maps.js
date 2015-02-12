
if (false) {var ol=null;}

var rmap;
var site = {};
var pits = {};

var pitsGeoJson = {
  'type': 'FeatureCollection',
  'crs': {
    'type': 'name',
    'properties':{
      'name': 'EPSG:3857'
    }
  },
  'features':[]
};

function buildMap(siteJson, pitsJson) {

  var siteGeoJson = {
    'type': 'FeatureCollection',
    'crs':{
      'type':'name',
      'properties':{
        'name':'EPSG:3857'
      }
    },
    'features':[
      {
        'type': 'Feature',
        'geometry': siteJson
      }
    ]
  };


  site.style = function() {
    return [new ol.style.Style({
      stroke: new ol.style.Stroke({
        color: 'white',
        lineDash: [4],
        width: 2
      }),
      fill: new ol.style.Fill({
        color: 'rgba(255, 255, 255, 0.2)'
      })
    })];
  };

  site.source = new ol.source.GeoJSON(({object:siteGeoJson}));

  for (var i = 0; i < pitsJson.length; i++) {
    var pit = pitsJson[i];
    pitsGeoJson.features.push(
      {
        'type': 'Feature',
        'geometry': pit.geometry,
        'properties':{
          'pk':pit.id,
          'id':pit.id,
          'name':pit.properties.name,
          'score':pit.properties.score.value
        }
      });
  }

  site.layer = new ol.layer.Vector({
    source: site.source,
    style: site.style
  });

  pits.style = function (feature) {
    return [new ol.style.Style({
      stroke: new ol.style.Stroke({
        color: '#F15A24',
        width: 2
      }),
      fill: new ol.style.Fill({
        color: 'rgba(255, 255, 255, 0)'
      }),
      text: new ol.style.Text({
        text: feature.get('name'),
        font: '12px Calibri,sans-serif',
        stroke: new ol.style.Stroke({
          color: '#fff',
          width: 3
        }),
        fill: new ol.style.Fill({
          color: '#000'
        })
      })
    })];
  };

  pits.source = new ol.source.GeoJSON(({object:pitsGeoJson}));

  pits.layer = new ol.layer.Vector({
    source: pits.source,
    style: pits.style
  });

  var extent = site.source.getExtent();

  rmap = new ol.Map({
    target: 'report-map',
    layers: [
      new ol.layer.Group({
        title: 'Base maps',
        layers: [
          new ol.layer.Tile({
            visible: true,
            title: 'Satellite',
            type: 'base',
            source: new ol.source.MapQuest({layer: 'sat'})
          }),
          site.layer,
          pits.layer
        ]
      })
    ],
    view: new ol.View({
      center: ol.proj.transform([-122, 44], 'EPSG:4326', 'EPSG:3857'),
      zoom: 7
    })
  });

  // map.getView().fitExtent(site.source.getExtent(), map.getSize());
  rmap.getView().fitExtent(extent, rmap.getSize());
}

if (false) {buildMap();}