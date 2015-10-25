"use strict";

var rootCommons = require('commons')

var app = angular.module('lc-cover', [
  'rootApp'
])

app.directive('lcCover', lcIssueDirective)

lcIssueDirective.$inject = []

function lcIssueDirective() {
  return {
    restrict: 'A',
    templateUrl: require('lcAppCommons').buildUrl('form-m/lc-cover/lc-cover.html'),
    scope: true,
    bindToController: {
      formM: '=mfContext',
      cover: '=',
      onCoverChanged: '&'
    },
    controller: 'LcCoverDirectiveController as lcCover'
  }
}

app.controller('LcCoverDirectiveController', LcCoverDirectiveController)

LcCoverDirectiveController.$inject = ['$scope', 'formMCoverTypes', '$filter']

function LcCoverDirectiveController($scope, formMCoverTypes, $filter) {
  var vm = this
  var title = 'Register Cover'
  init()

  function init(form) {
    vm.title = title
    vm.showContainer = false
    vm.cover = {}
    vm.coverTypes = null

    if (form) {
      form.$setPristine()
      form.$setUntouched()
    }
  }

  vm.isValid = isValid
  /**
   * A function whose return value is used to evaluate whether a form control element has error or success
   * @param {string} name the name of a form control
   * @param {string|null} validity the type of validity to check for, 'ok' means valid while undefined means invalid
   * @returns {boolean}
   */
  function isValid(name, validity) {
    return $scope.coverForm[name].$dirty && $scope.coverForm[name][validity === 'ok' ? '$valid' : '$invalid']
  }

  vm.amountGetterSetter = function(val) {
    if (arguments.length) {
      if (!/[\d,\.]+/.test(val)) vm.cover.amount = null
      else vm.cover.amount = Number(val.replace(/,/g, ''))
    } else return vm.cover.amount ? $filter('number')(vm.cover.amount, 2) : undefined
  }

  vm.toggleShow = function toggleShow(form) {
    vm.showContainer = vm.formM.amount && vm.formM.number && !vm.showContainer

    if (!vm.showContainer) {
      init(form)
    }
    else {
      vm.title = 'Dismiss'
      vm.coverTypes = formMCoverTypes
      vm.cover.amount = vm.formM.amount
    }
  }

  $scope.$watch(function getFormM() {return vm.formM}, function(newFormM) {
    if (newFormM) {
      var number = newFormM.number
      var amount = newFormM.amount

      if (!number || !amount) init()
    }
  }, true)

  $scope.$watch(function getCover() {return vm.cover}, function(newCover) {
    vm.onCoverChanged({
      cover: newCover, coverForm: $scope.coverForm
    })

  }, true)
}
