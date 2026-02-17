(() => {
  var grid = document.querySelector('[role="grid"]');
  if (!grid) return 'ERROR:No grid';
  var rows = grid.querySelectorAll('[role="row"]');
  for (var i = 1; i < rows.length; i++) {
    var cells = rows[i].querySelectorAll('[role="gridcell"]');
    if (cells.length < 5) continue;
    var date = cells[0] ? cells[0].textContent.trim() : '';
    if (date && date.match(/\d{2}\/\d{2}\/\d{4}/)) {
      var memo = cells[3] ? cells[3].textContent.trim().substring(0, 40) : '';
      var dec = cells[7] ? cells[7].textContent.trim() : '';
      cells[0].click();
      return 'CLICKED:' + date + '|' + memo + '|DEC=' + dec;
    }
  }
  return 'DONE:No entries found';
})()
