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

      /*
       * Sites
       */
      .when('/sites', {
        templateUrl: 'views/sitelist.html',
        controller: 'SitelistCtrl'
      })

      .when('/site/new', {
        templateUrl: 'views/siteedit.html',
        controller: 'SiteeditCtrl'
      })

      .when('/site/:siteId', {
        templateUrl: 'views/sitedetail.html',
        controller: 'SitedetailCtrl'
      })

      .when('/site/:siteId/edit', {
        templateUrl: 'views/siteedit.html',
        controller: 'SiteeditCtrl'
      })

      /*
       * Pits
       */
      .when('/site/:siteId/pit/new', {
        templateUrl: 'views/pitedit.html',
        controller: 'PiteditCtrl'
      })

      .when('/site/:siteId/pit/:pitId/edit', {
        templateUrl: 'views/pitedit.html',
        controller: 'PiteditCtrl'
      })
      
      /*
       * Survey
       */
      .when('/site/:siteId/survey/done', {
        templateUrl: 'views/surveydone.html',
        controller: 'SurveydoneCtrl'
      })

      .when('/site/:siteId/survey/:questionId', {
        templateUrl: 'views/survey.html',
        controller: 'SurveyCtrl'
      })

      /*
       * Report
       */
      .when('/site/:siteId/report', {
        templateUrl: 'views/report.html',
        controller: 'ReportCtrl'
      })

      /*
       * Help
       */
      .when('/help/:topic', {
        templateUrl: 'views/help.html',
        controller: 'HelpCtrl'
      })

      /*
      pitService?
      authenticationService?
      contentService?
      mapConfigService?
      */

      .otherwise({
        templateUrl: '404.html'
      });
  });
