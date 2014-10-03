'use strict';

describe('Controller: SitenewCtrl', function () {

  // load the controller's module
  beforeEach(module('uiApp'));

  var SitenewCtrl,
    scope;

  // Initialize the controller and a mock scope
  beforeEach(inject(function ($controller, $rootScope) {
    scope = $rootScope.$new();
    SitenewCtrl = $controller('SitenewCtrl', {
      $scope: scope
    });
  }));

  it('should attach a list of awesomeThings to the scope', function () {
    expect(scope.awesomeThings.length).toBe(3);
  });
});
