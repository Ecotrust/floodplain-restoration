'use strict';

/**
 * @ngdoc function
 * @name uiApp.controller:SitedetailCtrl
 * @description
 * # SitedetailCtrl
 * Controller of the uiApp
 */
angular.module('uiApp')
  .controller('SitedetailCtrl', function ($scope, $routeParams, $rootScope, SiteFactory) {
    $rootScope.showMap = true;
    $scope.site = SiteFactory.getSite($routeParams.siteId);

    $scope.deleteSite = function(siteId) {
      console.log('Deleted site ' + siteId);
    };

    $scope.deleteSitePit = function(siteId, pitId) {
      console.log('Deleted ' + pitId + 'from site ' + siteId);
    };

  });
