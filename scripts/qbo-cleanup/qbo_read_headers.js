(() => {
  var grid = document.querySelector('[role="grid"]');
  if (!grid) return 'No grid';
  var rows = grid.querySelectorAll('[role="row"]');
  var headerRow = rows[0];
  var cells = headerRow.querySelectorAll('[role="columnheader"]');
  var result = [];
  for (var i = 0; i < cells.length; i++) {
    var t = cells[i].textContent.trim();
    if (t) result.push(i + ':' + t);
  }
  return result.join(' | ');
})()
