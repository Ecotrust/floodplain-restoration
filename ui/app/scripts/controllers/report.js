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

    // if (!$rootScope.userName) {
    //   $window.alert('You are not logged in. You will now be redirected to the login page.');
    //   $window.location = '/accounts/login/';
    // }

    map.showMap(false);

    $scope.awesomeThings = [
      'HTML5 Boilerplate',
      'AngularJS',
      'Karma'
    ];

    $rootScope.activeSiteId = $routeParams.siteId;
    $scope.pits = [];
    $scope.answers = {};

    var suitabilityCategories = {
      'low': {
        'minScore' : 0,
        'maxScore' : 33,
        'label' : 'Unsuitable',
        'class' : 'unsuitable'
      },
      'med' : {
        'minScore': 33,
        'maxScore': 66,
        'label': 'Moderately Suitable',
        'class': 'moderately-suitable'
      },
      'high' : {
        'minScore': 66,
        'maxScore': 100,
        'label': 'Highly Suitable',
        'class': 'highly-suitable'
      }
    };

    $scope.suitabilityScoreTypes = {
      'Site': 'Location',
      'Socio-Economic': 'Socio-Economic',
      'Landscape': 'Landscape',
      'Suitability': 'Overall'
    };

    $scope.contextMap = {
      'Site':'site',
      'Socio-Economic':'socio_economic',
      'Landscape':'landscape',
      'Suitability':'suitability'
    };

    QuestionFactory
      .getContexts()
      .then( function() {
        $scope.contextResponse = QuestionFactory.contexts;
        buildContext();
      });
    QuestionFactory
      .getCategories()
      .then( function() {
        $scope.categoryResponse = QuestionFactory.categories;
        buildContext();
      });

    function buildContext() {
      if ($scope.contextResponse && $scope.categoryResponse && $scope.questionResponse) {

        $scope.contextList = [];
        var suitabilityContext = [
          {
            'name': 'Suitability',
            'id': 4,
            'label': 'Overall',
            'components': [],
            'order': 0
          }
        ];
        $scope.contextResponse = suitabilityContext.concat($scope.contextResponse);
        $scope.contexts = {
          'Suitability': {
            'id': 4,
            'label': 'Overall',
            'components': []
          }
        };

        var contextMap = {};

        for (var i = 0; i < $scope.contextResponse.length; i++){
          contextMap[$scope.contextResponse[i].id.toString()] = $scope.contextResponse[i].name;
          $scope.contexts[$scope.contextResponse[i].name] = $scope.contextResponse[i];
          $scope.contexts[$scope.contextResponse[i].name].components = [];
          $scope.contexts[$scope.contextResponse[i].name].label = $scope.suitabilityScoreTypes[$scope.contextResponse[i].name];
          $scope.contextList.push($scope.contextResponse[i].name);
        }

        var categoryMap = {};

        for (var k = 0; k < $scope.questionResponse.length; k++) {
          var question = $scope.questionResponse[k];
          var catId = question.questionCategory.toString();
          if (!categoryMap.hasOwnProperty(catId)) {
            categoryMap[catId] = [];
          }
          categoryMap[catId].push(question.id);
        }

        for (var l = 0; l < $scope.categoryResponse.length; l++) {
          var category = $scope.categoryResponse[l];
          category.question_ids = categoryMap[category.id.toString()];
          var context = contextMap[category.context.toString()];
          $scope.contexts[context].components.push(category);
        }

        NodeFactory
          .getNodes($rootScope.activeSiteId)
          .then( function() {
            nodes = NodeFactory.nodes;
            $scope.numNodes = nodes.length;
            for (var i = 0; i < nodes.length; i++) {
              $scope.answers[nodes[i].question].value = nodes[i].value;
              $scope.answers[nodes[i].question].notes = nodes[i].notes;
              var choices = $scope.answers[nodes[i].question].choices;
              for (var choiceIndex in choices) {
                if (choices[choiceIndex].value === nodes[i].value) {
                  $scope.answers[nodes[i].question].answer = choices[choiceIndex].choice;
                }
              }
            }

            SiteFactory
              .getSuitabilityScores($rootScope.activeSiteId)
              .then( function() {

                $rootScope.suitability = SiteFactory.suitability;
                buildReport();
            
              });
          });
      }
    }

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

    function getBgColorClass(score) {
      for (var catKey in suitabilityCategories) {
        var cat = suitabilityCategories[catKey];
        if (score <= cat.maxScore && score >= cat.minScore) {
          return cat.class;
        }
      }
      return 'transparent';
    }

    function buildReport() {
      for (var key in $scope.suitabilityScoreTypes) {  //TODO: what if keys do not match?
        var score = $rootScope.suitability[$scope.contextMap[key]] * 100;
        $scope.contexts[key].score = score;
        $scope.contexts[key].rank = getRank(score);
        $scope.contexts[key].bgColorClass = getBgColorClass(score);

      }
    }

    var nodes = [];

    QuestionFactory
      .getQuestions()
      .then( function() {
        $scope.questionResponse = QuestionFactory.questions;
        $scope.numQuestions = $scope.questionResponse.length;  //QuestionFactory will likely change substantially
        $scope.maxQuestionId = $scope.questionResponse[$scope.questionResponse.length-1].id;
        for (var i = 0; i < $scope.questionResponse.length; i++) {
          $scope.answers[$scope.questionResponse[i].id] = $scope.questionResponse[i];
          $scope.answers[$scope.questionResponse[i].id].value = false;
          $scope.answers[$scope.questionResponse[i].id].notes = false;
          $scope.answers[$scope.questionResponse[i].id].answer = false;
          $scope.answers[$scope.questionResponse[i].id].displayId = i + 1;
        }
        buildContext();
        map.showMap(false);
      });

    $scope.alert = function (msg) {
      $window.alert(msg);
    };

    $scope.toggleCircleIconClass = function(iconId) {
      var icon = document.getElementById(iconId);
      if (icon.classList.contains('glyphicon-chevron-down')) {
        icon.className = icon.className.replace(/\bglyphicon-chevron-down\b/,'glyphicon-chevron-up');
      } else {
        icon.className = icon.className.replace(/\bglyphicon-chevron-up\b/,'glyphicon-chevron-down');
      }
    };

    $scope.selectComponent = function(componentId) {
      var component = document.getElementById(componentId);
      if (component.classList.contains('report-component-selected')) {
        component.className = component.className.replace(/\breport-component-selected\b/,'');
      } else {
        component.className = component.className + ' report-component-selected';
      }
    };

  });
