'use strict';

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


    var siteSource = new ol.source.GeoJSON(
      ({
        object: site
      })
    );

    var siteLayer = new ol.layer.Vector({
      source: siteSource
      // style: styleFunction
    });

    var pitSource = new ol.source.GeoJSON(
      ({
        object: {
          'type': 'FeatureCollection',
          'features': site.properties.pit_set
        }
      })
    );

    var pitLayer = new ol.layer.Vector({
      source: pitSource
      // style: styleFunction
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
  });
