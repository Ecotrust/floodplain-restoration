'use strict';

/**
 * @ngdoc function
 * @name uiApp.controller:HelpCtrl
 * @description
 * # HelpCtrl
 * Controller of the uiApp
 */
angular.module('uiApp')
  .controller('HelpCtrl', function ($scope, $routeParams, $rootScope, $sce, ContentFactory) {
    $rootScope.showMap = false;

    $scope.text = $sce.trustAsHtml(ContentFactory.get($routeParams.topic));
    $scope.topic = $routeParams.topic;

  });
