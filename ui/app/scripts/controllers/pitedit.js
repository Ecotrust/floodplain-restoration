'use strict';

/**
 * @ngdoc function
 * @name uiApp.controller:PiteditCtrl
 * @description
 * # PiteditCtrl
 * Controller of the uiApp
 */
angular.module('uiApp')
  .controller('PiteditCtrl', function ($scope, $routeParams, SiteFactory) {
    $scope.site = SiteFactory.getSite($routeParams.siteId);
    $scope.pit = SiteFactory.getSitePit($routeParams.siteId, $routeParams.pitId);

    $scope.pitAttrs = [
      'contamination', 'substrate', 'adjacent_river_depth',
      'slope_dist', 'pit_levies', 'bedrock', 'bank_slope',
      'pit_depth', 'surface_area', 'complexity'
    ];
    
  });
