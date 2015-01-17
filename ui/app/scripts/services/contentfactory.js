'use strict';

/**
 * @ngdoc service
 * @name uiApp.contentfactory
 * @description
 * # contentfactory
 * Factory in the uiApp.
 */
angular.module('uiApp')
  .factory('ContentFactory', function ($http) {

    // TODO get from REST API
    // If you need HTML here, the view needs to contain an ng-bind-html directive 
    // e.g. <span ng-bind-html='content.attrWithHtml'></span>
    /*jshint multistr:true */

    var service = {};

    service.content = {
      'about': 'We are building an online tool that provides an efficient and sound approach to quickly identify whether restoring a former gravel pit mine site is worth the investment of time and money.',
      'title': 'Floodplain Gravel Mine Restoration',
      'welcome': 'The Floodplain Gravel Mine Restoration Tool',
      'hook': 'Informed decision making and resource investment <br> for the restoration of floodplain mining sites.',
      'requirements': '<a class="homepage-link" href="#/help/documents">Before you get started</a>',
      'getStarted': 'Get Started',
      'siteListHeader': 'All Sites',
      'siteCreateDirections': 'Click anywhere on the map to start defining your general site boundary. <br/><br/> Continue clicking to complete the shape of your site. <br/><br/> When you\'re satisfied with your site outline, double-click to end drawing.<br/><br/> Name and save your site when done. You can come back and edit this at any time.',
      'siteEditDirections': 'Click and hold anywhere on the site border to grab it. <br/><br/> Drag the section of border to where it belongs.',
      'siteEditDefinitions': '<div class="definition-block blue-text"><p><span class="definition-term">Site</span>: A contiguous plot of land that encompasses one or more pits.</p><p><span class="definition-term">Pit</span>: A single gravel pit mine.</p></div>',
      'pitCreateDirections': 'Like drawing your site, click once on the map to begin drawing your pit boundaries. Click again to add additional points. Double-click to finish.',
      'pitEditDirections': 'Click and hold anywhere on the pit border to grab it. Drag the section of the border to where it belongs.',
      'previousQuestion': '<< Previous Question',
      'attribution': 'This tool is a product of The Nature Conservancy and Ecotrust',
      'documents': '\
        <h3>Before you get started...</h3>\
        <h4>Please assemble as many of the following resources as possible:</h4>\
        <div class="table-container">\
          <div class="table-row">\
            <div class="table-cell col-md-12">\
              <div class="property-box padded-box">\
                <p class="blue-text document-list-item">Taxlot, land user, easement, access, infrastructure, and other relevant site information.</p>\
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
                <p class="blue-text document-list-item">Ecological assessments, research, reports, or data on species and habitat in the watershed, the reach, or on the site</p>\
                <hr class="document-list-hr">\
                <p class="blue-text document-list-item">Reasonable estimates of both pit depth and river thalweg</p>\
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

    service.initialContent = function () {
      return service.content;
    };

    service.allContent = function () {
        var promise = $http.get('/api/content.json');

        promise.success(function(data) {
          for (var i = 0; i < data.length; i++) {
            service.content[data[i].slug] = data[i].content;
          }
        });
        
        promise.error(function() {
          console.log('Could not fetch content.json');
        });

        return promise;
      };

    service.getContent = function (key) {
        return service.content[key];
      };

    service.get = function (key) {
        return this.getContent(key);
      };

    return service;
  });
