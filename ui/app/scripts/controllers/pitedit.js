'use strict';

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
    var activePitId = parseInt($routeParams.pitId, 10);

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

      // set active pit
      for (var j = $scope.site.properties.pit_set.length - 1; j >= 0; j--) {
        var pit = $scope.site.properties.pit_set[j];
        if (pit.id === activePitId) {
          $scope.pit = pit;
        }
      }

      // map
      map.clear();
      map.loadSites({
        type: 'FeatureCollection',
        features:[$scope.site]
      });
      if (newPit) {
        map.loadPits({
          type: 'FeatureCollection',
          features: []
        });
        map.addPit();
      } else {
        // map.loadPits(SiteFactory.getActivePitCollection());
        map.loadPits({
          type: 'FeatureCollection',
          // features:$scope.site.properties.pit_set
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
      if (newPit) {
        console.log('POST new Pit');
      } else {
        console.log('PUT edited Pit');
      }
      console.log("New geometry is ", map.getActivePitWkt());
      console.log('Save Pit ' + $scope.pit.id );
      console.log('spinner on');
      console.log('If AJAX call is a success, update the SiteFactory singleton');
      console.log('spinner off');
    };

  });
