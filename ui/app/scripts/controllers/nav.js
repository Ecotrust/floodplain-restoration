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
    $scope.site = {
      'properties': {
        'name': null
      }
    };
    
    $rootScope.$watch('activeSiteId', function() {

      $scope.site = {
        'properties': {
          'name': null
        }
      };

      SiteFactory
        .getSites()
        .then( function() {
          $scope.sites = SiteFactory.sites.features;

          // set active site
          for (var i = SiteFactory.sites.features.length - 1; i >= 0; i--) {
            var site = SiteFactory.sites.features[i];
            if (site.id === parseInt($rootScope.activeSiteId, 10)) {
              $scope.site = site;
            }
          }
        });
    });
  
    $scope.questions = [];
    QuestionFactory
      .getQuestions()
      .then( function() {
        $scope.questions = QuestionFactory.questions;
      });
    // $scope.categoryQuestions = QuestionFactory.getCategoryQuestions();
  });
