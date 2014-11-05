'use strict';

/**
 * @ngdoc function
 * @name uiApp.directive:SurveyDir
 * @description
 * # SurveyDir
 * Survey Directive of the uiApp
 */
angular.module('uiApp')
  .directive('SurveyDir', function ($window, $timeout) {
    // $window.alert('stuff!1');
    return function(scope, element) {
      // $window.alert('stuff!');
      $window.resize();
      $timeout(function(){ 
        $window.triggerHandler('resize'); 
        $window.triggerHandler('SurveyDir');
      });
    }

  });
