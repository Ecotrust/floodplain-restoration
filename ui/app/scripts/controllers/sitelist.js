'use strict';

if (false) { var map; }

/**
 * @ngdoc function
 * @name uiApp.controller:SitelistCtrl
 * @description
 * # SitelistCtrl
 * Controller of the uiApp
 */
angular.module('uiApp')
  .controller('SitelistCtrl', function ($scope, $rootScope, $window, SiteFactory, QuestionFactory, NodeFactory) {

    if (!$rootScope.userName) {
      $window.alert('You are not logged in. You will now be redirected to the login page.');
      $window.location = '/accounts/login/';
    }

    map.showMap(true);
    
    $scope.sites = [];
    $rootScope.activeSiteId = null;
    $scope.numQuestions = 0;

    function getNodes(site) {
      NodeFactory
        .getNodes($scope.sites[site].id)
        .then( function() {
          $scope.sites[site].nodeCount = NodeFactory.nodes.length;
        });
    }

    SiteFactory
      .getSites()
      .then( function() {
        $scope.sites = SiteFactory.sites.features;
        map.clear();
        map.loadSites(SiteFactory.sites);
        map.showMap(true);
        for (var site in $scope.sites) {
          getNodes(site);
        }
      });

    QuestionFactory
      .getQuestions()
      .then( function() {
        $scope.numQuestions = QuestionFactory.questions.length;
      });

    $scope.deleteSite = function(siteId) {
      if ($window.confirm('Delete this property? Are you sure?') === true) {
        SiteFactory.deleteSite(siteId).then(function() {

          // Update new sites
          $scope.sites = SiteFactory.sites.features;

          // Map active sites
          map.clear();
          map.loadSites(SiteFactory.sites);
        });
      }
    };

    $scope.toggleCircleIconClass = function(iconId) {
      var icon = document.getElementById(iconId);
      if (icon.classList.contains('glyphicon-plus-sign')) {
        icon.className = icon.className.replace(/\bglyphicon-plus-sign\b/,'glyphicon-minus-sign');
      } else {
        icon.className = icon.className.replace(/\bglyphicon-minus-sign\b/,'glyphicon-plus-sign');
      }
    };

  });
