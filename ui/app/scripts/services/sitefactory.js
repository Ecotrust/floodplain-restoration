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
      var url = '/api/site/' + activeSiteId;
      console.log('DELETE', url);

      var promise = $http.delete(url);
      return promise;
    };

    service.deleteSitePit = function(activeSiteId, pitId) {
      var url = '/api/pit/' + pitId;
      console.log('DELETE', url);

      var promise = $http.delete(url);
      return promise;
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

    service.getSuitabilityScores = function () {
      // TODO http://localhost:8000/api/site/2/suitability.json
      //var site = this.getSite(siteId);

      var suitability = {
        'site': 0.27260624999999994,
        'landscape': 0.46898395525146463,
        'suitability': 0.43765438899978504,
        'socio_economic': 0.43198437499999986
      };

      return suitability;
    };

    return service;

  });
