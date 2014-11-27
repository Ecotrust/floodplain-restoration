'use strict';

if (false) { var ol = null; }

var rmap = {
  site: {},
  pit: {}
};


/*
 * Vector feature styling
 */
rmap.styleEditable = function() {
  return [new ol.style.Style({
    stroke: new ol.style.Stroke({
      color: 'blue',
      width: 2
    }),
    fill: new ol.style.Fill({
      color: 'rgba(55, 55, 255, 0.4)'
    })
  })];
};

rmap.pit.style = function() {
  return [new ol.style.Style({
    stroke: new ol.style.Stroke({
      color: 'white',
      width: 2
    }),
    fill: new ol.style.Fill({
      color: 'rgba(255, 255, 100, 0.1)'
    })
  })];
};

rmap.site.style = function() {
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


/*
 * Public methods
 */
rmap.loadSites = function(data) {

  if (!data || data.type !== 'FeatureCollection') {
    console.log('ERROR in data supplied to rmap.loadSites:', data);
    return false;
  }
  rmap.map.removeLayer(rmap.site.layer);

  rmap.site.source = new ol.source.GeoJSON(
    ({
      object: data
    })
  );

  rmap.site.layer = new ol.layer.Vector({
    source: rmap.site.source,
    style: rmap.site.style
  });

  rmap.map.addLayer(rmap.site.layer);
  rmap.map.getView().fitExtent(rmap.site.source.getExtent(), rmap.map.getSize());
};

rmap.loadPits = function(data) {
  
  if (!data || data.type !== 'FeatureCollection') {
    console.log('ERROR in data supplied to rmap.loadPits:', data);
    return false;
  }
  rmap.map.removeLayer(rmap.pit.layer);

  rmap.pit.source = new ol.source.GeoJSON(
    ({
      object: data
    })
  );

  rmap.pit.layer = new ol.layer.Vector({
    source: rmap.pit.source,
    style: rmap.pit.style
  });

  rmap.map.addLayer(rmap.pit.layer);
};

rmap.clear = function() {
  rmap.map.removeInteraction(rmap.drawPit);
  rmap.map.removeInteraction(rmap.drawSite);
  rmap.map.removeInteraction(rmap.modifyPit);
  rmap.map.removeInteraction(rmap.modifySite);
  rmap.map.removeLayer(rmap.pit.layer);
  rmap.map.removeLayer(rmap.site.layer);
};

rmap.wktFormat = new ol.format.WKT();

rmap.getActiveSiteWkt = function() {
  var features = rmap.site.source.getFeatures();
  var geom = features[0].getGeometry();
  var geomwkt = rmap.wktFormat.writeGeometry(geom);
  return geomwkt;
};

rmap.getActivePitWkt = function() {
  var features = rmap.pit.source.getFeatures();
  var geom = features[0].getGeometry();
  var geomwkt = rmap.wktFormat.writeGeometry(geom);
  return geomwkt;
};

rmap.map = new ol.Map({
  target: 'report-map',
  layers: [
    new ol.layer.Tile({
      source: new ol.source.MapQuest({layer: 'sat'})
    })
  ],
  view: new ol.View({
    center: ol.proj.transform([-122, 44], 'EPSG:4326', 'EPSG:3857'),
    zoom: 7
  })
});
