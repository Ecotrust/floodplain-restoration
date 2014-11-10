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
    $rootScope.showMap = true;
    
    $scope.sites = [];

    $rootScope.siteId = null;
    $rootScope.siteName = null;

    ///////////////////////////////////////////////////
    map.clear();
    SiteFactory.getSites()
      .then( function() {
        $scope.sites = SiteFactory.sites.features;
        console.log("within ctrl, then ", $scope.sites);
        map.loadSites(SiteFactory.sites);
      });
    ///////////////////////////////////////////////////
  });
