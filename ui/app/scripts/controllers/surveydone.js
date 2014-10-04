'use strict';

/**
 * @ngdoc function
 * @name uiApp.controller:SurveydoneCtrl
 * @description
 * # SurveydoneCtrl
 * Controller of the uiApp
 */
angular.module('uiApp')
  .controller('SurveydoneCtrl', function ($scope, $routeParams, SiteFactory) {
    $scope.suitability = SiteFactory.getSuitabilityScores($routeParams.siteId); // /api/site/2/suitability.json
  });
