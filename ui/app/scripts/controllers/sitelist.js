'use strict';

/**
 * @ngdoc function
 * @name uiApp.controller:SitelistCtrl
 * @description
 * # SitelistCtrl
 * Controller of the uiApp
 */
angular.module('uiApp')
  .controller('SitelistCtrl', function ($scope, $rootScope, SiteFactory) {
    map.showMap(true);
    
    $scope.sites = [];

    $rootScope.siteId = null;
    $rootScope.siteName = null;

    SiteFactory.getSites()
      .then( function() {
        $scope.sites = SiteFactory.sites.features;
        map.clear();
        map.loadSites(SiteFactory.sites);
      });
  });
