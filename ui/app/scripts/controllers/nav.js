'use strict';

/**
 * @ngdoc function
 * @name uiApp.controller:NavCtrl
 * @description
 * # NavCtrl
 * Controller of the uiApp
 */
angular.module('uiApp')
  .controller('NavCtrl', function ($scope, $rootScope, SiteFactory, QuestionFactory) {
    $scope.sites = [];
    SiteFactory.getSites().then(
      function() {
        $scope.sites = SiteFactory.sites.features;
      }
    );
  
    $scope.questions = [];
    QuestionFactory
      .getQuestions()
      .then( function() {
        $scope.questions = QuestionFactory.questions;
      });
    // $scope.categoryQuestions = QuestionFactory.getCategoryQuestions();
  });
