'use strict';

if (false) {var map =  null;}

/**
 * @ngdoc function
 * @name uiApp.controller:ReportCtrl
 * @description
 * # ReportCtrl
 * Controller of the uiApp
 */
angular.module('uiApp')
  .controller('ReportCtrl', function ($scope, $rootScope, $window, $routeParams, SiteFactory, QuestionFactory, NodeFactory) {

    if (!$rootScope.userName) {
      $window.alert('You are not logged in. You will now be redirected to the login page.');
      $window.location = '/accounts/login/';
    }

    map.showMap(false);

    $scope.awesomeThings = [
      'HTML5 Boilerplate',
      'AngularJS',
      'Karma'
    ];

    $rootScope.activeSiteId = $routeParams.siteId;
    $scope.pits = [];

    var suitabilityCategories = {
      'low': {
        'minScore' : 0,
        'maxScore' : 33,
        'label' : 'Unsuitable',
        'bgColor': 'gray'
      },
      'med' : {
        'minScore': 33,
        'maxScore': 66,
        'label': 'Moderately Suitable',
        'bgColor': 'yellow'
      },
      'high' : {
        'minScore': 66,
        'maxScore': 100,
        'label': 'Highly Suitable',
        'bgColor': 'green'
      }
    };

    var suitabilityScoreTypes = {
      'site': 'Property',
      'socio_economic': 'Socio-Economic',
      'landscape': 'Landscape',
      'suitability': 'Overall'
    };

    $scope.context_list = ['site', 'socio_economic', 'landscape','suitability'];

    $scope.contexts = {
      'site': {
        'label': 'Property',
        'components': [
          {
            'name': 'Pit restorability',
            'question_ids': []
          },
          {
            'name': 'Practical, property-level restorability',
            'question_ids': [1,2,3]
          }
        ]
      },
      'socio_economic': {
        'label': 'Socio-Economic',
        'components': [
          {
            'name': 'Cost benefit',
            'question_ids': [8,9,10]
          },
          {
            'name': 'Threat to other areas / permutability',
            'question_ids': [4,5,6,7]
          }
        ]
      },
      'landscape': {
        'label': 'Landscape',
        'components': [
          {
            'name': 'Conservation value',
            'question_ids': [26,27]
          },
          {
            'name': 'Biotic conditions',
            'question_ids': [23,24,25]
          },
          {
            'name': 'Abiotic conditions',
            'question_ids': [19,20,21,22]
          },
          {
            'name': 'Geomorphic controls',
            'question_ids': [11,12,13,14]
          },
          {
            'name': 'Floodplain characteristics',
            'question_ids': [15,16,17,18]
          }
        ]
      },
      'suitability': {
        'label': 'Overall',
        'components': []
      },
    };

    SiteFactory
      .getSites()
      .then( function() {

        $scope.sites = SiteFactory.sites.features;

        // set active site
        for (var i = SiteFactory.sites.features.length - 1; i >= 0; i--) {
          var site = SiteFactory.sites.features[i];
          if (site.id === parseInt($rootScope.activeSiteId, 10)) {
            $scope.site = site;
            $scope.pits = site.properties.pit_set;
            break;
          }
        }

      });


    function getRank(score) {
      for (var catKey in suitabilityCategories) {
        var cat = suitabilityCategories[catKey];
        if (score <= cat.maxScore && score >= cat.minScore) {
          return cat.label;
        }
      }
      return null;
    }

    function getBgColor(score) {
      for (var catKey in suitabilityCategories) {
        var cat = suitabilityCategories[catKey];
        if (score <= cat.maxScore && score >= cat.minScore) {
          return cat.bgColor;
        }
      }
      return 'transparent';
    }

    function buildReport() {

      for (var key in suitabilityScoreTypes) {  //TODO: what if keys do not match?
        var score = $rootScope.suitability[key] * 100;
        $scope.contexts[key]['score'] = score;
        $scope.contexts[key]['rank'] = getRank(score);
        $scope.contexts[key]['bgColor'] = getBgColor(score);

      }

    };

    // $scope.questions = QuestionFactory.getQuestions();
    $scope.maxQuestionId = 2;  //QuestionFactory will likely change substantially
                                  //We'll hardcode this for now.

    var questions = [];
    var nodes = [];

    QuestionFactory
      .getQuestions()
      .then( function() {
        questions = QuestionFactory.questions;
        $scope.numQuestions = questions.length;  //QuestionFactory will likely change substantially
        $scope.maxQuestionId = questions[questions.length-1].id;

        NodeFactory
          .getNodes($rootScope.activeSiteId)
          .then( function() {
            nodes = NodeFactory.nodes;
            $scope.numNodes = nodes.length;

            SiteFactory
              .getSuitabilityScores($rootScope.activeSiteId)
              .then( function() {

                $rootScope.suitability = SiteFactory.suitability;
                buildReport();
            
            });
          });

        
        map.showMap(false);
      });

    $scope.alert = function (msg) {
      $window.alert(msg);
    }
  });
