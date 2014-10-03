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
                'type': 'Polygon',
                'coordinates': [
                  [
                    [
                      -401141.524441,
                      273728.550073
                    ],
                    [
                      -587036.37723,
                      68183.127842
                    ],
                    [
                      -489196.98102,
                      -39441.75797
                    ],
                    [
                      -117407.27545,
                      87752.476806
                    ],
                    [
                      -401141.524441,
                      273728.550073
                    ]
                  ]
                ]
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
          'type': 'Polygon',
          'coordinates': [
            [
              [
                [
                  -401141.524441,
                  273728.550073
                ],
                [
                  -587036.37723,
                  68183.127842
                ],
                [
                  -489196.98102,
                  -39441.75797
                ],
                [
                  -117407.27545,
                  87752.476806
                ],
                [
                  -401141.524441,
                  273728.550073
                ]
              ]
            ]
          ]
        }
      }
    ];

    // Public API
    return {
      getSites: function () {
        return sites;
      },

      getSitePit: function (siteId, pitId) {
        pitId = parseInt(pitId, 10);
        var site = this.getSite(siteId);

        for (var i = site.properties.pit_set.length - 1; i >= 0; i--) {
          if (site.properties.pit_set[i].id === pitId) {
            return site.properties.pit_set[i];
          }
        }
        return null;
      },

      getSite: function (siteId) {
        siteId = parseInt(siteId, 10);
        for (var i = sites.length - 1; i >= 0; i--) {
          if (sites[i].id === siteId) {
            $rootScope.siteId = siteId;
            $rootScope.siteName = sites[i].properties.name;
            return sites[i];
          }
        }
        return null;
      }



      //getNextQuestionForSite

    };


  });
