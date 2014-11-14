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
  .controller('SitedetailCtrl', function ($scope, $routeParams, $rootScope, $window, SiteFactory, NodeFactory) {

    if (!$rootScope.userName) {
      alert('You are not logged in. You will now be redirected to the login page.');
      $window.location = '/accounts/login/';
    }

    map.showMap(true);

    var activeSiteId = parseInt($routeParams.siteId, 10);
    $rootScope.activeSiteId = activeSiteId;
    
    $scope.surveyPrompt = "Begin Survey";
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

    NodeFactory
      .getNodes($rootScope.activeSiteId)
      .then( function() {
        var nodes = NodeFactory.nodes;
        if (nodes.length > 0) {
          $scope.surveyPrompt = "Continue Survey";
        }
        map.showMap(true);
      });

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
