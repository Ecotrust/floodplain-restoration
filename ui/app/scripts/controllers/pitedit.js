'use strict';

// Hack to make linter happy about global variables
if (false) { var map; }


/**
 * @ngdoc function
 * @name uiApp.controller:PiteditCtrl
 * @description
 * # PiteditCtrl
 * Controller of the uiApp
 */
angular.module('uiApp')
  .controller('PiteditCtrl', function ($scope, $routeParams, $rootScope, $location, $window, $sce, ContentFactory, SiteFactory) {

    if (!$rootScope.userName) {
      $window.alert('You are not logged in. You will now be redirected to the login page.');
      $window.location = '/accounts/login/';
    }

    map.showMap(true);

    $scope.pitEditDirections = $sce.trustAsHtml(ContentFactory.get('pitEditDirections'));

    var activeSiteId = parseInt($routeParams.siteId, 10);
    $rootScope.activeSiteId = activeSiteId;
    $scope.activePitId = false;
    var blankPit;
    var isNewPit = false;

    $scope.pitFormObj = {
      'form': [
        {
          'question': 'Name',
          'id': 'name',
          'order': 0,
          'type': 'text',
          'answers': []
        },
        {
          'question': 'Contamination',
          'id': 'contamination',
          'order': 10,
          'type': 'select',
          'answers': [
            {
              'label': 'Unknown',
              'value': 0.5
            },
            {
              'label': 'Clean',
              'value': 1
            },
            {
              'label': 'Contaminated',
              'value': 0
            }
          ]
        },
        {
          'question': 'Substrate',
          'id': 'substrate',
          'order': 20,
          'type': 'select',
          'answers': [
            {
              'label': 'Unknown',
              'value': 0.5
            },
            {
              'label': 'Good',
              'value': 1
            },
            {
              'label': 'Bad',
              'value': 0
            }
          ]
        },
        {
          'question': 'Adjacent River Depth',
          'id': 'adjacent_river_depth',
          'order': 30,
          'type': 'select',
          'answers': [
            {
              'label': 'Unknown',
              'value': 0.5
            },
            {
              'label': 'Deeper than pit (good?)',
              'value': 1
            },
            {
              'label': 'Same as pit',
              'value': 0.6
            },
            {
              'label': 'Shallower than pit (bad?)',
              'value': 0
            }
          ]
        },
        {
          'question': 'Slope Distance',
          'id': 'slope_dist',
          'order': 40,
          'type': 'select',
          'answers': [
            {
              'label': 'Unknown',
              'value': 0.5
            },
            {
              'label': 'Short (< 20 ft.)',
              'value': 1
            },
            {
              'label': 'Medium (20-80 ft.)',
              'value': 0.6
            },
            {
              'label': 'Long (> 80ft.)',
              'value': 0
            }
          ]
        },
        {
          'question': 'Pit Levees',
          'id': 'pit_levies',
          'order': 50,
          'type': 'select',
          'answers': [
            {
              'label': 'Unknown',
              'value': 0.5
            },
            {
              'label': 'Yes (Good?)',
              'value': 1
            },
            {
              'label': 'No (Bad?)',
              'value': 0
            }
          ]
        },
        {
          'question': 'Bedrock',
          'id': 'bedrock',
          'order': 60,
          'type': 'select',
          'answers': [
            {
              'label': 'Unknown',
              'value': 0.5
            },
            {
              'label': 'Yes (Good?)',
              'value': 1
            },
            {
              'label': 'No (Bad?)',
              'value': 0
            }
          ]
        },
        {
          'question': 'Bank Slope',
          'id': 'bank_slope',
          'order': 70,
          'type': 'select',
          'answers': [
            {
              'label': 'Unknown',
              'value': 0.5
            },
            {
              'label': 'Gentle (Good?)',
              'value': 1
            },
            {
              'label': 'Steep (Bad?)',
              'value': 0
            }
          ]
        },
        {
          'question': 'Pit Depth',
          'id': 'pit_depth',
          'order': 80,
          'type': 'select',
          'answers': [
            {
              'label': 'Unknown',
              'value': 0.5
            },
            {
              'label': 'Shallower than river (Good?)',
              'value': 1
            },
            {
              'label': 'About the same',
              'value': 0.6
            },
            {
              'label': 'Deeper than river (Bad?)',
              'value': 0
            }
          ]
        },
        {
          'question': 'Surface Area',
          'id': 'surface_area',
          'order': 90,
          'type': 'select',
          'answers': [
            {
              'label': 'Unknown',
              'value': 0.5
            },
            {
              'label': '< 1 acre',
              'value': 1
            },
            {
              'label': '> 1 acre',
              'value': 0
            }
          ]
        },
        {
          'question': 'Complexity',
          'id': 'complexity',
          'order': 100,
          'type': 'select',
          'answers': [
            {
              'label': 'Unknown',
              'value': 0.5
            },
            {
              'label': 'Simple',
              'value': 1
            },
            {
              'label': 'Complex',
              'value': 0
            }
          ]
        },
        {
          'question': 'Notes',
          'id': 'notes',
          'order': 110,
          'type': 'textarea',
          'answers': []
        }
      ]
    };

    if ($routeParams.pitId === undefined) {
      $scope.pitEditDirections = $sce.trustAsHtml(ContentFactory.get('pitCreateDirections'));
      isNewPit = true;
      blankPit = {
        id: '',
        type: 'Feature',
        geometry: {}, // wkt
        properties: {
          'notes': '',
          'name': '<new pit>',
          'site': activeSiteId,
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
      };
    } else {
      $scope.activePitId = parseInt($routeParams.pitId, 10);
    }
    
    $scope.pit = {};
    $scope.site = {};
    $scope.sites = [];

    SiteFactory.getSites().then( function() {
      $scope.sites = SiteFactory.sites.features;

      // set active site
      for (var i = SiteFactory.sites.features.length - 1; i >= 0; i--) {
        var site = SiteFactory.sites.features[i];
        if (site.id === activeSiteId) {
          $scope.site = site;
        }
      }

      map.clear();
      map.loadSites({
        type: 'FeatureCollection',
        features:[$scope.site]
      });

      if (isNewPit) {
        $scope.pit = blankPit;
        map.loadPits({
          type: 'FeatureCollection',
          features: []
        });
        map.addPit();
      } else {
        for (var j = $scope.site.properties.pit_set.length - 1; j >= 0; j--) {
          var pit = $scope.site.properties.pit_set[j];
          if (pit.id === $scope.activePitId) {
            $scope.pit = pit;
          }
        }
        map.loadPits({
          type: 'FeatureCollection',
          features: [$scope.pit]
        });
        map.editPit();
      }

      map.showMap(true);
    });

    var newPit = false;
    if ($routeParams.pitId === 'new' || $scope.pit === null) {
      newPit = true;
      $scope.pit = {
        id: '',
        type: 'Feature',
        geometry: {}, // wkt
        properties: {}
      };
    }

    $scope.$on('activeFeatureWKT', function (event, wkt) {
      $scope.pit.geometry = wkt;
    });

    $scope.save = function () {
      console.log('spinner on');
      try {
        var pitWkt = map.getActivePitWkt;
        if (isNewPit) {
          SiteFactory
            .postSitePit(activeSiteId, $scope.pit, pitWkt())
            .then(function() {
              console.log('spinner off');
              $location.path('/site/' + activeSiteId);
            });
        } else {
          SiteFactory
            .putSitePit(activeSiteId, $scope.pit, map.getActivePitWkt())
            .then(function() {
              console.log('spinner off');
              $location.path('/site/' + activeSiteId);
            });
        }
      } catch (error){
        console.log(error);
        $window.alert('No Pit Drawn');
      }
    };

  });
