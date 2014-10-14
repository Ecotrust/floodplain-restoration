'use strict';

/**
 * @ngdoc service
 * @name uiApp.siteFactory
 * @description
 * # siteFactory
 * Factory in the uiApp.
 */
angular.module('uiApp')
  .factory('SiteFactory', function ($rootScope) {

    var activeSiteId;
    var activePitId;

    var sites = [
      {
        'id': 2,
        'type': 'Feature',
        'properties': {
          'name': 'Willamette Confluence',
          'pit_set' : [
            {
              'id': 2,
              'type': 'Feature',
              'geometry': {
                'coordinates': [ [ [ -13658685.458334716036916, 5653282.611971635371447 ], [ -13654710.732863888144493, 5665206.788384127430618 ], [ -13639423.327206851914525, 5663678.047818418592215 ], [ -13639423.327206851914525, 5648084.894048248417675 ], [ -13658685.458334716036916, 5653282.611971635371447 ] ] ],
                'type': 'Polygon'
              },
              'properties': {
                'user': 'dummyuser',
                'name': 'testpit',
                'notes': '',
                'date_created': '2014-09-29T20:13:17.927Z',
                'date_modified': '2014-09-29T20:13:17.927Z',
                'site': 2,
                'contamination': 0.5,
                'substrate': 0.5,
                'adjacent_river_depth': 0.5,
                'slope_dist': 0.5,
                'pit_levies': 0.5,
                'bedrock': 0.5,
                'bank_slope': 0.5,
                'pit_depth': 0.5,
                'surface_area': 0.5,
                'complexity': 0.5
              }
            },
            {
              'id': 3,
              'type': 'Feature',
              'geometry': {
                'coordinates': [ [ [ -13680087.826254565268755, 5619038.823299874551594 ], [ -13679782.078141424804926, 5631574.495938645675778 ], [ -13667857.901728937402368, 5633103.236504349857569 ], [ -13667857.901728937402368, 5616287.090281615033746 ], [ -13680087.826254565268755, 5619038.823299874551594 ] ] ],
                'type': 'Polygon'
              },
              'properties': {
                'user': 'dummyuser',
                'name': 'another testpit',
                'notes': '',
                'date_created': '2014-09-29T20:13:17.927Z',
                'date_modified': '2014-09-29T20:13:17.927Z',
                'site': 2,
                'contamination': 0.5,
                'substrate': 0.5,
                'adjacent_river_depth': 0.5,
                'slope_dist': 0.5,
                'pit_levies': 0.5,
                'bedrock': 0.5,
                'bank_slope': 0.5,
                'pit_depth': 0.5,
                'surface_area': 0.5,
                'complexity': 0.5
              }
            }
          ],
          'inputnode_set': [
            {
              'user': 'dummyuser',
              'id': 2,
              'name': '',
              'notes': '',
              'date_created': '2014-09-29T20:13:17.938Z',
              'date_modified': '2014-09-29T20:13:17.938Z',
              'site': 2,
              'question': 1,
              'value': 0.3
            }
          ]
        },
        'geometry': {
          'coordinates': [ [ [ [ -13692317.750780193135142, 5650225.130840227939188 ], [ -13684674.047951675951481, 5694864.355358773842454 ], [ -13621689.936644691973925, 5674684.979891482740641 ], [ -13631168.128152053803205, 5585100.782741256989539 ], [ -13713414.370586901903152, 5593967.478022339753807 ], [ -13692317.750780193135142, 5650225.130840227939188 ] ] ] ],
          'type': 'MultiPolygon'
        },
      },
      {
        'id': 4,
        'type': 'Feature',
        'properties': {
          'name': 'Another Site',
          'pit_set' : [
            {
              'id': 2,
              'type': 'Feature',
              'geometry': {
                'coordinates': [ [ [ -13758685.458334716036916, 5653282.611971635371447 ],
                                   [ -13754710.732863888144493, 5665206.788384127430618 ],
                                   [ -13739423.327206851914525, 5663678.047818418592215 ],
                                   [ -13739423.327206851914525, 5648084.894048248417675 ],
                                   [ -13758685.458334716036916, 5653282.611971635371447 ] ] ],
                'type': 'Polygon'
              },
              'properties': {
                'user': 'dummyuser',
                'name': 'testpit',
                'notes': '',
                'date_created': '2014-09-29T20:13:17.927Z',
                'date_modified': '2014-09-29T20:13:17.927Z',
                'site': 2,
                'contamination': 0.5,
                'substrate': 0.5,
                'adjacent_river_depth': 0.5,
                'slope_dist': 0.5,
                'pit_levies': 0.5,
                'bedrock': 0.5,
                'bank_slope': 0.5,
                'pit_depth': 0.5,
                'surface_area': 0.5,
                'complexity': 0.5
              }
            }
          ],
          'inputnode_set': [
            {
              'user': 'dummyuser',
              'id': 2,
              'name': '',
              'notes': '',
              'date_created': '2014-09-29T20:13:17.938Z',
              'date_modified': '2014-09-29T20:13:17.938Z',
              'site': 2,
              'question': 1,
              'value': 0.3
            }
          ]
        },
        'geometry': {
          'coordinates': [ [ [ [ -13792317, 5650225 ], [ -13784674, 5694864 ], [ -13721689, 5674684 ],
                               [ -13739423, 5585100 ], [ -13813414, 5593967 ], [ -13792317, 5650225 ] ] ] ],
          'type': 'MultiPolygon'
        },
      }
    ];

    // Public API
    return {
      getSites: function () {
        return sites;
      },

      getSitesCollection: function() {
        return {
          type: 'FeatureCollection',
          features: sites
        };
      },

      getPitsCollection: function() {
        var site = this.getActiveSite();
        return {
          type: 'FeatureCollection',
          features: site.properties.pit_set
        };
      },

      setActivePitId: function (pitId) {
        activePitId = parseInt(pitId, 10);
        var p = this.getSitePit(pitId);
        if (typeof(p) === 'undefined' || typeof(p) === null) {
          console.log('ERROR - can not edit pit ' + pitId + '... does not exist');
        } 
        $rootScope.$broadcast('activePitChanged', {});
      },

      getActivePit: function() {
        return this.getSitePit(activePitId);
      },

      getActivePitCollection: function() {
        var pit = this.getSitePit(activePitId);
        return {
          type: 'FeatureCollection',
          features: [pit]
        };
      },

      getActivePitId: function() {
        return activePitId;
      },

      getSitePit: function (pitId) {
        pitId = parseInt(pitId, 10);
        var site = this.getActiveSite();

        for (var i = site.properties.pit_set.length - 1; i >= 0; i--) {
          if (site.properties.pit_set[i].id === pitId) {
            return site.properties.pit_set[i];
          }
        }
        return null;
      },

      getSuitabilityScores: function () {
        // TODO http://localhost:8000/api/site/2/suitability.json
        //var site = this.getSite(siteId);

        var suitability = {
          'site': 0.27260624999999994,
          'landscape': 0.46898395525146463,
          'suitability': 0.43765438899978504,
          'socio_economic': 0.43198437499999986
        };

        return suitability;
      },

      setActiveSiteId: function(siteId) {
        siteId = parseInt(siteId, 10);
        if (siteId !== activeSiteId) {
          $rootScope.$broadcast('activeSiteChanged', {});
          activeSiteId = siteId;
        }

        var site = this.getActiveSite();
        if (site) {
          $rootScope.activeSiteId = site.id;
          $rootScope.activeSiteName = site.properties.name;
        } else {
          activeSiteId = null;
          $rootScope.activeSiteId = null;
          $rootScope.activeSiteName = null;
        }
      },

      getActiveSite: function () {
        for (var i = sites.length - 1; i >= 0; i--) {
          if (sites[i].id === activeSiteId) {
            return sites[i];
          }
        }
        return null;
      },

      getActiveSiteId: function() {
        return activeSiteId;
      },

      getActiveSiteCollection: function() {
        return {
          type: 'FeatureCollection',
          features: [this.getActiveSite()]
        };
      }
      //getNextQuestionForSite

    };


  });
