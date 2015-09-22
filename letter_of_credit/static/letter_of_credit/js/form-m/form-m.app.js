"use strict";

require('./form-m')
require('./bid-request')

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
