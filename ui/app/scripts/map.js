'use strict';

var map = {
  site: {},
  pit: {}
};


/*
 * Vector feature styling
 */
map.styleEditable = function() {
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

map.pit.style = function() {
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

map.site.style = function() {
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
map.loadSites = function(data) {

  if (!data || data.type !== 'FeatureCollection') {
    console.log("ERROR in data supplied to map.loadSites:", data);
    return false;
  }
  map.map.removeLayer(map.site.layer);

  map.site.source = new ol.source.GeoJSON(
    ({
      object: data
    })
  );

  map.site.layer = new ol.layer.Vector({
    source: map.site.source,
    style: map.site.style
  });

  map.map.addLayer(map.site.layer);
  map.map.getView().fitExtent(map.site.source.getExtent(), map.map.getSize());
};

map.loadPits = function(data) {
  
  if (!data || data.type !== 'FeatureCollection') {
    console.log("ERROR in data supplied to map.loadPits:", data)
    return false;
  }
  map.map.removeLayer(map.pit.layer);

  map.pit.source = new ol.source.GeoJSON(
    ({
      object: data
    })
  );

  map.pit.layer = new ol.layer.Vector({
    source: map.pit.source,
    style: map.pit.style
  });

  map.map.addLayer(map.pit.layer);
};

map.clear = function() {
  map.map.removeInteraction(map.drawPit);
  map.map.removeInteraction(map.drawSite);
  map.map.removeInteraction(map.modifyPit);
  map.map.removeInteraction(map.modifySite);
  map.map.removeLayer(map.pit.layer);
  map.map.removeLayer(map.site.layer);
};

map.wktFormat = new ol.format.WKT();

map.editSite = function() {
  map.modifySite = new ol.interaction.Modify({
    features: new ol.Collection(map.site.source.getFeatures()),
    deleteCondition: function(event) {
      return ol.events.condition.shiftKeyOnly(event) &&
          ol.events.condition.singleClick(event);
    }
  });
  map.map.addInteraction(map.modifySite);
  map.site.layer.setStyle(map.styleEditable);
};

map.editPit = function() {
  map.modifyPit = new ol.interaction.Modify({
    features: new ol.Collection(map.pit.source.getFeatures()),
    deleteCondition: function(event) {
      return ol.events.condition.shiftKeyOnly(event) &&
          ol.events.condition.singleClick(event);
    }
  });
  map.map.addInteraction(map.modifyPit);
  map.map.getView().fitExtent(map.pit.source.getExtent(), map.map.getSize());
  map.pit.layer.setStyle(map.styleEditable);
};

map.addSite = function() {
  map.drawSite = new ol.interaction.Draw({
    source: map.site.source,
    type: 'MultiPolygon'
  });
  map.drawSite.on('drawstart', function(e) {
    map.site.source.clear();
  });
  map.drawSite.on('drawend', function(e) {
    console.log("drawing ended... TODO start editing");
  });
  map.map.addInteraction(map.drawSite);
  map.site.layer.setStyle(map.styleEditable);
};

map.addPit = function() {
  map.drawPit = new ol.interaction.Draw({
    source: map.pit.source,
    type: 'Polygon'
  });
  map.drawPit.on('drawstart', function(e) {
    console.log('clearing drawing');
    map.pit.source.clear();
  });
  map.drawPit.on('drawend', function(e) {
    console.log("drawing ended... TODO start editing");
  });
  map.map.addInteraction(map.drawPit);
  map.pit.layer.setStyle(map.styleEditable);
};

map.getActiveSiteWkt = function() {
  var features = map.site.source.getFeatures();
  var geom = features[0].getGeometry();
  var geomwkt = map.wktFormat.writeGeometry(geom);
  return geomwkt;
};

map.getActivePitWkt = function() {
  var features = map.pit.source.getFeatures();
  var geom = features[0].getGeometry();
  var geomwkt = map.wktFormat.writeGeometry(geom);
  return geomwkt;
};

map.map = new ol.Map({
  target: 'map',
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

map.onResize = function (height, width) {
  $('.map-container').height(height - 51);
  map.map.updateSize();
};

function resize() {
  var height = $(window).height();
  var width = $(window).width();
  var screen_width = $( window ).width();
  map.onResize(height, width);
    
  if (screen_width > 991) {
    leftPanelResize(height, width);
    bodyResize(height, width);
  }
};

function bodyResize(height, width){
  $('body').css('padding-top', parseInt($('#main-navbar').css("height")));
};

function leftPanelResize(height, width) { 
  $('.left-panel-column').height(height - 51);
};

$(window).resize(resize);

$(document).ready(function() {
  window.setTimeout(resize,1);
});

map.showMap = function (show) {
  if (show) {
    $('#left-container').removeClass('col-md-12');
    $('#map-container').addClass('col-md-6');
    $('#left-container').addClass('col-md-6');
  } else {
    $('#map-container').removeClass('col-md-6');
    $('#left-container').removeClass('col-md-6');
    $('#left-container').addClass('col-md-12');
  }
};