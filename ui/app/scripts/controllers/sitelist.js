'use strict';

/**
 * @ngdoc function
 * @name uiApp.controller:SitelistCtrl
 * @description
 * # SitelistCtrl
 * Controller of the uiApp
 */
angular.module('uiApp')
  .controller('SitelistCtrl', function ($scope, $rootScope, SiteFactory) {
    $scope.sites = SiteFactory.getSites();
    $rootScope.siteId = null;
    $rootScope.siteName = null;
  });
