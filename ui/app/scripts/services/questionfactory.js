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
    service.activeQuestion = {};
    
    service.getQuestions = function () {
        var promise = $http.get('/api/questions.json');

        promise.success(function(data) {
          // full args
          // data, status, headers, config
          service.questions = data;
        });
        
        promise.error(function() {
          console.log('Could not fetch questions.json');
        });

        return promise;
      };

    return service;
  });
