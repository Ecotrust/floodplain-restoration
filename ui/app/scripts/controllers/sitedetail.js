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
    SiteFactory.setActiveSiteId($routeParams.siteId);
    $scope.site = SiteFactory.getActiveSite();

    $scope.deleteSite = function(siteId) {
      console.log('Deleted site ' + siteId);
    };

    $scope.deleteSitePit = function(siteId, pitId) {
      console.log('Deleted pit ' + pitId + ' from site ' + siteId);
    };

    ///////////////////////////////////////////////////
    map.clear();
    map.loadSites(SiteFactory.getActiveSiteCollection());
    map.loadPits(SiteFactory.getPitsCollection());
    ///////////////////////////////////////////////////
  });
