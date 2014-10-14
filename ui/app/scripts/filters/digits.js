'use strict';

/**
 * @ngdoc filter
 * @name uiApp.filter:digits
 * @function
 * @description
 * # digits
 * Filter in the uiApp.
 */
angular.module('uiApp')
  .filter('digits', function() {
    return function(input) {
      if (input < 10) {
        input = '0' + input;
      }
      return input;
    };
  });