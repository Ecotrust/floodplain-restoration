'use strict';

/**
 * @ngdoc function
 * @name uiApp.controller:MainCtrl
 * @description
 * # MainCtrl
 * Controller of the uiApp
 */

if (false) {
  var map = null;
}

angular.module('uiApp')
  .controller('MainCtrl', function ($scope, $rootScope, $sce, ContentFactory) {
    $rootScope.activeSiteId = null;
    map.showMap(false);
    $scope.attribution = $sce.trustAsHtml(ContentFactory.get('attribution'));
  });
