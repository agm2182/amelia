(() => {
  var grid = document.querySelector('[role="grid"]');
  if (!grid) return 'No grid found';
  var rows = grid.querySelectorAll('[role="row"]');
  var count = 0;
  for (var i = 1; i < rows.length; i++) {
    var cells = rows[i].querySelectorAll('[role="gridcell"]');
    var date = cells[0] ? cells[0].textContent.trim() : '';
    if (date && date.match(/\d{2}\/\d{2}\/\d{4}/)) count++;
  }
  return 'Data rows: ' + count + ' (total rows: ' + rows.length + ')';
})()
