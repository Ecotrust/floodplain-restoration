'use strict';

// Just for the sake of jshint
// TODO remove this!!!
var ol = ol;
var map;

// ol3 map directive
angular.module('uiApp')
  .directive('olMap', ['$parse', function($parse) {
  return {
    restrict: 'A',
    link: function(scope, element, attrs) {
      map = $parse(attrs.olMap)(scope);
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
      source: siteSource,
      style: function() {
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
      }
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
      source: pitSource,
      style: function() {  // optionally takes feature, resolution 
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
      }
    });

    var baseLayer = new ol.layer.Tile({
      source: new ol.source.OSM()
    });
    // var editFeature = {};
    // var editSource = new ol.source.GeoJSON(
    //   ({object: editFeature})
    // );
    // var editLayer = new ol.layer.Vector({
    //   source: editSource
    //   // style: pitStyle
    // });
    
    // var drawSource = new ol.source.Vector();
    // var drawLayer = new ol.layer.Vector({
    //   source: drawSource,
    //   style: new ol.style.Style({
    //     fill: new ol.style.Fill({
    //       color: 'rgba(255, 255, 255, 0.2)'
    //     }),
    //     stroke: new ol.style.Stroke({
    //       color: '#ffcc33',
    //       width: 2
    //     }),
    //     image: new ol.style.Circle({
    //       radius: 7,
    //       fill: new ol.style.Fill({
    //         color: '#ffcc33'
    //       })
    //     })
    //   })
    // });

    $rootScope.$on('activeSiteChanged', function (args) {
      console.log('MapCtrl says activeSiteChanged!', args);
    });
    
    $rootScope.$on('activePitChanged', function () {
      // var pit = SiteFactory.getActivePit();

      // // console.log(modify);
      // debugger;
      // modify = new ol.interaction.Modify({
      //   features: new ol.Collection([])
      // });

      // //modify.features = new ol.Collection([pit]);
      // // modify.features.clear();
      // // modify.features.push(pit);
      // //console.log('MapCtrl says activePitChanged to', p);
      // modify = new ol.interaction.Modify({
      //   features: new ol.Collection([pitLayer.source_.getFeatureById(SiteFactory.getActivePit().id)])
      // });
      // console.log('---', modify);
    });


    // select = new ol.interaction.Select({
    //   layers: [pitLayer]
    // });

    // draw = new ol.interaction.Draw({
    //   source: drawSource,
    //   type: /** @type {ol.geom.GeometryType} */ ('Polygon')
    // });

    // var modify = new ol.interaction.Modify({
    //   features: select.getFeatures()
    // });

    var map = new ol.Map({
      //interactions: ol.interaction.defaults().extend([draw, select, modify]),
      layers: [
        baseLayer,
        siteLayer,
        pitLayer
        // drawLayer
      ],
      view: new ol.View({
        center: [-13654860, 5653425],
        zoom: 9
      })
    });
    
    $scope.map1 = map;

  });
