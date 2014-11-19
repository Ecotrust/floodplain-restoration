'use strict';

if (false) {var map =  null;}

/**
 * @ngdoc function
 * @name uiApp.controller:ReportCtrl
 * @description
 * # ReportCtrl
 * Controller of the uiApp
 */
angular.module('uiApp')
  .controller('ReportCtrl', function ($scope, $rootScope, $window) {

    if (!$rootScope.userName) {
      $window.alert('You are not logged in. You will now be redirected to the login page.');
      $window.location = '/accounts/login/';
    }

    map.showMap(false);

    $scope.awesomeThings = [
      'HTML5 Boilerplate',
      'AngularJS',
      'Karma'
    ];
  });
