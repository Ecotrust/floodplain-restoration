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
        'title': 'Property Information',
        'question': 'Is the property for sale at or below fair market value?',
        'detail': 'Detail about Fill material availability',
        'order': 100.0,
        'category': 'Property Information',
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
        'title': '',
        'question': 'Are there recent or continuing impacts from contaminated sites upstream or adjacent to your property, within the river reach?',
        'detail': 'Additional info and resources',
        'order': 100.0,
        'category': 'Water Quality',
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
