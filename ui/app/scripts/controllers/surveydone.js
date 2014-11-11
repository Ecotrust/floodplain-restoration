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
  .controller('SurveydoneCtrl', function ($scope, $routeParams, $rootScope, SiteFactory, QuestionFactory) {
    map.showMap(true);
    var questions = [];
    $scope.siteId = $routeParams.siteId;
    $scope.suitability = SiteFactory.getSuitabilityScores($routeParams.siteId); // /api/site/2/suitability.json
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
