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
    $rootScope.showMap = true;

    SiteFactory.setActiveSiteId($routeParams.siteId);
    var site = SiteFactory.getActiveSite();

    var newSite = false;
    if ($routeParams.siteId === 'new' || site === null) {
      newSite = true;
      site = {
        id: '',
        type: 'Feature',
        geometry: {}, // wkt
        properties: {}
      };
    }

    $scope.site = site;
      
    $scope.$on('activeFeatureWKT', function (event, wkt) {
      $scope.site.geometry = wkt;
    });

    $scope.save = function () {
      if (newSite) {
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

    // ----------------------- Map setup ------------------------------------//
    map.clear();
    if (newSite) {
      map.loadSites({type: 'FeatureCollection', features: []});
      map.addSite();
    } else {
      map.loadSites(SiteFactory.getActiveSiteCollection());
      map.editSite();
    } 
  });
