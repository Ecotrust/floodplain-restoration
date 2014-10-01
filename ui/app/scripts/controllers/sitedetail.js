'use strict';

/**
 * @ngdoc function
 * @name uiApp.controller:SitedetailCtrl
 * @description
 * # SitedetailCtrl
 * Controller of the uiApp
 */
angular.module('uiApp')
  .controller('SitedetailCtrl', function ($scope, $routeParams, SiteFactory) {
    $scope.site = SiteFactory.getSite($routeParams.siteId);
  });
