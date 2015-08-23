// Generated by CoffeeScript 1.7.1
$(function() {
  var $checkAll, $checkOne, $manualPostingBtn, $summary, $tbody, POSTDATATDSELECTOR, TOTAL_POST_DATA_TD, el, postingCheck, tabVal, _i, _len, _ref;
  $checkAll = $('input[type=checkbox]:first');
  $checkOne = $('input[type=checkbox]:not(:first)');
  postingCheck = [];
  $tbody = $('tbody');
  $manualPostingBtn = $('.post-table>img');
  POSTDATATDSELECTOR = 'td:nth-last-child(-n+7):not(:last-child)';
  $summary = $('.summary-div');
  TOTAL_POST_DATA_TD = 6;
  $summary.on({
    "mouseenter": function(evt) {
      return $(this).children().show().last().get(0).scrollIntoView(false);
    },
    "mouseleave": function(evt) {
      return $(this).children().hide();
    }
  });
  tabVal = 1;
  _ref = $(POSTDATATDSELECTOR);
  for (_i = 0, _len = _ref.length; _i < _len; _i++) {
    el = _ref[_i];
    if (el.innerText !== '') {
      $(el).prop('tabindex', tabVal++);
    }
  }
  $('table').checkOneAll('input[type=checkbox]:not(:first)', 'input[type=checkbox]:first');
  $tbody.on({
    'focusin': function() {
      return $(this).addClass('selected');
    },
    'focusout': function() {
      var $el;
      $el = $(this);
      return $el.removeClass('selected');
    }
  }, 'tr');
  $tbody.on({
    'focusout': function() {
      var $el, val;
      $el = $(this);
      $el.prop('contenteditable', false);
      if ($el.is('.manual-posting') && $el.text()) {
        $el.prop('tabindex', parseInt($el.siblings().get(1).innerText) * TOTAL_POST_DATA_TD);
      }
      if ($el.is(':nth-child(4)')) {
        val = kanmii.numberFormat($el.text());
        if (val) {
          return $el.text(val);
        }
      }
    },
    'dblclick': function() {
      return $(this).prop('contenteditable', true);
    },
    'focus click': function() {
      $(this).removeClass('text-copied');
      return kanmii.selectText(this);
    }
  }, POSTDATATDSELECTOR);
  $('th>span:first').click(function() {
    var csrfToken, postIdsArray, posting, url, _ref1;
    _ref1 = $('.post-table>span:first').text().split('|'), url = _ref1[0], csrfToken = _ref1[1];
    postIdsArray = (function() {
      var _j, _len1, _ref2, _results;
      _ref2 = $checkOne.filter(':checked');
      _results = [];
      for (_j = 0, _len1 = _ref2.length; _j < _len1; _j++) {
        el = _ref2[_j];
        _results.push(el.value);
      }
      return _results;
    })();
    if (postIdsArray.length) {
      posting = $.post(url, {
        ids: JSON.stringify(postIdsArray),
        csrfmiddlewaretoken: csrfToken
      });
      posting.done(function(data) {
        var dataObj;
        dataObj = JSON.parse(data);
        return $checkOne.each(function() {
          if (dataObj[el.value] === true) {
            $(this).parent().siblings().last().empty().text('Posted');
            postingCheck.push(true);
          }
        });
      });
      return posting.fail(function(error) {
        return alert("Error status: " + error.status + "\nError response text: " + error.responseText);
      });
    }
  });
  $('th>span:last').click(function() {
    var $batchNoBox, batchNo;
    $batchNoBox = $('#id-batch-no');
    batchNo = $batchNoBox.val();
    if (!batchNo || batchNo.length < 4) {
      $batchNoBox.addClass('empty-batch-no');
      return;
    }
    if (!kanmii.all(postingCheck)) {
      if (!window.confirm("Entries not marked as posted, are you sure you want to continue?")) {
        return;
      }
    }
    $('caption').text("Batch " + batchNo);
    $('.batch-no-div').remove();
    $('tr').children(':last-child').remove();
    $('tr').children(':first-child').remove();
    $manualPostingBtn.remove();
    return $summary.remove();
  });
  return $manualPostingBtn.click(function(evt) {
    var $prevTr, $prevTrKids, $tr, $trKids, index, numRows;
    $tr = $('<tr>');
    $tbody.append($tr);
    numRows = $tbody.children().size();
    $tr.append($('<td>'), $('<td>', {
      text: numRows
    }), (function() {
      var _j, _ref1, _results;
      _results = [];
      for (index = _j = 1, _ref1 = TOTAL_POST_DATA_TD - 1; 1 <= _ref1 ? _j <= _ref1 : _j >= _ref1; index = 1 <= _ref1 ? ++_j : --_j) {
        _results.push($('<td>', {
          contenteditable: true,
          tabindex: index + (numRows - 1) * TOTAL_POST_DATA_TD
        }));
      }
      return _results;
    })(), $('<td>', {
      contenteditable: true,
      "class": 'manual-posting'
    }), $('<td>'));
    $prevTr = $tr.prev();
    $trKids = $tr.children(POSTDATATDSELECTOR);
    if ($prevTr.size()) {
      $prevTrKids = $prevTr.children();
      if ((parseInt($prevTrKids.eq(1).text()) % 2) !== 0) {
        $prevTrKids.filter(POSTDATATDSELECTOR).each(function(index, el) {
          if (_.contains([1, 3, 4, 5], index)) {
            $trKids.eq(index).text(el.innerText);
          }
          if ((index === 2) && /^d/i.test(el.innerText)) {
            $trKids.eq(index).text('CR');
          }
          $trKids.addClass('text-copied');
        });
      }
    }
    return $trKids.eq(0).focus();
  });
});
