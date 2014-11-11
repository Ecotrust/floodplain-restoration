'use strict';

/**
 * @ngdoc function
 * @name uiApp.controller:SurveyCtrl
 * @description
 * # SurveyCtrl
 * Controller of the uiApp
 */
angular.module('uiApp')
  .controller('SurveyCtrl', function ($scope, $routeParams, $rootScope, SiteFactory, QuestionFactory) {
    map.showMap(true);
    
    var questionId = parseInt($routeParams.questionId, 10);

    $scope.siteId = $routeParams.siteId;
    
    $scope.question = {};
    
    QuestionFactory
      .getQuestions()
      .then( function() {
        for (var i = QuestionFactory.questions.length - 1; i >= 0; i--) {
          var question = QuestionFactory.questions[i];
          if (question.id === questionId) {
            $scope.question = question;
          }
        }
        map.showMap(true);
      });

    $scope.numQuestions = 4;  //QuestionFactory will likely change substantially
                                  //We'll hardcode this for now.

    var maxQuestionId = 4;
    var minQuestionId = 0;
    
    $scope.showPrev = true;
    $scope.showPrev = true;

    $scope.nextQuestion = function() {
      var next = questionId + 1;
      $scope.showNext = true;
      if (next > maxQuestionId) {
        next = maxQuestionId;
        $scope.showNext = true;
        return 'done';
      }
      return next;
    };

    $scope.prevQuestion = function() {
      var prev = questionId - 1;
      $scope.showPrev = true;
      if (prev < minQuestionId) {
        prev = minQuestionId;
        $scope.showPrev = false;
      }
      return prev;
    };

    // map.clear();
    // map.loadSites(SiteFactory.getActiveSiteCollection());
    // map.loadPits(SiteFactory.getPitsCollection());
  });
