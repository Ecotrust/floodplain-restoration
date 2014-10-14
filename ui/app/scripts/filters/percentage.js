'use strict';

/**
 * @ngdoc filter
 * @name uiApp.filter:percentage
 * @function
 * @description
 * # percentage
 * Filter in the uiApp.
 */
angular.module('uiApp')
  .filter('percentage', function($filter) {
	  return function (input, decimals) {
	    return $filter('number')(input * 100, decimals) + '%';
	  };
  });