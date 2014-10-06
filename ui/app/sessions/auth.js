'use strict';

// When running behind grunt:
//   this file is static for testing purposes only

// When running in production:
//   This file is served up dynamically by the django app
//   see the django template by the same name for the dynamic version
//   which is served behind nginx based on django auth sessions
angular
  .module('uiApp').run(function($rootScope){
    $rootScope.userId = 'dummyuser';
   // $rootScope.userId = '';
    $rootScope.baseUrl = 'http://localhost:8000'; // no trailing slash
    console.log($rootScope);
  });
