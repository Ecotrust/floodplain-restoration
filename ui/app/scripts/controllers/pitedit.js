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
  .controller('PiteditCtrl', function ($scope, $routeParams, $rootScope, $location, $window, $sce, ContentFactory, SiteFactory, QuestionFactory) {

    if (!$rootScope.userName) {
      $window.alert('You are not logged in. You will now be redirected to the login page.');
      $window.location = '/accounts/login/';
    }

    map.showMap(true);

    $scope.pitEditDirections = $sce.trustAsHtml(ContentFactory.get('pitEditDirections'));
    QuestionFactory
      .getPitQuestions()
      .then( function() {
        $scope.pitQuestions = QuestionFactory.pitQuestions;
      });

    var activeSiteId = parseInt($routeParams.siteId, 10);
    $rootScope.activeSiteId = activeSiteId;
    $scope.activePitId = false;
    var blankPit;
    var isNewPit = false;

    var questionDefaults = {
      'contamination': 0.75,
      'adjacent_river_depth': 0.75,
      'slope_dist': 0.9,
      'pit_levies': 0.85,
      'bank_slope': 0.75,
      'surface_area': 0.5
    };


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
          // 'question': $scope.pitQuestions?$scope.pitQuestions.contamination.question:'Is hazardous waste present?',
          'question': 'Is hazardous waste present?',
          'visible': true,
          'id': 'contamination',
          'order': 10,
          'type': 'select',
          'answers': [
            {
              'label': 'I don\'t know',
              'value': questionDefaults.contamination
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
              'label': 'Yes, and the cost and effort to remediate it is acceptable.',
              'value': 0.7
            },
            {
              'label': 'Yes, but I do not know if it can be remediated.',
              'value': 0.5
            },
            {
              'label': 'Yes, and it will be expensive and/or very difficult to remediate.',
              'value': 0.0
            }
          ]
        },
        {
          'question': 'Is the pit more than twice as deep as the adjacent river <u><i>thalweg</i></u>?',
          'visible': true,
          'id': 'adjacent_river_depth',
          'order': 30,
          'type': 'select',
          'answers': [
            {
              'label': 'I don\'t know',
              'value': questionDefaults.adjacent_river_depth
            },
            {
              'label': 'No',
              'value': 1
            },
            {
              'label': 'They are the same depth',
              'value': 0.7
            },
            {
              'label': 'Yes',
              'value': 0.0
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
              'value': questionDefaults.slope_dist
            },
            {
              'label': 'Short (< 250 ft.)',
              'value': 1
            },
            {
              'label': 'Medium (250-1000 ft.)',
              'value': 0.6
            },
            {
              'label': 'Long (> 1000 ft.)',
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
              'value': questionDefaults.pit_levies
            },
            {
              'label': 'No',
              'value': 1
            },
            {
              'label': 'Yes',
              'value': 0.0
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
              'value': questionDefaults.bank_slope
            },
            {
              'label': 'The bank slope is very shallow around most of the pit.',
              'value': 1
            },
            {
              'label': 'The bank slope is a mix of steep and shallow.',
              'value': 0.7
            },
            {
              'label': 'The bank slope is steep around most of the pit.',
              'value': 0.0
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


    // var pitQuestionList = [];
    // var keys = Object.keys($rootScope.pitQuestions);
    // for (var i = 0; i < keys.length; i++){
    //   var key = keys[i];
    //   pitQuestionList.push($rootScope.pitQuestions[key]);
    // }
    //
    // pitQuestionList.sort(function(a,b) {
    //   return a.order - b.order;
    // });

    // $scope.pitFormObj = {
    //   'form': pitQuestionList
    // };

    // $scope.pitFormObj = {
    //   'form': [
    //     'name',
    //     'contamination',
    //     'adjacent_river_depth',
    //     'slope_dist',
    //     'pit_levies',
    //     'bank_slope',
    //     'surface_area'
    //   ]
    // };



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
          'contamination': questionDefaults.contamination,
          'adjacent_river_depth': questionDefaults.adjacent_river_depth,
          'slope_dist': questionDefaults.slope_dist,
          'pit_levies': questionDefaults.pit_levies,
          'bank_slope': questionDefaults.bank_slope,
          'surface_area': questionDefaults.surface_area
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
