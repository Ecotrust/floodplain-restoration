'use strict';

/**
 * @ngdoc function
 * @name uiApp.controller:SurveydoneCtrl
 * @description
 * # SurveydoneCtrl
 * Controller of the uiApp
 */
if(false) {
  var map=null;
}

angular.module('uiApp')
  .controller('SurveydoneCtrl', function ($scope, $routeParams, $rootScope, $window, SiteFactory, QuestionFactory) {

    if (!$rootScope.userName) {
      alert('You are not logged in. You will now be redirected to the login page.');
      $window.location = '/accounts/login/';
    }

    map.showMap(true);
    var questions = [];
    $rootScope.activeSiteId = $routeParams.siteId;

    SiteFactory
      .getSuitabilityScores($routeParams.siteId)
      .then( function() {
        $rootScope.suitability = SiteFactory.suitability;
      });
    // $scope.questions = QuestionFactory.getQuestions();
    $scope.maxQuestionId = 2;  //QuestionFactory will likely change substantially
                                  //We'll hardcode this for now.

    QuestionFactory
      .getQuestions()
      .then( function() {
        questions = QuestionFactory.questions;
        $scope.numQuestions = questions.length;  //QuestionFactory will likely change substantially
        $scope.maxQuestionId = questions[questions.length-1].id;
        
        map.showMap(true);
      });

    // map.clear();
    // map.loadSites(SiteFactory.getActiveSiteCollection());
    // map.loadPits(SiteFactory.getPitsCollection());
  });
