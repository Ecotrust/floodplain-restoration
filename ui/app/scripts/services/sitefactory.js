'use strict';

/**
 * @ngdoc service
 * @name uiApp.siteFactory
 * @description
 * # siteFactory
 * Factory in the uiApp.
 */
angular.module('uiApp')
  .factory('SiteFactory', function ($rootScope, $http) {

    var service = {};

    service.sites = [];

    service.getSites = function () {
        var promise = $http.get('/api/site.json');

        promise.success(function(data) {
          // full args
          // data, status, headers, config
          service.sites = data;
        });
        
        promise.error(function() {
          console.log('Could not fetch sites.json');
        });

        return promise;
      };

    service.deleteSite = function(activeSiteId) {
      console.log('Delete site ' + activeSiteId);
      // TODO return a promise
    };

    service.deleteSitePit = function(activeSiteId, pitId) {
      console.log('Delete pit ' + pitId + ' from site ' + activeSiteId);
      // TODO return a promise
    };

    service.postSite = function(site, wkt) {
      console.log('POST', site, wkt);
      // TODO return a promise
    };

    service.putSite = function(site, wkt) {
      console.log('PUT', site, wkt);
      // TODO return a promise
    };

    service.postSitePit = function(siteId, pit, wkt) {
      console.log('POST', pit, wkt);
      // TODO return a promise
    };

    service.putSitePit = function(siteId, pit, wkt) {
      console.log('PUT', pit, wkt);
      // TODO return a promise
    };

    return service;

  });
