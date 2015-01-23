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
    service.contexts = {
      'site': {
        'id': 1,
        'label': 'Site',
        'components': [
          {
            'id': 10,
            'name': 'Pit restorability',
            'question_ids': []
          },
          {
            'id': 11,
            'name': 'Practical, site-level restorability',
            'question_ids': [1,2,3]
          }
        ]
      },
      'socio_economic': {
        'id': 2,
        'label': 'Socio-Economic',
        'components': [
          {
            'id': 12,
            'name': 'Cost benefit',
            'question_ids': [8,9,10]
          },
          {
            'id': 13,
            'name': 'Threat to other areas / permitability',
            'question_ids': [4,5,6,7]
          }
        ]
      },
      'landscape': {
        'id': 3,
        'label': 'Landscape',
        'components': [
          {
            'id': 14,
            'name': 'Conservation value',
            'question_ids': [26,27]
          },
          {
            'id': 15,
            'name': 'Biotic conditions',
            'question_ids': [23,24,25]
          },
          {
            'id': 16,
            'name': 'Abiotic conditions',
            'question_ids': [19,20,21,22]
          },
          {
            'id': 17,
            'name': 'Geomorphic controls',
            'question_ids': [11,12,13,14]
          },
          {
            'id': 18,
            'name': 'Floodplain characteristics',
            'question_ids': [15,16,17,18]
          }
        ]
      },
      'suitability': {
        'id': 4,
        'label': 'Overall',
        'components': []
      },
    };
    
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

    service.getContexts = function() {
      var promise = $http.get('/api/questions.json');

      promise.success(function(data) {
        service.questions = data;
        service.contexts = service.contexts;
      });

      promise.error(function() {
        console.log('Could not fetch contexts.');
      });

      return promise;
    };

    return service;
  });
