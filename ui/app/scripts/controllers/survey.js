'use strict';

/**
 * @ngdoc function
 * @name uiApp.controller:SurveyCtrl
 * @description
 * # SurveyCtrl
 * Controller of the uiApp
 */

if(false) {
  var map = null;
}

angular.module('uiApp')
  .controller('SurveyCtrl', function ($scope, $routeParams, $rootScope, SiteFactory, QuestionFactory, NodeFactory) {
    map.showMap(true);
    
    var questionId = parseInt($routeParams.questionId, 10);

    $scope.siteId = $routeParams.siteId;
    
    var questions = [];
    $scope.question = {};
    $scope.numQuestions = questions.length;
    var maxQuestionId = 999;
    var minQuestionId = 0;

    var nodes = [];
    $scope.node = {};
    $scope.numNodes = 0;
    
    QuestionFactory
      .getQuestions()
      .then( function() {
        questions = QuestionFactory.questions;
        $scope.numQuestions = questions.length;  //QuestionFactory will likely change substantially
        maxQuestionId = questions[questions.length-1].id;
        for (var i = QuestionFactory.questions.length - 1; i >= 0; i--) {
          var question = QuestionFactory.questions[i];
          if (question.id === questionId) {
            $scope.question = question;
          }
        }
        map.showMap(true);
      });

    NodeFactory
      .getNodes()
      .then( function() {
        nodes = NodeFactory.nodes;
        $scope.numNodes = nodes.length;
        for (var i = NodeFactory.nodes.length - 1; i >=0; i--) {
          var node = NodeFactory.nodes[i];
          if (node.question === questionId && node.site === parseInt($scope.siteId, 10)) {
            $scope.node = node;
          }
        }
        map.showMap(true);
      });


    $scope.showPrev = true;
    $scope.showPrev = true;

    $scope.nextQuestion = function() {
      var next = questionId + 1;
      $scope.showNext = true;
      if (next > $scope.numQuestions) {
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
