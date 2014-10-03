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

      .when('/sites', {
        templateUrl: 'views/sitelist.html',
        controller: 'SitelistCtrl'
      })

      .when('/site/:siteId', {
        templateUrl: 'views/sitedetail.html',
        controller: 'SitedetailCtrl'
      })

      .when('/site/new', {
        templateUrl: 'views/sitenew.html',
        controller: 'SitenewCtrl'
      })

      .when('/site/:siteId/edit', {
        templateUrl: 'views/siteedit.html',
        controller: 'SiteeditCtrl'
      })

      .when('/site/:siteId/pit/new', {
        templateUrl: 'views/pitnew.html',
        controller: 'PitnewCtrl'
      })

      .when('/site/:siteId/pit/:pitId/edit', {
        templateUrl: 'views/pitedit.html',
        controller: 'PiteditCtrl'
      })

      .when('/site/:siteId/survey/:questionId', {
        templateUrl: 'views/survey.html',
        controller: 'SurveyCtrl'
      })

      .when('/site/:siteId/survey/done', {
        templateUrl: 'views/surveydone.html',
        controller: 'SurveydoneCtrl'
      })

      .when('/site/:siteId/report', {
        templateUrl: 'views/report.html',
        controller: 'ReportCtrl'
      })

      .when('/help/:topic', {
        templateUrl: 'views/help.html',
        controller: 'HelpCtrl'
      })

      /*
      ... all of these can drive from a contentService which has all the CMSy text in one json

      How about delete actions?

      pitService?
      authenticationService?
      contentService?
      mapConfigService?

      */
      .otherwise({
        templateUrl: '404.html'
      });
  });
