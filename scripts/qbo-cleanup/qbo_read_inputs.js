(() => {
  var inputs = document.querySelectorAll('input[type="text"], input:not([type])');
  var result = [];
  for (var i = 0; i < inputs.length; i++) {
    var inp = inputs[i];
    var label = inp.getAttribute('aria-label') || inp.getAttribute('placeholder') || inp.name || '';
    if (inp.value) result.push(label + '=' + inp.value);
  }
  return result.join(' | ');
})()
