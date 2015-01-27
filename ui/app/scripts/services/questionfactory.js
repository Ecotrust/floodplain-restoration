'use strict';

/**
 * @ngdoc service
 * @name uiApp.questions
 * @description
 * # questions
 * Factory in the uiApp.
 */
angular.module('uiApp')
  .factory('QuestionFactory', function ($http) {

    var service = {};

    service.questions = [];
    service.categories = [];
    service.contexts = [];
    
    service.getQuestions = function () {
        var promise = $http.get('/api/questions.json');

        promise.success(function(data) {
          // full args
          // data, status, headers, config
          data.sort(function(a,b) {
            return a.order - b.order;
          });
          service.questions = data;
        });
        
        promise.error(function() {
          console.log('Could not fetch questions.json');
        });

        return promise;
      };

    service.getCategories = function() {
      var promise = $http.get('/api/categories.json');

      promise.success(function(data) {
        service.categories = data;
      });

      promise.error(function() {
        console.log('Could not fetch categories.');
      });

      return promise;
    };

    service.getContexts = function() {
      var promise = $http.get('/api/contexts.json');

      promise.success(function(data) {
        service.contexts = data;
      });

      promise.error(function() {
        console.log('Could not fetch contexts.');
      });

      return promise;
    };

    return service;
  });
