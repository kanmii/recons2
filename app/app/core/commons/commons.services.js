"use strict";

var rootCommons = require('commons')
var services = angular.module('rootApp')

services.factory('Currency', Currency)
Currency.$inject = ['$resource', 'urls']
function Currency($resource, urls) {
  var url = appendToUrl(urls.currencyAPIUrl, ':id')
  return $resource(url, {id: '@id'}, {
      'put': {
        method: 'PUT'
      }
    }
  )
}

services.factory('getTypeAheadCurrency', getTypeAheadCurrency)
getTypeAheadCurrency.$inject = ['Currency']
function getTypeAheadCurrency(Currency) {

  function getCurrency(currencyCode) {
    return Currency.query({code: currencyCode}).$promise
  }

  return getCurrency
}

services.factory('Branch', Branch)
Branch.$inject = ['$resource', 'urls']
function Branch($resource, urls) {
  var url = appendToUrl(urls.branchAPIUrl, ':id')
  return $resource(url, {id: '@id'}, {
      'put': {
        method: 'PUT'
      }
    }
  )
}

services.factory('parseDate', parseDate);
function parseDate() {
  return function(aDate) {
    //aDate is a date string and not datetime
    if ((typeof aDate === 'string') && /\d{4}-\d{2}-\d{2}/.test(aDate)) {
      return aDate;
    } else if (aDate instanceof Date) {
      return aDate.strftime('%Y-%m-%d');
    }

    return null
  }
}

services.factory('formatDate', formatDate);
function formatDate() {
  return function(aDate) {
    //aDate is a date string and not datetime
    if ((typeof aDate === 'string') && /\d{4}-\d{2}-\d{2}/.test(aDate)) {
      return aDate;
    } else if (aDate instanceof Date) {
      return aDate.strftime('%Y-%m-%d');
    }

    return null
  }
}

services.controller('XhrErrorDisplayCtrl', XhrErrorDisplayCtrl)
XhrErrorDisplayCtrl.$inject = ['error', 'errorKeyMap', 'close']
function XhrErrorDisplayCtrl(error, errorKeyMap, close) {
  error = angular.copy(error)

  console.log(error);//TODO: remove console logging

  if (error.status === 400) {
    error.messages = error.data
    this.errorKeyMap = errorKeyMap
  }
  this.error = error
  this.close = close
}

services.factory('xhrErrorDisplay', xhrErrorDisplay)
xhrErrorDisplay.$inject = ['ModalService']
function xhrErrorDisplay(ModalService) {
  return function handleError(errorObj, errorKeyMap) {
    ModalService.showModal({
      template: require('./xhr-error-display.service.html'),
      controller: 'XhrErrorDisplayCtrl as xhrErrorDisplay',
      inputs: {error: errorObj, errorKeyMap: errorKeyMap}
    }).then(modalHandler)

    function modalHandler(modal) {
      modal.element.dialog({
        modal: true,
        dialogClass: 'no-close',
        title: 'Request Not Completed',
        close: function() {modal.controller.close()}
      })
    }
  }
}
