'use strict';

describe('Controller: SitedetailCtrl', function () {

  // load the controller's module
  beforeEach(module('uiApp'));

  var SitedetailCtrl,
    scope;

  // Initialize the controller and a mock scope
  beforeEach(inject(function ($controller, $rootScope) {
    scope = $rootScope.$new();
    SitedetailCtrl = $controller('SitedetailCtrl', {
      $scope: scope
    });
  }));

  it('should attach a list of awesomeThings to the scope', function () {
    expect(scope.awesomeThings.length).toBe(3);
  });
});
