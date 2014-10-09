'use strict';

/**
 * @ngdoc function
 * @name uiApp.controller:MapCtrl
 * @description
 * # MapCtrl
 * Controller of the uiApp
 */
angular.module('uiApp')
  .controller('MapCtrl', function ($scope, $rootScope, leafletData, SiteFactory) {


    //SiteFactory.setActiveSiteId($routeParams.siteId);
    var site = SiteFactory.getActiveSite();

    // See docs for leaflet.draw at https://github.com/Leaflet/Leaflet.draw
    var drawnItems = new L.FeatureGroup();

    var options = {
      edit: {
        featureGroup: drawnItems,
        remove: false,
        // edit: false
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

    $rootScope.$on('activeSiteUpdated', function (args) {
      console.log('MapCtrl says activeSiteChanged!', args);
    });
    
    var style = function (feature) {
      var isSite = false;
      if ('pit_set' in feature.properties) {
        isSite = true;
      }

      return {
        fillColor: isSite?'white':'red',
        weight: 2,
        opacity: 1,
        color: 'black',
        dashArray: isSite?'3':'1',
        fillOpacity: isSite?0.1:0.5
      };
    }

    var getData = function() {

      var theData = {
        'type': 'FeatureCollection',
        'features': [site]
      };

      // And the remainder are pits
      for (var i = site.properties.pit_set.length - 1; i >= 0; i--) {
        var pit = site.properties.pit_set[i];
        theData.features.push(pit);
      }

      return theData;
    }

    angular.extend($scope, {
      startview: {
        lat: 45,
        lng: -123,
        zoom: 7
      },
      controls: {
        custom: [ drawControl ]
      },
      geojson: {
        data: getData(),
        style: style
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
      map.on('draw:editstart', function () {
      //   //drawnItems.clearLayers();
      });
      map.on('draw:drawstart', function () {
        drawnItems.clearLayers();
      });
      map.on('draw:created', createdActiveFeature );
    });
  });
