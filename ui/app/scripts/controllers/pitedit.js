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
    $rootScope.showMap = true;

    SiteFactory.setActiveSiteId($routeParams.siteId);
    var site = SiteFactory.getActiveSite();
    $scope.site = site;

    SiteFactory.setActivePitId($routeParams.pitId);
    var pit = SiteFactory.getSitePit($routeParams.pitId);
    $scope.pit = pit;

    var newPit = false;
    if ($routeParams.pitId === 'new' || pit === null) {
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

    // ----------------------- Map setup ------------------------------------//
    map.clear();
    map.loadSites(SiteFactory.getActiveSiteCollection());
    if (newPit) {
      map.loadPits({type: 'FeatureCollection', features: []});
      map.addPit();
    } else {
      map.loadPits(SiteFactory.getActivePitCollection());
      map.editPit();
    } 
  });
