'use strict';

/**
 * @ngdoc overview
 * @name uiApp
 * @description
 * # uiApp
 *
 * Main module of the application.
 */
angular
  .module('uiApp', [
    'ngAnimate',
    'ngCookies',
    'ngResource',
    'ngRoute',
    'ngSanitize',
    'ngTouch'
  ])
  .config(function ($routeProvider) {
    $routeProvider
      .when('/', {
        templateUrl: 'views/main.html',
        controller: 'MainCtrl'
      })
      .when('/about', {
        templateUrl: 'views/about.html',
        controller: 'AboutCtrl'
      })
      .when('/sites', {
        templateUrl: 'views/sitelist.html',
        controller: 'SitelistCtrl'
      })
      .when('/sites/:siteId', {
        templateUrl: 'views/sitedetail.html',
        controller: 'SitedetailCtrl'
      })
      .otherwise({
        templateUrl: '404.html'
      });
  });
