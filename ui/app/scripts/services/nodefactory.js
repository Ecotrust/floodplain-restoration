'use strict';

/**
 * @ngdoc service
 * @name uiApp.nodeFactory
 * @description
 * # nodeFactory
 * Factory in the uiApp.
 */
angular.module('uiApp')
  .factory('NodeFactory', function ($http) {
    var service = {};

    service.nodes = [];
    

    service.getNodes = function () {
      var promise = $http.get('/api/node.json');

      promise.success(function(data) {
        // full args
        // data, status, headers, config
        service.nodes = data;
      });
      
      promise.error(function() {
        console.log('Could not fetch questions.json');
      });

      return promise;
    };

    service.postNode = function(node, wkt) {
      console.log('POST', node, wkt);
      // TODO return a promise
    };

    service.putNode = function(node, wkt) {
      console.log('PUT', node, wkt);
      // TODO return a promise
    };

    return service;
  });
