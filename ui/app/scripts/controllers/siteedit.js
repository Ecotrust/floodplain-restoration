'use strict';

// Hack to make linter happy about global variables
if (false) { var map; }

/**
 * @ngdoc function
 * @name uiApp.controller:SiteeditCtrl
 * @description
 * # SiteeditCtrl
 * Controller of the uiApp
 */
angular.module('uiApp')
  .controller('SiteeditCtrl', function ($scope, $routeParams, $location, $rootScope, $window, $sce, ContentFactory, SiteFactory) {

    if (!$rootScope.userName) {
      alert('You are not logged in. You will now be redirected to the login page.');
      $window.location = '/accounts/login/';
    }

    $scope.siteEditDirections = $sce.trustAsHtml(ContentFactory.get('siteCreateDirections'));
    $scope.siteEditDefinitions = $sce.trustAsHtml(ContentFactory.get('siteEditDefinitions'));
    $scope.title = 'Creating A New Property'

    map.showMap(true);

    $scope.sites = [];
    $scope.site = {};
    var isNewSite = false;
    var activeSiteId;
    var blankSite;

    if ($routeParams.siteId === undefined) {
      activeSiteId = null;
      isNewSite = true;
      blankSite = {
        id: '',
        type: 'Feature',
        geometry: {}, // wkt
        properties: {}
      };
    } else {
      activeSiteId = parseInt($routeParams.siteId, 10);
    }
    $rootScope.activeSiteId = activeSiteId;

    SiteFactory.getSites().then(
      function() {
        $scope.sites = SiteFactory.sites.features;

        map.clear();

        if (isNewSite) {
          map.loadSites({type: 'FeatureCollection', features: []});
          map.addSite(blankSite);

        } else {
          // set active site
          for (var i = SiteFactory.sites.features.length - 1; i >= 0; i--) {
            var site = SiteFactory.sites.features[i];
            if (site.id === activeSiteId) {
              $scope.site = site;
              $scope.title = 'Editing <span class="label label-info">'+ site.properties.name + '</span>'
              $scope.siteEditDirections = $sce.trustAsHtml(ContentFactory.get('siteEditDirections'));
            }
          }

          map.loadSites({
            type: 'FeatureCollection',
            features:[$scope.site]
          });
          map.editSite();
        }
        map.showMap(true);
      }
    );

    $scope.$on('activeFeatureWKT', function (event, wkt) {
      $scope.site.geometry = wkt;
    });

    $scope.save = function () {
      console.log('spinner on');
      if (isNewSite) {
        SiteFactory
          .postSite($scope.site, map.getActiveSiteWkt())
          .then(function() {
            console.log('spinner off (POST new site complete!)');
            $location.path('/sites');
          });
      } else {
        SiteFactory
          .putSite($scope.site, map.getActiveSiteWkt())
          .then(function() {
            console.log('spinner off (PUT existing site complete!)');
            $location.path('/sites');
          });
      }
    };

  });
