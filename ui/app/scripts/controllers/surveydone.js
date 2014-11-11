'use strict';

/**
 * @ngdoc function
 * @name uiApp.controller:SurveydoneCtrl
 * @description
 * # SurveydoneCtrl
 * Controller of the uiApp
 */
angular.module('uiApp')
  .controller('SurveydoneCtrl', function ($scope, $routeParams, $rootScope, SiteFactory) {
    map.showMap(true);
    $scope.siteId = $routeParams.siteId;
    $scope.suitability = SiteFactory.getSuitabilityScores($routeParams.siteId); // /api/site/2/suitability.json
    // $scope.questions = QuestionFactory.getQuestions();
    $scope.numQuestions = 2;  //QuestionFactory will likely change substantially
                                  //We'll hardcode this for now.

    // map.clear();
    // map.loadSites(SiteFactory.getActiveSiteCollection());
    // map.loadPits(SiteFactory.getPitsCollection());
  });
