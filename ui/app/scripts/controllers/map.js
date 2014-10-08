'use strict';

/**
 * @ngdoc function
 * @name uiApp.controller:MapCtrl
 * @description
 * # MapCtrl
 * Controller of the uiApp
 */
angular.module('uiApp')
  .controller('MapCtrl', function ($scope, $rootScope, leafletData) {

    // See docs for leaflet.draw at https://github.com/Leaflet/Leaflet.draw
    var drawnItems = new L.FeatureGroup();
    var options = {
      edit: {
        featureGroup: drawnItems,
        remove: false,
        edit: false
      },
      draw: {
        polyline: false,
        rectangle: false,
        circle: false,
        marker: false,
        // polygon: false
        polygon: {
          repeatMode: false,
          showArea: true
        }
      }
    };

    var drawControl = new L.Control.Draw(options);

    angular.extend($scope, {
      startview: {
        lat: 45,
        lng: -123,
        zoom: 8
      },
      controls: {
        custom: [ drawControl ]
      }
    });

    var createdActiveFeature = function(e) {
      var layer = e.layer;
      drawnItems.addLayer(layer);
      var json = layer.toGeoJSON();

      // Construct Well Known Text
      // Assume 2D polygon with no interior rings
      var wkts = [];
      var coords = json.geometry.coordinates[0];
      for (var i = coords.length - 1; i >= 0; i--) {
        wkts.push(coords[i][0] + ' ' + coords[i][1]);
      }
      var wkt = 'POLYGON((' + wkts.join(', ') + '))';

      $rootScope.$broadcast('activeFeatureWKT', wkt);
    };

    leafletData.getMap().then(function(map) {
      map.addLayer(drawnItems);

      map.on('draw:drawstart', function () {
        drawnItems.clearLayers();
      });

      map.on('draw:created', createdActiveFeature);
    });
  });
