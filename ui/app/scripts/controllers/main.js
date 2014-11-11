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
    $rootScope.siteId = null;
    $rootScope.siteName = null;
    map.showMap(false);
  });
