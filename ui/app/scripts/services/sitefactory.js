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

    return service;











    // var activeSiteId;
    // var activePitId;

    // var sites = dummydata.features; // TODO dummydata.js provides `dummydata` global, rm 'em

    // // Public API
    // return {
    //   getSites: function () {
    //     return sites;
    //   },

    //   getSitesCollection: function() {
    //     return {
    //       type: 'FeatureCollection',
    //       features: sites
    //     };
    //   },

    //   getPitsCollection: function() {
    //     var site = this.getActiveSite();
    //     return {
    //       type: 'FeatureCollection',
    //       features: site.properties.pit_set
    //     };
    //   },

    //   setActivePitId: function (pitId) {
    //     activePitId = parseInt(pitId, 10);
    //     var p = this.getSitePit(pitId);
    //     if (typeof(p) === 'undefined' || typeof(p) === null) {
    //       console.log('ERROR - can not edit pit ' + pitId + '... does not exist');
    //     } 
    //     $rootScope.$broadcast('activePitChanged', {});
    //   },

    //   getActivePit: function() {
    //     return this.getSitePit(activePitId);
    //   },

    //   getActivePitCollection: function() {
    //     var pit = this.getSitePit(activePitId);
    //     return {
    //       type: 'FeatureCollection',
    //       features: [pit]
    //     };
    //   },

    //   getActivePitId: function() {
    //     return activePitId;
    //   },

    //   getSitePit: function (pitId) {
    //     pitId = parseInt(pitId, 10);
    //     var site = this.getActiveSite();

    //     for (var i = site.properties.pit_set.length - 1; i >= 0; i--) {
    //       if (site.properties.pit_set[i].id === pitId) {
    //         return site.properties.pit_set[i];
    //       }
    //     }
    //     return null;
    //   },

    //   getSuitabilityScores: function () {
    //     // TODO http://localhost:8000/api/site/2/suitability.json
    //     //var site = this.getSite(siteId);

    //     var suitability = {
    //       'site': 0.27260624999999994,
    //       'landscape': 0.46898395525146463,
    //       'suitability': 0.43765438899978504,
    //       'socio_economic': 0.43198437499999986
    //     };

    //     return suitability;
    //   },

    //   setActiveSiteId: function(siteId) {
    //     siteId = parseInt(siteId, 10);
    //     if (siteId !== activeSiteId) {
    //       $rootScope.$broadcast('activeSiteChanged', {});
    //       activeSiteId = siteId;
    //     }

    //     var site = this.getActiveSite();
    //     if (site) {
    //       $rootScope.activeSiteId = site.id;
    //       $rootScope.activeSiteName = site.properties.name;
    //     } else {
    //       activeSiteId = null;
    //       $rootScope.activeSiteId = null;
    //       $rootScope.activeSiteName = null;
    //     }
    //   },

    //   getActiveSite: function () {
    //     for (var i = sites.length - 1; i >= 0; i--) {
    //       if (sites[i].id === activeSiteId) {
    //         return sites[i];
    //       }
    //     }
    //     return null;
    //   },

    //   getActiveSiteId: function() {
    //     return activeSiteId;
    //   },

    //   getActiveSiteCollection: function() {
    //     return {
    //       type: 'FeatureCollection',
    //       features: [this.getActiveSite()]
    //     };
    //   }
    //   //getNextQuestionForSite

    // };


  });
