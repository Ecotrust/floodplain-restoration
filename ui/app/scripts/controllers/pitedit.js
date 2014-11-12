'use strict';

// Hack to make linter happy about global variables
if (false) { var map; }

/**
 * @ngdoc function
 * @name uiApp.controller:PiteditCtrl
 * @description
 * # PiteditCtrl
 * Controller of the uiApp
 */
angular.module('uiApp')
  .controller('PiteditCtrl', function ($scope, $routeParams, $rootScope, SiteFactory) {
    map.showMap(true);

    var activeSiteId = parseInt($routeParams.siteId, 10);
    var activePitId;
    var blankPit;
    var isNewPit = false;

    if ($routeParams.pitId === undefined) {
      activePitId = null;
      isNewPit = true;
      blankPit = {
        id: '',
        type: 'Feature',
        geometry: {}, // wkt
        properties: {}
      };
    } else {
      activePitId = parseInt($routeParams.pitId, 10);
    }
    
    console.log($routeParams, isNewPit);
    $scope.pit = {};
    $scope.site = {};
    $scope.sites = [];

    SiteFactory.getSites().then( function() {
      $scope.sites = SiteFactory.sites.features;

      // set active site
      for (var i = SiteFactory.sites.features.length - 1; i >= 0; i--) {
        var site = SiteFactory.sites.features[i];
        if (site.id === activeSiteId) {
          $scope.site = site;
        }
      }

      map.clear();
      map.loadSites({
        type: 'FeatureCollection',
        features:[$scope.site]
      });

      if (isNewPit) {
        $scope.pit = blankPit;
        map.loadPits({
          type: 'FeatureCollection',
          features: []
        });
        map.addPit();
      } else {
        for (var j = $scope.site.properties.pit_set.length - 1; j >= 0; j--) {
          var pit = $scope.site.properties.pit_set[j];
          if (pit.id === activePitId) {
            $scope.pit = pit;
          }
        }
        map.loadPits({
          type: 'FeatureCollection',
          features: [$scope.pit]
        });
        map.editPit();
      }

      map.showMap(true);
    });

    var newPit = false;
    if ($routeParams.pitId === 'new' || $scope.pit === null) {
      newPit = true;
      $scope.pit = {
        id: '',
        type: 'Feature',
        geometry: {}, // wkt
        properties: {}
      };
    }

    $scope.$on('activeFeatureWKT', function (event, wkt) {
      $scope.pit.geometry = wkt;
    });

    $scope.save = function () {
      if (isNewPit) {
        SiteFactory
          .postSitePit(activeSiteId, $scope.pit, map.getActivePitWkt())
          .then(function() {
            console.log('spinner off');
          });
      } else {
        SiteFactory
          .putSitePit(activeSiteId, $scope.pit, map.getActivePitWkt())
          .then(function() {
            console.log('spinner off');
          });
      }
    };

  });
