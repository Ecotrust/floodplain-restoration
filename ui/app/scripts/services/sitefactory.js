'use strict';

/**
 * @ngdoc service
 * @name uiApp.siteFactory
 * @description
 * # siteFactory
 * Factory in the uiApp.
 */
angular.module('uiApp')
  .factory('SiteFactory', function ($rootScope, $http, $window) {

    var service = {};

    service.sites = [];
    service.suitability = {};

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

      promise.success(function() {
        for (var i = service.sites.features.length - 1; i >= 0; i--) {
          var site = service.sites.features[i];
          if (site.id === activeSiteId) {
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
      var promise = $http.post(url, site);

      promise.success(function() {});

      promise.error( function(res) {
        console.log('ERROR', res);
        $window.alert('Could not create new property. Be sure you have all required fields filled in.');
      });

      return promise;
    };

    service.postSitePit = function(siteId, pit, wkt) {
      var url = '/api/pit';
      pit.geometry = wkt;  // replace geojson geom with wkt
      var promise = $http.post(url, pit);

      promise.success( function() {});

      promise.error( function(res) {
        console.log('ERROR', res);
        $window.alert('Could not create new pit. Be sure you have all required fields filled in.');
      });

      return promise;
    };
    // PUT
    service.putSite = function(site, wkt) {
      var url = '/api/site/' + site.id;
      site.geometry = wkt;  // replace geojson geom with wkt
      var promise = $http.put(url, site);

      promise.success( function() {});

      promise.error( function(res) {
        console.log('ERROR', res);
        $window.alert('Could not update property. Be sure you have all required fields filled in.');
      });

      return promise;
      // TODO return a promise
    };

    service.putSitePit = function(siteId, pit, wkt) {
      var url = '/api/pit/' + pit.id;
      pit.geometry = wkt;  // replace geojson geom with wkt
      var promise = $http.put(url, pit);

      promise.success( function() {});

      promise.error( function(res) {
        console.log('ERROR', res);
        $window.alert('Could not update pit. Be sure you have all required fields filled in.');
      });

      return promise;
    };

    service.getSuitabilityScores = function (siteId) {
      var url = '/api/site/' + siteId + '/suitability.json';
      var promise = $http.get(url);

      promise.success(function(data) {
        service.suitability= data;
      });

      promise.error(function() {
        console.log('Could not fetch suitability.json');
      });

      return promise;
    };

    return service;

  });
