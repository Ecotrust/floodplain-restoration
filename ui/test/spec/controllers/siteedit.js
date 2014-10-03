'use strict';

describe('Controller: SiteeditCtrl', function () {

  // load the controller's module
  beforeEach(module('uiApp'));

  var SiteeditCtrl,
    scope;

  // Initialize the controller and a mock scope
  beforeEach(inject(function ($controller, $rootScope) {
    scope = $rootScope.$new();
    SiteeditCtrl = $controller('SiteeditCtrl', {
      $scope: scope
    });
  }));

  it('should attach a list of awesomeThings to the scope', function () {
    expect(scope.awesomeThings.length).toBe(3);
  });
});
