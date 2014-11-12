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

    // Delete
    service.deleteSite = function(activeSiteId) {
      var url = '/api/site/' + activeSiteId;

      var promise = $http.delete(url);

      promise.success(function(data) {
        for (var i = service.sites.features.length - 1; i >= 0; i--) {
          var site = service.sites.features[i];
          if (site.id == activeSiteId) {
            service.sites.features.splice(i, 1); // pop it off the list
          }
        }
      });

      promise.error(function() {
        console.log('Could not DELETE', url);
      });

      return promise;
    };

    service.deleteSitePit = function(activeSiteId, pitId) {
      var url = '/api/pit/' + pitId;

      // TODO service.getSiteById()
      var siteIndex;
      for (var i = service.sites.features.length - 1; i >= 0; i--) {
        var site = service.sites.features[i];
        if (site.id == activeSiteId) {
          siteIndex = i;
        }
      }

      var promise = $http.delete(url);

      promise.success(function() {
        for (var i = service.sites.features[siteIndex].properties.pit_set.length - 1; i >= 0; i--) {
          var pit = service.sites.features[siteIndex].properties.pit_set[i];
          if (pit.id === pitId) {
            // Pop it off the array
            service.sites.features[siteIndex].properties.pit_set.splice(i, 1);
          }
        }
      });
              
      return promise;
    };

    // Create New / POST
    service.postSite = function(site, wkt) {
      var url = '/api/site';
      site.geometry = wkt;  // replace geojson geom with wkt
      console.log("POST", url, site);
      var promise = $http.post(url, site);
      // *************************** see TODO
      return promise;
    };

    service.postSitePit = function(siteId, pit, wkt) {
      var url = '/api/pit';
      pit.geometry = wkt;  // replace geojson geom with wkt
      console.log("POST", url, pit);
      var promise = $http.post(url, pit);
      // *************************** see TODO
      return promise;
    };

    // PUT
    service.putSite = function(site, wkt) {
      console.log('PUT', site, wkt);
      // TODO return a promise
    };

    service.putSitePit = function(siteId, pit, wkt) {
      console.log('PUT', pit, wkt);
      // TODO return a promise
    };

    service.getSuitabilityScores = function () {
      // TODO
      // GET from e.g. /api/site/2/suitability.json
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
