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
    

    service.getNodes = function (siteId) {
      var promise = $http.get('/api/node?format=json&site=' + siteId);

      promise.success(function(data) {
        service.nodes = data;
      });
      
      promise.error(function() {
        console.log('Could not fetch questions.json');
      });

      return promise;
    };

    service.postNode = function(node) {
      var postPromise = $http.post('/api/node', node);

      postPromise.success(function(status){
        service.status = status;
      });

      postPromise.error(function(status){
        service.status = status;
        console.log('Could not create new node -- Error: ' + status);
      });

      return postPromise;
    };

    service.putNode = function(node) {
      var putPromise = $http.put('/api/node/' + node.id, node);

      putPromise.success(function(status){
        service.status = status;
      });

      putPromise.error(function(status) {
        service.status = status;
        console.log('Could not update node id: ' + node.id + ' -- Error: ' + status);
      });

      return putPromise;
    };

    return service;
  });
