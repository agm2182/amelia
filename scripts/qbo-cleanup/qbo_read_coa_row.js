(() => {
  var rows = document.querySelectorAll('tr, [role="row"]');
  var result = [];
  for (var i = 0; i < rows.length; i++) {
    if (rows[i].textContent.indexOf('Capital One Checking') >= 0) {
      var cells = rows[i].querySelectorAll('td');
      var parts = [];
      for (var j = 0; j < cells.length; j++) {
        var t = cells[j].textContent.trim();
        if (t) parts.push(j + ':' + t);
      }
      result.push(parts.join(' | '));
    }
  }
  return result.join('\n') || 'Not found';
})()
