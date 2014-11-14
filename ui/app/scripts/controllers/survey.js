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
  .controller('SurveyCtrl', function ($scope, $routeParams, $rootScope, $location, $window, SiteFactory, QuestionFactory, NodeFactory) {

    if (!$rootScope.userName) {
      alert('You are not logged in. You will now be redirected to the login page.');
      $window.location = '/accounts/login/';
    }

    map.showMap(true);
    
    var questionId = parseInt($routeParams.questionId, 10);

    $rootScope.activeSiteId = $routeParams.siteId;
    
    var questions = [];
    $scope.question = {};
    $scope.numQuestions = questions.length;
    var maxQuestionId = 999;
    var minQuestionId = 0;

    var nodes = [];
    $scope.node = {
      notes: '',
      site: $rootScope.activeSiteId,
      question: questionId,
      value: null
    };

    $scope.numNodes = 0;
    $scope.nodeVal = null;
    $scope.nodeNotes = null;
    $scope.newNode = true;
    
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
      .getNodes($rootScope.activeSiteId)
      .then( function() {
        nodes = NodeFactory.nodes;
        $scope.numNodes = nodes.length;
        for (var i = NodeFactory.nodes.length - 1; i >=0; i--) {
          var node = NodeFactory.nodes[i];
          if (node.question === questionId && node.site === parseInt($rootScope.activeSiteId, 10)) {
            $scope.node = node;
            $scope.nodeVal = node.value;
            $scope.nodeNotes = node.notes;
            $scope.newNode = false;
          }
        }
        map.showMap(true);
      });


    $scope.showPrev = true;
    $scope.showPrev = true;

    $scope.submitForm = function() {
      if ($scope.nodeVal === null) {
        alert('Please answer the question before moving on. If you are unable to answer the question, select "Not Sure".');
      } else {
        var nextQuestion = $scope.nextQuestion();
        $scope.node.value = $scope.nodeVal;
        $scope.node.notes = $scope.nodeNotes;
        if ($scope.newNode){
          NodeFactory
            .postNode($scope.node)
            .then( function () {
              $location.path('site/' + $rootScope.activeSiteId + '/survey/' + nextQuestion);
            });
        } else {
          NodeFactory
            .putNode($scope.node)
            .then( function () {
              $location.path('site/' + $rootScope.activeSiteId + '/survey/' + nextQuestion);
            });
        }
      }
    };

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
