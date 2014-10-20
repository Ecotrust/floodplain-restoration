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
    $scope.sites = SiteFactory.getSites();
    $scope.questions = QuestionFactory.getQuestions();
    // $scope.categoryQuestions = QuestionFactory.getCategoryQuestions();
  });
