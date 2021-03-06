'use strict';

/**
 * @ngdoc function
 * @name uiApp.controller:SurveydoneCtrl
 * @description
 * # SurveydoneCtrl
 * Controller of the uiApp
 */
if(false) {
  var map=null;
  var d3 = null;
}

angular.module('uiApp')
  .controller('SurveydoneCtrl', function ($scope, $routeParams, $rootScope, $window, SiteFactory, QuestionFactory) {

    if (!$rootScope.userName) {
      $window.alert('You are not logged in. You will now be redirected to the login page.');
      $window.location = '/accounts/login/';
    }

    map.showMap(true);
    var questions = [];
    $rootScope.activeSiteId = $routeParams.siteId;

    SiteFactory
      .getSuitabilityScores($routeParams.siteId)
      .then( function() {
        $rootScope.suitability = SiteFactory.suitability;
        var suitabilityList= [];
        var suitabilityCategories = {
          'low': {
            'minScore' : 0,
            'maxScore' : 33,
            'label' : 'Unsuitable',
            'class': 'unsuitable'
          },
          'med' : {
            'minScore': 33,
            'maxScore': 66,
            'label': 'Moderately Suitable',
            'class': 'moderately-suitable'
          },
          'high' : {
            'minScore': 66,
            'maxScore': 100,
            'label': 'Highly Suitable',
            'class': 'highly-suitable'
          }
        };

        var suitabilityScoreTypes = {
          'site': 'Site',
          'socio_economic': 'Socio-Economic',
          'landscape': 'Landscape',
          'suitability': 'Overall'
        };

        for (var key in suitabilityScoreTypes) {  //TODO: what if keys do not match?
          suitabilityList.push({
            'key': key,
            'value': Math.floor(SiteFactory.suitability[key] * 100)
          });
        }

        var scoreDivs = d3.select('.suitability-scores')
          .selectAll('div')
            .data(suitabilityList)
            .enter().append('div')
              .attr('class', 'suitability-score');

        var scoreDivPs = scoreDivs.append('p');

        scoreDivPs.append('span')
          .attr('class', 'suitability-label')
          .text(function(d) {return suitabilityScoreTypes[d.key] + ': ';});
            
        scoreDivPs.append('span')
          .attr('class', 'suitability-rank')
          .text(function(d) {
            for (var catKey in suitabilityCategories) {
              var cat = suitabilityCategories[catKey];
              if (d.value <= cat.maxScore && d.value >= cat.minScore) {
                return cat.label;
              }
            }
            console.log('no label for ' + d.key);
            return null;
          });

        scoreDivs.append('div')
          .attr('class', function(d) {
            for (var catKey in suitabilityCategories) {
              var cat = suitabilityCategories[catKey];
              if (d.value <= cat.maxScore && d.value >= cat.minScore) {
                return 'suitability-bar ' + cat.class;
              }
            }
            return 'suitability-bar';
          })
          .style('width', function(d) { return d.value + '%';})
          .text(function(d) {return d.value;});

      });
    // $scope.questions = QuestionFactory.getQuestions();
    $scope.maxQuestionId = 2;  //QuestionFactory will likely change substantially
                                  //We'll hardcode this for now.

    QuestionFactory
      .getQuestions()
      .then( function() {
        questions = QuestionFactory.questions;
        $scope.numQuestions = questions.length;  //QuestionFactory will likely change substantially
        $scope.maxQuestionId = questions.length;
        
        map.showMap(true);
      });

    $scope.alert = function (msg) {
      $window.alert(msg);
    };

  });
