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
                'coordinates': [
                  [
                    [
                      -122.70492553710936, 45.259422036351694
                    ],
                    [
                      -122.75161743164061, 45.09485258791474
                    ],
                    [
                      -122.57583618164062, 45.10260769705975
                    ],
                    [
                      -122.58132934570311, 45.24782097102814
                    ],
                    [
                      -122.70492553710936, 45.259422036351694
                    ]
                  ]
                ],
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
                'coordinates': [
                  [
                    [
                      -122.80517578125,
                      45.021126517829614
                    ],
                    [
                      -122.68981933593749,
                      45.06770141120143
                    ],
                    [
                      -122.64587402343751,
                      45.00753503123719
                    ],
                    [
                      -122.77496337890625,
                      44.941473354802504
                    ],
                    [
                      -122.80517578125,
                      45.021126517829614
                    ]
                  ]
                ],
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
          'coordinates': [
            [
              [
                [
                  -122.8216552734375, 45.40616374516014
                ],
                [
                  -122.9644775390625, 44.89479576469787
                ],
                [
                  -122.3712158203125, 44.902577996288876
                ],
                [
                  -122.3382568359375, 45.390735154248894
                ],
                [
                  -122.8216552734375, 45.40616374516014
                ]
              ]
            ]
          ],
          'type': 'MultiPolygon'
        },
      }
    ];

    // Public API
    return {
      getSites: function () {
        return sites;
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
        // console.log(site);
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
      }
      //getNextQuestionForSite

    };


  });
