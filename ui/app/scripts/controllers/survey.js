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
    
    var questionDisplayId = parseInt($routeParams.questionId, 10);

    $rootScope.activeSiteId = $routeParams.siteId;
    
    var questions = [];
    $scope.question = {};
    $scope.numQuestions = questions.length;
    // var maxQuestionId = 999;
    var minQuestionId = 0;

    var nodes = [];
    $scope.node = {
      notes: '',
      site: $rootScope.activeSiteId,
      question: questionDisplayId,
      value: null
    };

    $scope.numNodes = 0;
    $scope.nodeVal = null;
    $scope.nodeNotes = null;
    $scope.newNode = true;
    $scope.hasExternalLink = false;
    $scope.hasDownload = false;
    $scope.hasImage = false;
    
    QuestionFactory
      .getQuestions()
      .then( function() {
        questions = QuestionFactory.questions;
        $scope.numQuestions = questions.length;
        $scope.question = questions[questionDisplayId - 1];
        $scope.question.displayId = questionDisplayId;
        $scope.node.question = $scope.question.id;
        if ($scope.question.externalLink !== null) {
          $scope.hasExternalLink = true;
        }
        if ($scope.question.supplement !== "") {
          $scope.hasDownload = true;
        }
        if ($scope.question.image !== "") {
          $scope.hasImage = true;
        }
        map.showMap(true);
        NodeFactory
          .getNodes($rootScope.activeSiteId)
          .then( function() {
            nodes = NodeFactory.nodes;
            $scope.numNodes = nodes.length;
            for (var i = NodeFactory.nodes.length - 1; i >=0; i--) {
              var node = NodeFactory.nodes[i];
              if (node.question === $scope.question.id && node.site === parseInt($rootScope.activeSiteId, 10)) {
                $scope.node = node;
                $scope.nodeVal = node.value;
                $scope.nodeNotes = node.notes;
                $scope.newNode = false;
              }
            }
            map.showMap(true);
          });
      });



    $scope.showPrev = true;

    $scope.submitForm = function() {
      var valueChecked = false;
      var formElements = document.getElementById('pitForm').elements;
      for (var i = 0; i < formElements.length; i++) {
        if (formElements[i].type === 'radio' && formElements[i].checked){
          valueChecked=true;
        }
      }
      var nextQuestion = $scope.nextQuestion();
      if ($scope.nodeVal === null || !valueChecked) {
        //   alert('Please answer the question before moving on. If you are unable to answer the question, select "I don\'t know."');
        $location.path('site/' + $rootScope.activeSiteId + '/survey/' + nextQuestion);
      } else {
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
      var next = questionDisplayId + 1;
      $scope.showNext = true;
      if (next > $scope.numQuestions) {
        $scope.showNext = true;
        return 'done';
      }
      return next;
    };

    $scope.prevQuestion = function() {
      var prev = questionDisplayId - 1;
      $scope.showPrev = true;
      if (prev < minQuestionId) {
        prev = minQuestionId;
        $scope.showPrev = false;
      }
      return prev;
    };

    $scope.toggleCircleIconClass = function(iconId) {
      var icon = document.getElementById(iconId);
      if (icon.classList.contains('glyphicon-plus-sign')) {
        icon.className = icon.className.replace(/\bglyphicon-plus-sign\b/,'glyphicon-minus-sign');
      } else {
        icon.className = icon.className.replace(/\bglyphicon-minus-sign\b/,'glyphicon-plus-sign');
      }
    };

  });
