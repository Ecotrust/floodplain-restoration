'use strict';

/**
 * @ngdoc function
 * @name uiApp.controller:SurveyCtrl
 * @description
 * # SurveyCtrl
 * Controller of the uiApp
 */
angular.module('uiApp')
  .controller('SurveyCtrl', function ($scope, $routeParams, $rootScope, QuestionFactory) {
    $rootScope.showMap = true;
    
    var questionId = parseInt($routeParams.questionId, 10);

    $scope.siteId = $routeParams.siteId;
    $scope.question = QuestionFactory.getQuestion(questionId);

    var maxQuestionId = QuestionFactory.maxId();
    var minQuestionId = QuestionFactory.minId();
    
    $scope.showPrev = true;
    $scope.showPrev = true;

    $scope.nextQuestion = function() {
      var next = questionId + 1;
      $scope.showNext = true;
      if (next > maxQuestionId) {
        next = maxQuestionId;
        $scope.showNext = true;
        return "done";
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
  });
