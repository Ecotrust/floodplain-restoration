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
          'visible': true,
          'id': 'name',
          'order': 0,
          'type': 'text',
          'answers': []
        },
        {
          'question': 'Is hazardous waste present?',
          'visible': true,
          'id': 'contamination',
          'order': 10,
          'type': 'select',
          'answers': [
            {
              'label': 'I don\'t know',
              'value': 0.5
            },
            {
              'label': 'No, definitely not.',
              'value': 1
            },
            {
              'label': 'No, I don’t think so',
              'value': 0.8
            },
            {
              'label': 'Yes, but I do not know if it can be remediated.',
              'value': 0.4
            },
            {
              'label': 'Yes, and the cost and effort to remediate it is acceptable.',
              'value': 0.2
            },
            {
              'label': 'Yes, and it will be expensive and/or very difficult to remediate.',
              'value': 0
            }
          ]
        },
        {
          'question': 'Is the pit deeper than the adjacent river <u><i>thalweg</i></u>?',
          'visible': true,
          'id': 'adjacent_river_depth',
          'order': 30,
          'type': 'select',
          'answers': [
            {
              'label': 'I don\'t know',
              'value': 0.5
            },
            {
              'label': 'No',
              'value': 1
            },
            {
              'label': 'They are the same depth',
              'value': 0.51
            },
            {
              'label': 'Yes',
              'value': 0
            }
          ],
          'info': 'The thalweg of the river is the line of the lowest points within the channel, spanning the length of the river.'
        },
        {
          'question': 'What is the distance from the river to the pit edge?',
          'visible': true,
          'id': 'slope_dist',
          'order': 40,
          'type': 'select',
          'answers': [
            {
              'label': 'I don\'t know',
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
          'question': 'Are there any pit-adjacent levees?',
          'visible': true,
          'id': 'pit_levies',
          'order': 50,
          'type': 'select',
          'answers': [
            {
              'label': 'I don\'t know',
              'value': 0.5
            },
            {
              'label': 'Yes',
              'value': 1
            },
            {
              'label': 'No',
              'value': 0
            }
          ]
        },
        {
          'question': 'Select the answer that best describes the slope of the pit bank:',
          'visible': true,
          'id': 'bank_slope',
          'order': 70,
          'type': 'select',
          'answers': [
            {
              'label': 'I don\'t know',
              'value': 0.5
            },
            {
              'label': 'The bank slope is very shallow around most of the pit.',
              'value': 1
            },
            {
              'label': 'The bank slope is a mix of steep and shallow.',
              'value': 0.51
            },
            {
              'label': 'The bank slope is steep around most of the pit.',
              'value': 0
            }
          ]
        },
        {
          'question': 'What is the surface area of the pit?',
          'visible': false,
          'id': 'surface_area',
          'order': 90,
          'type': 'select',
          'answers': [
            {
              'label': 'I don\'t know',
              'value': 0.5
            },
            {
              'label': '< 5 acres',
              'value': 1
            },
            {
              'label': '5-20 acres',
              'value': 0.6
            },
            {
              'label': '20-30 acres',
              'value': 0.3
            },
            {
              'label': '> 30 acres',
              'value': 0
            }
          ]
        },
        {
          'question': 'Notes',
          'visible': true,
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
          'surface_area': 0.5
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
      map.loadOtherPits({
        type: 'FeatureCollection',
        features:$scope.site.properties.pit_set
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

    $scope.setPitArea = function (pit) {
      var acres = map.getActivePitArea();
      var areaVal = 0.5;
      if (acres <= 5){
        areaVal = 1;
      } else if (5 < acres && acres <= 20) {
        areaVal = 0.6;
      } else if (20 < acres && acres <= 30) {
        areaVal = 0.3;
      } else if (acres > 30) {
        areaVal = 0;
      }

      pit.properties.surface_area = areaVal;
    };

    $scope.save = function () {
      try {
        var pitWkt = map.getActivePitWkt;
        $scope.setPitArea($scope.pit);
        if (isNewPit) {
          SiteFactory
            .postSitePit(activeSiteId, $scope.pit, pitWkt())
            .then(function() {
              $location.path('/site/' + activeSiteId);
            });
        } else {
          SiteFactory
            .putSitePit(activeSiteId, $scope.pit, map.getActivePitWkt())
            .then(function() {
              $location.path('/site/' + activeSiteId);
            });
        }
      } catch (error){
        console.log(error);
        $window.alert('No Pit Drawn');
      }
    };

  });
