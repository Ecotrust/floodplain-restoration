'use strict';

describe('Controller: PiteditCtrl', function () {

  // load the controller's module
  beforeEach(module('uiApp'));

  var PiteditCtrl,
    scope;

  // Initialize the controller and a mock scope
  beforeEach(inject(function ($controller, $rootScope) {
    scope = $rootScope.$new();
    PiteditCtrl = $controller('PiteditCtrl', {
      $scope: scope
    });
  }));

  it('should attach a list of awesomeThings to the scope', function () {
    expect(scope.awesomeThings.length).toBe(3);
  });
});
