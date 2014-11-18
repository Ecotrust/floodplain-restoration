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
  .controller('PiteditCtrl', function ($scope, $routeParams, $rootScope, $location, $window, SiteFactory) {

    if (!$rootScope.userName) {
      alert('You are not logged in. You will now be redirected to the login page.');
      $window.location = '/accounts/login/';
    }

    map.showMap(true);

    var activeSiteId = parseInt($routeParams.siteId, 10);
    $rootScope.activeSiteId = activeSiteId;
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
        properties: {
          'notes': '',
          'name': '<new pit>',
          'site': activeSiteId,
          'contamination': 0.5,
          'substrate': 0.5,
          'adjacent_river_depth': 0.5,
          'slope_dist': 0.5,
          'pit_levies': 0.5,
          'bedrock': 0.5,
          'bank_slope': 0.5,
          'pit_depth': 0.5,
          'surface_area': 0.5,
          'complexity': 0.5
        }
      };
    } else {
      activePitId = parseInt($routeParams.pitId, 10);
    }
    
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
      console.log('spinner on');
      try {
        var pitWkt = map.getActivePitWkt;
        if (isNewPit) {
          SiteFactory
            .postSitePit(activeSiteId, $scope.pit, pitWkt())
            .then(function() {
              console.log('spinner off');
              $location.path('/site/' + activeSiteId);
            });
        } else {
          SiteFactory
            .putSitePit(activeSiteId, $scope.pit, map.getActivePitWkt())
            .then(function() {
              console.log('spinner off');
              $location.path('/site/' + activeSiteId);
            });
        }
      } catch (error){
        console.log(error);
        $window.alert('No Pit Drawn');
      }
    };

  });
