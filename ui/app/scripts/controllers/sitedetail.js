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
        console.log($scope.site);
        map.loadPits({
          type: 'FeatureCollection',
          features:$scope.site.properties.pit_set
        });
      }
    );

    $scope.deleteSite = function(siteId) {
      console.log('Deleted site ' + activeSiteId);
    };

    $scope.deleteSitePit = function(siteId, pitId) {
      console.log('Deleted pit ' + pitId + ' from site ' + activeSiteId);
    };

  });
