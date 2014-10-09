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
        console.log('New Pit saved');
        console.log(JSON.stringify($scope.pit));
      } else {
        console.log('Pit ' + $scope.pit.id + ' saved');
      }
    };
  });
