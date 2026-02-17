(() => {
  var grid = document.querySelector('[role="grid"]');
  if (!grid) return 'No grid';
  var hdrRow = grid.querySelectorAll('[role="row"]')[0];
  var hdrs = hdrRow.querySelectorAll('[role="columnheader"]');
  var hdrMap = [];
  for (var h = 0; h < hdrs.length; h++) {
    hdrMap.push(h + ':' + hdrs[h].textContent.trim());
  }
  var rows = grid.querySelectorAll('[role="row"]');
  var results = ['HEADERS: ' + hdrMap.join(' | ')];
  var count = 0;
  for (var i = 1; i < rows.length && count < 5; i++) {
    var cells = rows[i].querySelectorAll('[role="gridcell"]');
    var date = cells[0] ? cells[0].textContent.trim() : '';
    if (!date || !date.match(/\d{2}\/\d{2}\/\d{4}/)) continue;
    var parts = [];
    for (var j = 0; j < cells.length; j++) {
      var t = cells[j].textContent.trim();
      if (t) parts.push(j + ':' + t.substring(0, 50));
    }
    results.push(parts.join(' | '));
    count++;
  }
  return results.join('\n');
})()
