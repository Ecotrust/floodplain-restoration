'use strict';

/**
 * @ngdoc function
 * @name uiApp.controller:ReportCtrl
 * @description
 * # ReportCtrl
 * Controller of the uiApp
 */
angular.module('uiApp')
  .controller('ReportCtrl', function ($scope, $rootScope) {
    map.showMap(true);

    $scope.awesomeThings = [
      'HTML5 Boilerplate',
      'AngularJS',
      'Karma'
    ];
  });
