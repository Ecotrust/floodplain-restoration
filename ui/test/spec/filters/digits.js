'use strict';

describe('Filter: digits', function () {

  // load the filter's module
  beforeEach(module('uiApp'));

  // initialize a new instance of the filter before each test
  var digits;
  beforeEach(inject(function ($filter) {
    digits = $filter('digits');
  }));

  it('should return the input prefixed with "digits filter:"', function () {
    var text = 'angularjs';
    expect(digits(text)).toBe('digits filter: ' + text);
  });

});
