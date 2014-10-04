'use strict';

/**
 * @ngdoc service
 * @name uiApp.questions
 * @description
 * # questions
 * Factory in the uiApp.
 */
angular.module('uiApp')
  .factory('QuestionFactory', function () {

    var questions = [
      {
        'layers': [],
        'id': 1,
        'name': 'fill_material_availability',
        'title': 'Fill material availability',
        'question': 'Fill material availability?',
        'detail': 'Detail about Fill material availability',
        'order': 100.0,
        'category': '',
        'image': '',
        'supplement': '',
        'choices': [
          {
            'choice': 'available',
            'value': 1.0
          },
          {
            'choice': 'Not Sure',
            'value': 0.5
          },
          {
            'choice': 'unavailable',
            'value': 0.0
          }
        ]
      },
      {
        'layers': [],
        'id': 2,
        'name': 'q2',
        'title': 'Question2',
        'question': 'Question 2 is not about Fill material availability?',
        'detail': 'Definitely no thing to do with  bout Fill material availability',
        'order': 100.0,
        'category': '',
        'image': '',
        'supplement': '',
        'choices': [
          {
            'choice': 'suitable',
            'value': 1.0
          },
          {
            'choice': 'Not Sure',
            'value': 0.5
          },
          {
            'choice': 'unsuitable',
            'value': 0.0
          }
        ]
      }
    ];

    // TODO put question list in rootScope for navbar dropdown
    return {
      getQuestion: function (questionId) {
        // questionId = parseInt(questionId, 10);
        for (var i = questions.length - 1; i >= 0; i--) {
          if (questions[i].id === questionId) {
            return questions[i];
            // TODO determine choice based on inputnodes of selected site
          }
        }
      },

      minId: function() {
        return 1; //TODO
      },

      maxId: function() {
        return 2;  // TODO 
      }
    };
  });
