'use strict';

/**
 * @ngdoc function
 * @name uiApp.controller:NavCtrl
 * @description
 * # NavCtrl
 * Controller of the uiApp
 */

angular.module('uiApp')
  .controller('NavCtrl', function ($scope, $rootScope, $window, $location, SiteFactory, QuestionFactory) {

    $scope.sites = [];
    $scope.site = {
      'properties': {
        'name': null
      }
    };
    
    $rootScope.$watch('activeSiteId', function() {

      $scope.site = {
        'properties': {
          'name': null
        }
      };

      if ($rootScope.userName) {

        SiteFactory
          .getSites()
          .then( function() {
            $scope.sites = SiteFactory.sites.features;

            // set active site
            for (var i = SiteFactory.sites.features.length - 1; i >= 0; i--) {
              var site = SiteFactory.sites.features[i];
              if (site.id === parseInt($rootScope.activeSiteId, 10)) {
                $scope.site = site;
              }
            }
          });
      }
    });
  
    $scope.questions = [];
    $scope.questionsObj = {};
    $scope.contexts = [];
    $scope.contextsObj = {};
    var componentQuestions = {};
    QuestionFactory
      .getContexts()
      .then( function() {
        $scope.contexts = QuestionFactory.contexts;
        QuestionFactory
        .getCategories()
        .then( function() {
          $scope.categories = QuestionFactory.categories;
          QuestionFactory
          .getQuestions()
          .then( function() {
            $scope.questions = QuestionFactory.questions;
            for (var question in $scope.questions) {
              var questionObj = $scope.questions[question];
              questionObj.surveyNumber = parseInt(question, 10);
              $scope.questionsObj[questionObj.id.toString()] = questionObj;
              if (!componentQuestions.hasOwnProperty(questionObj.questionCategory.toString())) {
                componentQuestions[questionObj.questionCategory.toString()] = [];
              }
              componentQuestions[questionObj.questionCategory.toString()].push({
                'id':questionObj.id,
                'surveyId':questionObj.surveyNumber + 1
              });
            }
            var collectedComponents = {};
            for (var componentId in $scope.categories) {
              var component = $scope.categories[componentId];
              if (!collectedComponents.hasOwnProperty(component.context.toString())) {
                collectedComponents[component.context.toString()] = [];
              }
              collectedComponents[component.context.toString()].push({
                'id':component.id,
                'name':component.name,
                'question_ids':componentQuestions[component.id.toString()]
              });
            }
            for (var contextId in $scope.contexts) {
              var context = $scope.contexts[contextId.toString()];
              $scope.contextsObj[context.name] = {
                'id' : context.id,
                'label' : context.name,
                'order' : context.order,
                'components' : collectedComponents[context.id.toString()]
              };
            }
          });
        });

      });
    

    $scope.href = function(link) {
      $location.path(link);
    };

    $scope.link = function(link) {
      $window.location = link;
    };

    // $scope.categoryQuestions = QuestionFactory.getCategoryQuestions();
  });
