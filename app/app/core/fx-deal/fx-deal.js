"use strict";

/*jshint camelcase:false*/

var app = angular.module('fx-deal-service', ['rootApp'])

app.factory('FxDeal', FxDeal)
FxDeal.$inject = ['$resource', 'urls']
function FxDeal($resource, urls) {
  var url = appendToUrl(urls.fxDealAPIUrl, ':id');
  return $resource(url, {id: '@id'}, {
      'put': {
        method: 'PUT'
      }
    }
  )
}

require('./add-deal/add-deal.js')
