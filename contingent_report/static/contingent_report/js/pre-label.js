$(function () {
  "use strict";

  var $preLabel, $targetCtrl;

  $preLabel = $('pre[data-label-for]');

  $targetCtrl = $("#" + ($preLabel.data('label-for')));

  if ($targetCtrl.val()) {
    $preLabel.hide();
  }

  $preLabel.css({
    position: 'absolute',
    top: 10,
    left: 25,
    margin: 0,
    padding: 0,
    color: '#ADACAC',
    display: 'block',
    border: 0,
    cursor: 'text',
    'background-color': 'initial',
    'white-space': 'pre-line',
    'border-radius': 0
  }).on('click', function () {
    var $el;
    $el = $(this);
    if ($targetCtrl.val) {
      if ($targetCtrl.val()) {
        $el.hide();
      } else {
        $targetCtrl.focus();
        $el.show();
      }
    } else if ($targetCtrl.text) {
      if ($targetCtrl.text()) {
        $el.hide();
      } else {
        $el.show();
      }
    }
    return $targetCtrl.focus();
  }).next().on({
    'focusout': function () {
      var $el;
      $el = $(this);
      if ($el.val) {
        if (!$el.val()) {
          return $el.prev().show();
        } else {
          return $el.prev().hide();
        }
      } else if ($el.text) {
        if (!$el.text()) {
          return $el.prev().show();
        } else {
          return $el.prev().hide();
        }
      }
    },
    'focusin': function () {
      var $el;
      $el = $(this);
      return $el.prev().hide();
    }
  });
})
