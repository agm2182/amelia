(() => {
  var grid = document.querySelector('[role="grid"]');
  if (!grid) return 'No grid';
  var rows = grid.querySelectorAll('[role="row"]');
  for (var i = 1; i < rows.length; i++) {
    var cells = rows[i].querySelectorAll('[role="gridcell"]');
    var date = cells[0] ? cells[0].textContent.trim() : '';
    if (date && date.match(/\d{2}\/\d{2}\/\d{4}/)) {
      var memo = cells[3] ? cells[3].textContent.trim().substring(0, 50) : '';
      var inc = cells[6] ? cells[6].textContent.trim() : '';
      var dec = cells[7] ? cells[7].textContent.trim() : '';
      var bal = cells[11] ? cells[11].textContent.trim() : '';
      return date + ' | Memo: ' + memo + ' | INC=' + inc + ' | DEC=' + dec + ' | BAL=' + bal;
    }
  }
  return 'No data rows';
})()
