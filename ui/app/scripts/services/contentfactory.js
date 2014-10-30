'use strict';

/**
 * @ngdoc service
 * @name uiApp.contentfactory
 * @description
 * # contentfactory
 * Factory in the uiApp.
 */
angular.module('uiApp')
  .factory('ContentFactory', function () {

    // TODO get from REST API
    // If you need HTML here, the view needs to contain an ng-bind-html directive 
    // e.g. <span ng-bind-html='content.attrWithHtml'></span>
    var allContent = {
      'about': 'We are building an online tool that provides an efficient and sound approach to quickly identify whether restoring a former gravel pit mine property is worth the investment of time and money.',
      'title': 'Floodplain Gravel Mine Restoration',
      'welcome': 'The Floodplain Gravel Mine Restoration Tool',
      'hook': 'Informed decision making and resource investment <br> for the restoration of floodplain mining sites.',
      'getStarted': 'Get Started',
      'siteListHeader': 'Select a property to evaluate',
      'previousQuestion': '<< Previous Question',
      'nextQuestion': 'Next Question >>',
      'attribution': 'This tool is a product of The Nature Conservancy and Ecotrust'
    };

    return {
      allContent: function () {
        return allContent;
      },
      getContent: function (key) {
        return allContent[key];
      },
      //alias
      get: function (key) {
        return this.getContent(key);
      }
    };
  });
