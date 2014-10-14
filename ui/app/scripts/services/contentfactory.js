'use strict';

/**
 * @ngdoc service
 * @name uiApp.contentfactory
 * @description
 * # contentfactory
 * Factory in the uiApp.
 */
angular.module('uiApp')
  .factory('ContentFactory', function ($rootScope) {

    // TODO get from REST API
    var allContent = {
      'about': 'We are building an online tool that provides an efficient and sound approach to quickly identify whether restoring a former gravel pit mine property is worth the investment of time and money.',
      'title': 'Floodplain Gravel Mine Restoration',
      'welcome': 'Welcome to the Floodplain Gravel Mine Restoration Tool',
      'hook': 'Informed decision making and resource investment for the restoration of floodplain mining sites.',
      'getStarted': 'Get Started',
      'siteListHeader': 'Select a property to evaluate'
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
