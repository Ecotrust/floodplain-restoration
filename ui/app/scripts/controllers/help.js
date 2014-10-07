'use strict';

/**
 * @ngdoc function
 * @name uiApp.controller:HelpCtrl
 * @description
 * # HelpCtrl
 * Controller of the uiApp
 */
angular.module('uiApp')
  .controller('HelpCtrl', function ($scope, $routeParams, $rootScope) {
    $rootScope.showMap = false;
    
    // TODO implement and use ContentFactory
    var allContent = {
      'about': 'We are building an online tool that provides an efficient and sound approach to quickly identify whether restoring a former gravel pit mine property is worth the investment of time and money.'
    };

    $scope.content = allContent[$routeParams.topic];
    $scope.topic = $routeParams.topic;

  });
