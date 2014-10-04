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
    var site = SiteFactory.getSite($routeParams.siteId);
    var pit = SiteFactory.getSitePit($routeParams.siteId, $routeParams.pitId);
    var newPit = false;
    if ($routeParams.pitId === 'new' || pit === null) {
      newPit = true;
    }
    $scope.site = site;
    $scope.pit = pit;
    $scope.save = function () {
      if (newPit) {
        console.log('New Pit saved');
      } else {
        console.log('Pit ' + $scope.pit.id + ' saved');
      }
    };
  });
