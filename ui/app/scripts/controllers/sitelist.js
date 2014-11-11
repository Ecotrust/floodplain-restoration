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

    $rootScope.siteId = null;
    $rootScope.siteName = null;

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
          for (var i = $scope.sites.length - 1; i >= 0; i--) {
            var site = $scope.sites[i];
            if (site.id === siteId) {
              $scope.sites.splice(i, 1);  // pop i off the array

              // TODO 
              // manage map; remove site and reload?
            }
          }
        });
      }
    };

  });
