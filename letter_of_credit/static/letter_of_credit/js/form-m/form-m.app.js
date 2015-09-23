"use strict";

require('./bid-request/add-bid')
require('./bid-request/table')
require('./bid-request')
require('./form-m/search-form-m-service')
require('./form-m/table')
require('./form-m/search-form-m')
require('./form-m/lc-issue')
require('./form-m')

var rootCommons = require('commons')

var app = angular.module('form-m-root-app',
  ['rootApp',
   'ui.router',
   'form-m',
   'form-m-bid'
  ])

app.config(rootCommons.interpolateProviderConfig)

app.run(['$rootScope', '$state', '$stateParams', function($rootScope, $state, $stateParams) {
  $rootScope.$state = $state
  $rootScope.$stateParams = $stateParams
}])

app.config(formMRootAppURLConfig)
formMRootAppURLConfig.$inject = ['$stateProvider', '$urlRouterProvider']
function formMRootAppURLConfig($stateProvider, $urlRouterProvider) {
  $urlRouterProvider
    .otherwise('/')

  $stateProvider
    .state('home', {
      url: '/',

      template: require('./home.html')
    })
}
