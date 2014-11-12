'use strict';

if (false) { var map; }

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

    $rootScope.activeSiteId = null;

    SiteFactory.getSites()
      .then( function() {
        $scope.sites = SiteFactory.sites.features;
        map.clear();
        map.loadSites(SiteFactory.sites);
        map.showMap(true);
      });

    $scope.deleteSite = function(siteId) {
      if (confirm('Delete this property? Are you sure?') === true) {
        SiteFactory.deleteSite(siteId).then(function() {

          // Update new sites
          $scope.sites = SiteFactory.sites.features;

          // Map active sites
          map.clear();
          map.loadSites(SiteFactory.sites);
        });
      }
    };

  });
