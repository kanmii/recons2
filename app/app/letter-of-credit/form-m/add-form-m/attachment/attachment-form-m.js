"use strict";

/*jshint camelcase:false*/

var app = angular.module( 'form-m-attachment', [
  'rootApp',
  'add-attachment',
  'attachment-service',
  'confirmation-dialog',
] )

app.directive( 'formMAttachment', formMAttachmentDirective )

formMAttachmentDirective.$inject = []

function formMAttachmentDirective() {
  return {
    restrict: 'A',
    templateUrl: require( 'commons' ).buildUrl(
      'letter-of-credit', 'form-m/add-form-m/attachment/attachment-form-m.html' ),
    scope: true,
    controller: 'FormMAttachmentDirectiveController as formMAttachment'
  }
}

app.controller( 'FormMAttachmentDirectiveController', FormMAttachmentDirectiveController )

FormMAttachmentDirectiveController.$inject = [
  'formMObject',
  'underscore',
  '$scope',
  'Attachment',
  'AttachmentFile',
  'confirmationDialog'
]

function FormMAttachmentDirectiveController(formMObject, underscore, $scope, Attachment, AttachmentFile,
  confirmationDialog) {
  var vm = this
  vm.formM = formMObject

  init()
  function init() {
    vm.showAttachment = false
    vm.showAddAttachmentForm = showAddAttachmentForm()

    /**
     * A mapping from attachment file ID to corresponding value of checked i.e
     * {1: true, 2: false}, where the keys are the attachment file IDs and the value will be whether attachment file
     * is checked or not
     * @type {{}}
     */
    vm.selectedAttachmentFiles = {}

    /**
     * A mapping from attachment ID to corresponding value of checked i.e
     * {1: true, 2: false}, where the keys are the attachment IDs and the value will be whether attachment
     * is checked or not
     * @type {{}}
     */
    vm.selectedAttachments = {}

    vm.selectedAttachmentsLen = 0
    vm.selectedAttachmentFilesLen = 0
  }

  function checkAttachmentFiles(selectedAttachmentFiles) {
    vm.selectedAttachmentFilesLen = 0

    underscore.each( selectedAttachmentFiles, function (checked, id) {
      if ( checked ) ++vm.selectedAttachmentFilesLen

      var file = getAttachmentFileFromId( id )
      if ( file ) file.checked = checked
    } )

    //if ( formMObject.attachments.length && !vm.selectedAttachmentFilesLen ) vm.selectedAttachmentFiles = {}
  }

  function getAttachmentFileFromId(id) {
    var lenAttachments = formMObject.attachments.length

    for ( var attachmentIndex = 0; attachmentIndex < lenAttachments; attachmentIndex++ ) {
      var files = vm.formM.attachments[attachmentIndex].files
      var lenFiles = files.length

      for ( var fileIndex = 0; fileIndex < lenFiles; fileIndex++ ) {
        var file = files[fileIndex]
        if ( file.id === +id ) return file
      }
    }

    return null
  }

  function checkAttachments(selectedAttachments) {
    vm.selectedAttachmentsLen = 0

    underscore.each( selectedAttachments, function (checked, id) {
      if ( checked ) ++vm.selectedAttachmentsLen

      var attachment = getAttachmentFromId( id )
      if ( attachment ) attachment.checked = checked
    } )
  }

  function getAttachmentFromId(id) {
    var len = formMObject.attachments.length

    for ( var attachmentIndex = 0; attachmentIndex < len; attachmentIndex++ ) {
      var attachment = formMObject.attachments[attachmentIndex]

      if ( attachment.id === +id ) return attachment
    }

    return null
  }

  function showAddAttachmentForm() {
    return !formMObject.attachments.length
  }

  vm.attachmentContext = {
    content_type: formMObject.ct_url,
    object_id: formMObject._id
  }

  vm.toggleShow = function toggleShow() {
    vm.showAttachment = formMObject._id && !vm.showAttachment

    if ( vm.showAttachment ) vm.showAddAttachmentForm = showAddAttachmentForm()
  }

  vm.toggleAddAttachmentForm = function toggleAddAttachmentForm() {

  }

  vm.attachmentFileAdded = function attachmentFileAdded(attachmentFileAddedResult) {
    console.log( attachmentFileAddedResult )

    if ( attachmentFileAddedResult.result ) {
      formMObject.setAttachments()
    }
  }

  vm.refreshAttachments = function refreshAttachments() {
    vm.selectedAttachmentFiles = {}
    vm.selectedAttachments = {}
    formMObject.setAttachments()
  }

  vm.getFileName = function getFileName(name) {
    var len = name.length

    if ( len < 41 ) return name

    var EXT_REGEX = new RegExp( "\\.[\\w]+$", 'i' )
    var ext = EXT_REGEX.exec( name )
    ext = ext ? ext[0] : ''
    var extLen = ext.length
    len = len - extLen
    name = name.replace( EXT_REGEX, '' )

    return name.slice( 0, 27 ) + '...' + name.slice( len - 5 ) + ext
  }

  vm.doAction = function doAction(action) {
    console.log( 'doAction = ', action )

    switch (action) {

      case 'delete-attachment':
      {
        deleteAttachment()
        break
      }

      case 'delete-file':
      {
        deleteAttachmentFile()
      }
    }
  }

  function deleteAttachment() {
    console.log( 'vm.selectedAttachments = ', vm.selectedAttachments )
  }

  function deleteAttachmentFile() {
    console.log( 'vm.selectedAttachmentFiles = ', vm.selectedAttachmentFiles )
  }

  $scope.$watch( function getFormMObject() {return formMObject}, function onFormMObjectChanged(formM) {

    if ( formM ) {
      if ( !formM.amount || !formM.number ) {
        init()
      }
    }
  }, true )

  $scope.$watch( function getSelectedAttachments() {return vm.selectedAttachments},
    function onSelectedAttachmentsChanged(selectedAttachments) {
      if ( selectedAttachments ) {
        //console.log( 'selectedAttachments = ' , selectedAttachments)
        checkAttachments( selectedAttachments )
      }
    }, true )

  $scope.$watch( function getSelectedAttachmentFiles() {return vm.selectedAttachmentFiles},
    function onSelectedAttachmentFilesChanged(selectedAttachmentFiles) {

      if ( selectedAttachmentFiles ) {
        //console.log( 'selectedAttachmentFiles = ', selectedAttachmentFiles )
        checkAttachmentFiles( selectedAttachmentFiles )
      }
    }, true )
}