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
    QuestionFactory
      .getQuestions()
      .then( function() {
        $scope.questions = QuestionFactory.questions;
        for (var question in $scope.questions) {
          $scope.questionsObj[$scope.questions[question].id.toString()] = $scope.questions[question];
        }
        $scope.contexts = QuestionFactory.contexts;
      });

    $scope.href = function(link) {
      $location.path(link);
    };

    $scope.link = function(link) {
      $window.location = link;
    };

    // $scope.categoryQuestions = QuestionFactory.getCategoryQuestions();
  });
