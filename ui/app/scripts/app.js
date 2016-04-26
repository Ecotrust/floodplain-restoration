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
  .config(function ($routeProvider, $httpProvider) {
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';

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
  })
  .run(function ($rootScope, ContentFactory, QuestionFactory) {

    $rootScope.content = ContentFactory.initialContent();
    ContentFactory
      .allContent()
      .then( function() {
        $rootScope.content = ContentFactory.content;
      });

    var setPitQuestionList = function() {
      $rootScope.pitQuestionList = []
      var keys = Object.keys($rootScope.pitQuestions);
      for (var i = 0; i < keys.length; i++) {
        $rootScope.pitQuestionList.push($rootScope.pitQuestions[keys[i]]);
        $rootScope.pitQuestionList.sort(function(a,b) {
          return a.order - b.order;
        });
      }
    };

    $rootScope.pitQuestions = QuestionFactory.initialPitQuestions();
    setPitQuestionList();

    QuestionFactory
      .getPitQuestions()
      .then( function() {
        var keys = Object.keys(QuestionFactory.pitQuestions);
        for (var i = 0; i < keys.length; i++) {
          $rootScope.pitQuestions[keys[i]] = QuestionFactory.pitQuestions[keys[i]];
        }
        setPitQuestionList();
      });
  });
