'use strict';

describe('Service: nodeFactory', function () {

  // load the service's module
  beforeEach(module('uiApp'));

  // instantiate service
  var nodeFactory;
  beforeEach(inject(function (_nodeFactory_) {
    nodeFactory = _nodeFactory_;
  }));

  it('should do something', function () {
    expect(!!nodeFactory).toBe(true);
  });

});
