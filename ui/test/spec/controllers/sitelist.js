'use strict';

describe('Controller: SitelistCtrl', function () {

  // load the controller's module
  beforeEach(module('uiApp'));

  var SitelistCtrl,
    scope;

  // Initialize the controller and a mock scope
  beforeEach(inject(function ($controller, $rootScope) {
    scope = $rootScope.$new();
    SitelistCtrl = $controller('SitelistCtrl', {
      $scope: scope
    });
  }));

  it('should attach a list of awesomeThings to the scope', function () {
    expect(scope.awesomeThings.length).toBe(3);
  });
});
