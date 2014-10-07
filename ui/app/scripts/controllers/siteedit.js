'use strict';

/**
 * @ngdoc function
 * @name uiApp.controller:SiteeditCtrl
 * @description
 * # SiteeditCtrl
 * Controller of the uiApp
 */
angular.module('uiApp')
  .controller('SiteeditCtrl', function ($scope, $routeParams, $rootScope, SiteFactory) {
    $rootScope.showMap = true;
    var site = SiteFactory.getSite($routeParams.siteId);
    var newSite = false;
    if ($routeParams.siteId === 'new' || site === null) {
      newSite = true;
    }

    $scope.site = site;
    $scope.save = function () {
      if (newSite) {
        console.log('New Site saved');
      } else {
        console.log('Save site ' + $scope.site.id);
      }
    };
  });
