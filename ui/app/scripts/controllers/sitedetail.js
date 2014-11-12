'use strict';

if (false) { var map; }

/**
 * @ngdoc function
 * @name uiApp.controller:SitedetailCtrl
 * @description
 * # SitedetailCtrl
 * Controller of the uiApp
 */
angular.module('uiApp')
  .controller('SitedetailCtrl', function ($scope, $routeParams, $rootScope, SiteFactory) {
    map.showMap(true);

    var activeSiteId = parseInt($routeParams.siteId, 10);
    SiteFactory.activeSiteId = activeSiteId;
    // $scope.site = SiteFactory.getActiveSite();

    $scope.sites = [];
    $scope.site = {};

    SiteFactory.getSites().then(
      function() {
        $scope.sites = SiteFactory.sites.features;

        // set active site
        for (var i = SiteFactory.sites.features.length - 1; i >= 0; i--) {
          var site = SiteFactory.sites.features[i];
          if (site.id === activeSiteId) {
            $scope.site = site;
          }
        }

        // map
        map.clear();
        map.loadSites({
          type: 'FeatureCollection',
          features:[$scope.site]
        });
        map.loadPits({
          type: 'FeatureCollection',
          features:$scope.site.properties.pit_set
        });
        map.showMap(true);
      }
    );

    $scope.deleteSitePit = function(siteId, pitId) {
      if (confirm('Delete this pit? Are you sure?') === true) {
        SiteFactory.deleteSitePit(siteId, pitId).then(function() {

          // Update new sites
          $scope.sites = SiteFactory.sites.features;

          // Set active site
          for (var i = SiteFactory.sites.features.length - 1; i >= 0; i--) {
            var site = SiteFactory.sites.features[i];
            if (site.id === activeSiteId) {
              $scope.site = site;
            }
          }

          // Update Map for Pits
          map.loadPits({
            type: 'FeatureCollection',
            features:$scope.site.properties.pit_set
          });
        });
      }
    };

  });
