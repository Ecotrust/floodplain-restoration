'use strict';

describe('Service: siteFactory', function () {

  // load the service's module
  beforeEach(module('uiApp'));

  // instantiate service
  var siteFactory;
  beforeEach(inject(function (_siteFactory_) {
    siteFactory = _siteFactory_;
  }));

  it('should do something', function () {
    expect(!!siteFactory).toBe(true);
  });

});
