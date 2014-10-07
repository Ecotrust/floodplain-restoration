'use strict';

/**
 * @ngdoc function
 * @name uiApp.controller:PiteditCtrl
 * @description
 * # PiteditCtrl
 * Controller of the uiApp
 */
angular.module('uiApp')
  .controller('PiteditCtrl', function ($scope, $routeParams, $rootScope, SiteFactory, PitFactory) {
    $rootScope.showMap = true;

    var site = SiteFactory.getSite($routeParams.siteId);
    $scope.site = site;

    var pit = PitFactory.getSitePit($routeParams.siteId, $routeParams.pitId);
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
