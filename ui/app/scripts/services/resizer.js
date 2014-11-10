'use strict';

/**
 * @ngdoc function
 * @name uiApp.directive:SurveyDir
 * @description
 * # SurveyDir
 * Survey Directive of the uiApp
 */
angular.module('uiApp')
  .config(function ($httpProvider) {
        $httpProvider.responseInterceptors.push('myHttpInterceptor');
        var resizePageFunction = function (data, headersGetter) {
            return data;
        };
        $httpProvider.defaults.transformRequest.push(resizePageFunction);
    })
// register the interceptor as a service, intercepts ALL angular ajax http calls
    .factory('myHttpInterceptor', function ($q, $window) {
        return function (promise) {
            return promise.then(function (response) {
            	window.setTimeout(resize, 1);
                return response;

            }, function (response) {
                window.setTimeout(resize, 1);
                return $q.reject(response);
            });
        };
    })