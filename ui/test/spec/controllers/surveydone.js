'use strict';

describe('Controller: SurveydoneCtrl', function () {

  // load the controller's module
  beforeEach(module('uiApp'));

  var SurveydoneCtrl,
    scope;

  // Initialize the controller and a mock scope
  beforeEach(inject(function ($controller, $rootScope) {
    scope = $rootScope.$new();
    SurveydoneCtrl = $controller('SurveydoneCtrl', {
      $scope: scope
    });
  }));

  it('should attach a list of awesomeThings to the scope', function () {
    expect(scope.awesomeThings.length).toBe(3);
  });
});
