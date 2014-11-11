'use strict';

/**
 * @ngdoc function
 * @name uiApp.controller:SiteeditCtrl
 * @description
 * # SiteeditCtrl
 * Controller of the uiApp
 */
angular.module('uiApp')
  .controller('SiteeditCtrl', function ($scope, $routeParams, $rootScope, SiteFactory) {
    map.showMap(true);

    //SiteFactory.setActiveSiteId($routeParams.siteId);
    //var site = SiteFactory.getActiveSite();

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

    SiteFactory.getSites().then(
      function() {
        $scope.sites = SiteFactory.sites.features;

        map.clear();

        if (isNewSite) {
          map.loadSites({type: 'FeatureCollection', features: []});
          map.addSite();

        } else {
          // set active site
          for (var i = SiteFactory.sites.features.length - 1; i >= 0; i--) {
            var site = SiteFactory.sites.features[i];
            if (site.id === activeSiteId) {
              $scope.site = site;
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
      if (isNewSite) {
        console.log('POST new Site');
      } else {
        console.log('PUT edited Site');
      }
      console.log('New geometry is ', map.getActiveSiteWkt());
      console.log('Save site ' + $scope.site.id);
      console.log('spinner on');
      console.log('If AJAX call is a success, update the SiteFactory singleton');
      console.log('spinner off');
    };

  });
