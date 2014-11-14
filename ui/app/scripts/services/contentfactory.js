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
    /*jshint multistr:true */
    var allContent = {
      'about': 'We are building an online tool that provides an efficient and sound approach to quickly identify whether restoring a former gravel pit mine property is worth the investment of time and money.',
      'title': 'Floodplain Gravel Mine Restoration',
      'welcome': 'The Floodplain Gravel Mine Restoration Tool',
      'hook': 'Informed decision making and resource investment <br> for the restoration of floodplain mining sites.',
      'requirements': '<a class="documents-link" href="#/help/documents">What will I need?</a>',
      'getStarted': 'Get Started',
      'siteListHeader': 'All properties',
      'previousQuestion': '<< Previous Question',
      'nextQuestion': 'Next Question >>',
      'attribution': 'This tool is a product of The Nature Conservancy and Ecotrust',
      'documents': '\
        <h3>Before you get started...</h3>\
        <h4>Please assemble as many of the following resources as possible:</h4>\
        <div class="table-container">\
          <div class="table-row">\
            <div class="table-cell col-md-12">\
              <div class="property-box padded-box">\
                <p class="blue-text document-list-item">Taxlot, land user, easement, access, infrastructure, and other relevant property information.</p>\
                <hr class="document-list-hr">\
                <p class="blue-text document-list-item">Any information on existing permits or pit reclaimation requirements</p>\
                <hr class="document-list-hr">\
                <p class="blue-text document-list-item">Existing conservation plans, recovery plans, prioritizations, regional priorities</p>\
                <hr class="document-list-hr">\
                <p class="blue-text document-list-item">Water rights information</p>\
                <hr class="document-list-hr">\
                <p class="blue-text document-list-item">State environment or water quality information</p>\
                <hr class="document-list-hr">\
                <p class="blue-text document-list-item">Watershed assessments, sediment budgets, and other available watershed or river research, reports, or data</p>\
                <hr class="document-list-hr">\
                <p class="blue-text document-list-item">Ecological assessments, research, reports, or data on species and habitat in the watershed, the reach, or on the property</p>\
              </div>\
            </div>\
            <div class="col-md-1 table-cell survey-nav-col">\
              <a href="#/">\
                <p class="survey-nav survey-nav-forward">\
                  <span class="glyphicon glyphicon-play survey-nav-icon"></span>\
                </p>\
              </a>\
            </div>'
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
