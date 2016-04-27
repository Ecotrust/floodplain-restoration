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

    service.initialPitQuestions = function() {

      var questionDefaults = {
        'contamination': 0.75,
        'adjacent_river_depth': 0.75,
        'slope_dist': 0.9,
        'pit_levies': 0.85,
        'bank_slope': 0.75,
        'surface_area': 0.5
      };

      return {
        'name': {
          'question': 'Name',
          'visible': true,
          'id': 'name',
          'order': 0,
          'type': 'text',
          'disabled': false,
          'answers': []
        },
        'contamination':{
          'question': 'Is hazardous waste present?',
          'visible': true,
          'id': 'contamination',
          'order': 10,
          'type': 'select',
          'disabled': false,
          'answers': [
            {
              'label': 'I don\'t know',
              'value': questionDefaults.contamination
            },
            {
              'label': 'No, definitely not.',
              'value': 1
            },
            {
              'label': 'No, I don’t think so',
              'value': 0.8
            },
            {
              'label': 'Yes, and the cost and effort to remediate it is acceptable.',
              'value': 0.7
            },
            {
              'label': 'Yes, but I do not know if it can be remediated.',
              'value': 0.5
            },
            {
              'label': 'Yes, and it will be expensive and/or very difficult to remediate.',
              'value': 0.0
            }
          ]
        },
        'adjacent_river_depth': {
          'question': 'Is the pit more than twice as deep as the adjacent river <u><i>thalweg</i></u>?',
          'visible': true,
          'id': 'adjacent_river_depth',
          'order': 30,
          'type': 'select',
          'disabled': false,
          'answers': [
            {
              'label': 'I don\'t know',
              'value': questionDefaults.adjacent_river_depth
            },
            {
              'label': 'No',
              'value': 1
            },
            {
              'label': 'They are the same depth',
              'value': 0.7
            },
            {
              'label': 'Yes',
              'value': 0.0
            }
          ],
          'info': 'The thalweg of the river is the line of the lowest points within the channel, spanning the length of the river.'
        },
        'slope_dist':{
          'question': 'What is the distance from the river to the pit edge?',
          'visible': true,
          'id': 'slope_dist',
          'order': 40,
          'type': 'select',
          'disabled': false,
          'answers': [
            {
              'label': 'I don\'t know',
              'value': questionDefaults.slope_dist
            },
            {
              'label': 'Short (< 250 ft.)',
              'value': 1
            },
            {
              'label': 'Medium (250-1000 ft.)',
              'value': 0.6
            },
            {
              'label': 'Long (> 1000 ft.)',
              'value': 0
            }
          ]
        },
        'pit_levies': {
          'question': 'Are there any pit-adjacent levees?',
          'visible': true,
          'id': 'pit_levies',
          'order': 50,
          'type': 'select',
          'disabled': false,
          'answers': [
            {
              'label': 'I don\'t know',
              'value': questionDefaults.pit_levies
            },
            {
              'label': 'No',
              'value': 1
            },
            {
              'label': 'Yes',
              'value': 0.0
            }
          ]
        },
        'bank_slope':{
          'question': 'Select the answer that best describes the slope of the pit bank:',
          'visible': true,
          'id': 'bank_slope',
          'order': 70,
          'type': 'select',
          'disabled': false,
          'answers': [
            {
              'label': 'I don\'t know',
              'value': questionDefaults.bank_slope
            },
            {
              'label': 'The bank slope is very shallow around most of the pit.',
              'value': 1
            },
            {
              'label': 'The bank slope is a mix of steep and shallow.',
              'value': 0.7
            },
            {
              'label': 'The bank slope is steep around most of the pit.',
              'value': 0.0
            }
          ]
        },
        'surface_area':{
          'question': 'What is the surface area of the pit?',
          'visible': false,
          'id': 'surface_area',
          'order': 90,
          'type': 'select',
          'disabled': true,
          'answers': [
            {
              'label': '< 5 acres',
              'value': 1
            },
            {
              'label': '5-20 acres',
              'value': 0.6
            },
            {
              'label': '20-30 acres',
              'value': 0.3
            },
            {
              'label': '> 30 acres',
              'value': 0
            }
          ]
        },
        'notes':{
          'question': 'Notes',
          'visible': true,
          'id': 'notes',
          'order': 110,
          'type': 'textarea',
          'disabled': false,
          'answers': []
        }
      }
    };

    service.getPitQuestions = function () {
        var promise = $http.get('/api/pitscores.json');

        promise.success(function(data) {
          var ret_val = {};
          for (var i=0; i<data.length; i++){
            ret_val[data[i].score] = data[i]
          }
          service.pitQuestions = ret_val;
        });

        promise.error(function() {
          console.log('Could not fetch pit questions json');
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
