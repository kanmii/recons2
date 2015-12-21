// Generated by CoffeeScript 1.6.3
var PATTERNS, getQueryParam;

PATTERNS = {
  LC_RE: /LC CHGS REF\/(ILCL[A-Z]{3}\d{9})(?:\/[A-Z]{3,})?/,
  FORMM_RE: /MF[\dA-Z]{7,}\/FM[LB]C (BA|CB)[\s\dA-Z]{8,}(?:\/[A-Z]{3,})?/,
  BILLS_RE: /COMM BC [A-Z]{3}[0-9,\.]{2,}\/(FOBC\d{8})(?:\/[A-Z]{3,})?/,
  OUT_RE: /TIREF ((?:FCO|OT[EG])\d{9})\/FT TO [^\/]+\/[^\/]+\/\w+/i,
  INW_RE: /TIREF (CF[EGC]\d{9})\/TF BY [^\/]+\/[^\/]+\/\w+/i
};

getQueryParam = function(text) {
  var matched;
  matched = PATTERNS.FORMM_RE.exec(text);
  if (matched) {
    return matched[0];
  }
  matched = PATTERNS.LC_RE.exec(text);
  if (matched) {
    return matched[1];
  }
  matched = PATTERNS.BILLS_RE.exec(text);
  if (matched) {
    return matched[1];
  }
  matched = PATTERNS.OUT_RE.exec(text);
  if (matched) {
    return matched[1];
  }
  matched = PATTERNS.INW_RE.exec(text);
  if (matched) {
    return matched[1];
  }
  return null;
};

$(function() {
  var $downloadBtn, $getBtn, $tbody, $textArea, $trClonable, displayRow, getAcct, reset, url;
  $textArea = $('#income2-text');
  $trClonable = $('#tr-clonable');
  $getBtn = $('#get-btn');
  $downloadBtn = $('#download-btn');
  $tbody = $('tbody');
  url = $('form').data('url');
  displayRow = function(rowArray) {
    var $tds, $tr;
    $tr = $trClonable.clone();
    $tbody.append($tr);
    $tds = $tr.children();
    $tds.filter('.gl').text(rowArray[0]);
    $tds.filter('.trxn-dt').text(rowArray[1]);
    $tds.filter('.ref').text(rowArray[2]);
    $tds.filter('.narr').text(rowArray[3]);
    $tds.filter('.val-dt').text(rowArray[4]);
    $tds.filter('.ccy').text(rowArray[5]);
    $tds.filter('.lcy-amt').text(rowArray[6]);
    $tds.filter('.fcy-amt').text(rowArray[7]);
    $tds.filter('.acct').text(rowArray[8]);
    return $tr.show();
  };
  getAcct = function(filterParam) {
    var filterParamEncoded;
    filterParamEncoded = encodeURIComponent(filterParam);
    return $.get("" + url + "?filter_param=" + filterParamEncoded);
  };
  reset = function() {
    $trClonable.siblings().remove();
    return $downloadBtn.prop('disabled', true);
  };
  $textArea.on({
    'focusout': function(evt) {
      var $el;
      $el = $(this);
      return $el.val(function(index, OldVal) {
        return kanmii.strip(OldVal);
      });
    },
    'change': function(evt) {
      var $el, val;
      $el = $(this);
      val = $el.val();
      if (val) {
        return $getBtn.prop('disabled', false);
      } else {
        return $getBtn.prop('disabled', true);
      }
    }
  });
  $getBtn.on({
    'click': function(evt) {
      var incomeText;
      evt.preventDefault();
      reset();
      incomeText = $textArea.val();
      if (!incomeText) {
        return;
      }
      $.parse(incomeText, {
        header: false,
        dynamicTyping: false,
        delimiter: '\t',
        step: function(data) {
          var ajaxGet, errors, filterParam, items, results;
          results = data.results, errors = data.errors;
          items = results[0];
          filterParam = getQueryParam(items[3]);
          if (filterParam) {
            ajaxGet = getAcct(filterParam);
            return ajaxGet.done(function(resp) {
              items[8] = resp;
              return displayRow(items);
            }).fail(function(resp) {
              console.log(filterParam);
              return console.log(resp);
            });
          }
        }
      });
      return $downloadBtn.prop('disabled', false);
    }
  });
  return $downloadBtn.on({
    'click': function(evt) {
      var result;
      if ($tbody.children().size() > 1) {
        result = kanmii.selectText($('table')[0]).toString();
        return saveAs(new Blob([result], {
          type: 'application/xls'
        }), 'income2.txt');
      }
    }
  });
});
