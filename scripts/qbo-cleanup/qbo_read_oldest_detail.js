(() => {
  var grid = document.querySelector('[role="grid"]');
  if (!grid) return 'No grid';
  var rows = grid.querySelectorAll('[role="row"]');
  var results = [];
  for (var i = rows.length - 1; i >= 1; i--) {
    var cells = rows[i].querySelectorAll('[role="gridcell"]');
    var date = cells[0] ? cells[0].textContent.trim() : '';
    if (!date || !date.match(/\d{2}\/\d{2}\/\d{4}/)) continue;
    var memo = cells[3] ? cells[3].textContent.trim().substring(0, 70) : '';
    var pmt = cells[6] ? cells[6].textContent.trim() : '';
    var dep = cells[7] ? cells[7].textContent.trim() : '';
    var bal = cells[11] ? cells[11].textContent.trim() : '';
    var typ = cells[13] ? cells[13].textContent.trim() : '';
    results.push(date + ' | ' + (pmt ? 'PMT=' + pmt : 'DEP=' + dep) + ' | BAL=' + bal + ' | ' + typ + ' | ' + memo);
    if (results.length >= 20) break;
  }
  return results.join('\n');
})()
