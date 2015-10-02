"use strict";

var formMCommons = require('formMCommons')

var app = angular.module('display-pending-bid', ['kanmii-underscore'])

app.directive('displayPendingBid', displayPendingBidDirective)
function displayPendingBidDirective() {
  return {
    restrict: 'EA',

    templateUrl: formMCommons.buildUrl('bid-request/display-pending-bid/display-pending-bid.html'),

    scope: {},

    bindToController: {
      bids: '=pendingBids',

      updateCollection: '&',

      pager: '=pagerObject',

      onDblClick: '&onRowDblClickCallback',

      newModel: '=',

      paginationSize: '=',

      selectedBids: '='
    },

    controller: 'displayPendingBidDirectiveCtrl as bidTable'
  }
}

app.controller('displayPendingBidDirectiveCtrl', displayPendingBidDirectiveCtrl)
displayPendingBidDirectiveCtrl.$inject = [
  'pagerNavSetUpLinks',
  '$scope',
  'kanmiiUnderscore'
]
function displayPendingBidDirectiveCtrl(pagerNavSetUpLinks, scope, kanmiiUnderscore) {
  var vm = this //jshint -W040

  vm.selectedBids = {}

  function setUpLinks(next, prev, count) {

    var numLinks = Math.ceil(count / vm.paginationSize)

    var linkProperties = pagerNavSetUpLinks(next, prev, numLinks)

    vm.nextPageLink = next
    vm.prevPageLink = prev

    vm.linkUrls = linkProperties.linkUrls
    vm.currentLink = linkProperties.currentLink

    /**
     * The row index offset. The row begin at one so in the view, we do `$index + 1` for row number. However, as we
     * move from page to page, the `$index` view value is reset back to zero, so that row number always begin at 1.
     * Since we know what the page number is (this.currentLink), we calculate the offset for the row (as an arithmetic
     * progression)
     * @type {number}
     */
    vm.rowIndexOffset = (vm.currentLink - 1) * vm.paginationSize
  }

  vm.onUpdateCollection = onUpdateCollection
  function onUpdateCollection(linkUrl) {
    vm.updateCollection({linkUrl: linkUrl})
  }

  scope.$watch(function getPager() {return vm.pager}, function updatedPager(pager) {
    if (pager && !kanmiiUnderscore.isEmpty(pager)) {
      setUpLinks(pager.next, pager.previous, pager.count)
    }
  })

  function deselectAllBids() {
    vm.bids.forEach(function(bid) {
      bid.highlighted = false
    })
  }

  vm.modelRowClicked = modelRowClicked
  function modelRowClicked(model) {
    if (!model.downloaded) {
      deselectAllBids()
      //only highlight a row if no row is checked and the row model is not downloaded previously
      model.highlighted = !kanmiiUnderscore.any(vm.bids, function(bid) {
        return bid.checked
      })
    }
  }

  scope.$watch(function getSelectedBids() {return vm.selectedBids}, function updatedSelectedBids(selectedBids) {
    if (selectedBids && !kanmiiUnderscore.isEmpty(selectedBids)) {

      kanmiiUnderscore.each(selectedBids, function(checked, id) {

        for (var bidIndex = 0; bidIndex < vm.bids.length; bidIndex++) {
          var bid = vm.bids[bidIndex]
          if (bid.id === +id) {
            bid.checked = checked

            if (!checked) {
              vm.toggleAll = false
            }
          }
        }

      })

      var checked = kanmiiUnderscore.all(vm.bids, function(bid) {
        return bid.checked === true
      })

      if (checked) vm.toggleAll = true
    }
  }, true)

  vm.toggleAll = null

  vm.toggleAllClicked = function toggleAllClicked() {
    vm.bids.forEach(function(bid) {
      vm.selectedBids[bid.id] = vm.toggleAll
    })
  }
}