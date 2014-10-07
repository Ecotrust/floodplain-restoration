'use strict';

/**
 * @ngdoc function
 * @name uiApp.controller:MainCtrl
 * @description
 * # MainCtrl
 * Controller of the uiApp
 */
angular.module('uiApp')
  .controller('MainCtrl', function ($scope, $rootScope) {
  	$rootScope.showMap = false;
    $rootScope.siteId = null;
    $rootScope.siteName = null;
  });
