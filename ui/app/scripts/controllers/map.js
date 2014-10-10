'use strict';

// Just for the sake of jshint
// TODO remove this!!!
var ol = ol;

// ol3 map directive
angular.module('uiApp')
  .directive('olMap', ['$parse', function($parse) {
  return {
    restrict: 'A',
    link: function(scope, element, attrs) {
      var map = $parse(attrs.olMap)(scope);
      map.setTarget(element[0]);
    }
  };
}]);


/**
 * @ngdoc function
 * @name uiApp.controller:MapCtrl
 * @description
 * # MapCtrl
 * Controller of the uiApp
 */
angular.module('uiApp')
  .controller('MapCtrl', function ($scope, $rootScope, SiteFactory) {

    var site = SiteFactory.getActiveSite();


    var siteStyle = function() {
      var style = [new ol.style.Style({
        stroke: new ol.style.Stroke({
          color: 'black',
          lineDash: [3],
          width: 1
        }),
        fill: new ol.style.Fill({
          color: 'rgba(255, 255, 255, 0.2)'
        })
      })];

      return style;
    };

    var siteSource = new ol.source.GeoJSON(
      ({
        object: site
      })
    );

    var siteLayer = new ol.layer.Vector({
      source: siteSource,
      style: siteStyle
    });


    var pitStyle = function() {  // optionally takes feature, resolution 
      var style = [new ol.style.Style({
        stroke: new ol.style.Stroke({
          color: 'black',
          width: 1
        }),
        fill: new ol.style.Fill({
          color: 'rgba(255, 255, 0, 0.5)'
        })
      })];

      return style;
    };

    var pitSource = new ol.source.GeoJSON(
      ({
        object: {
          'type': 'FeatureCollection',
          'features': site.properties.pit_set
        }
      })
    );

    var pitLayer = new ol.layer.Vector({
      source: pitSource,
      style: pitStyle
    });


    $rootScope.$on('activeSiteUpdated', function (args) {
      console.log('MapCtrl says activeSiteChanged!', args);
    });

    var map = new ol.Map({
      layers: [
        new ol.layer.Tile({
          source: new ol.source.OSM()
        }),
        siteLayer,
        pitLayer
      ],
      view: new ol.View({
        center: [-13654860, 5503425],
        zoom: 6
      })
    });
    
    $scope.map1 = map;

    $scope.editPit = function(pitId) {
      console.log('Editing pit ' + pitId);
    };


  });
