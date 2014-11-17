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
            'bgColor': 'gray'
          },
          'med' : {
            'minScore': 33,
            'maxScore': 66,
            'label': 'Moderately Suitable',
            'bgColor': 'yellow'
          },
          'high' : {
            'minScore': 66,
            'maxScore': 100,
            'label': 'Highly Suitable',
            'bgColor': 'green'
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
          .attr('class', 'suitability-category')
          .text(function(d) {
            for (var catKey in suitabilityCategories) {
              var cat = suitabilityCategories[catKey];
              if (d.value <= cat.maxScore && d.value >= cat.minScore) {
                console.log(cat.label);
                return cat.label;
              }
            }
            console.log('no label for ' + d.key);
            return null;
          });

        scoreDivs.append('div')
          .attr('class', 'suitability-bar')
          .style('width', function(d) { return d.value + '%';})
          .style('background-color', function(d) {
            for (var catKey in suitabilityCategories) {
              var cat = suitabilityCategories[catKey];
              if (d.value <= cat.maxScore && d.value >= cat.minScore) {
                console.log(cat.bgColor);
                return cat.bgColor;
              }
            }
            console.log('no bg color for ' + d.key);
            return 'transparent';
          })
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
        $scope.maxQuestionId = questions[questions.length-1].id;
        
        map.showMap(true);
      });

    $scope.alert = function (msg) {
      $window.alert(msg);
    }

  });
