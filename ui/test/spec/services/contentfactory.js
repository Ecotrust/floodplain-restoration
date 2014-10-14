'use strict';

describe('Service: contentfactory', function () {

  // load the service's module
  beforeEach(module('uiApp'));

  // instantiate service
  var contentfactory;
  beforeEach(inject(function (_contentfactory_) {
    contentfactory = _contentfactory_;
  }));

  it('should do something', function () {
    expect(!!contentfactory).toBe(true);
  });

});
