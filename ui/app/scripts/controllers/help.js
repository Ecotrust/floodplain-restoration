'use strict';

/**
 * @ngdoc function
 * @name uiApp.controller:HelpCtrl
 * @description
 * # HelpCtrl
 * Controller of the uiApp
 */

if (false) {
  var map = null;
}

angular.module('uiApp')
  .controller('HelpCtrl', function ($scope, $routeParams, $rootScope, $sce) {
    $scope.topic = $routeParams.topic;
    $rootScope.activeSiteId = null;

    map.showMap(false);
  });
