self.addEventListener('message', function(e) {
    const input = e.data;
    let output = '';
  
    try {
      
      const python = new PythonShell('path/to/python-interpreter.js');
      python.add_to_namespace({
        main: function() {
          return eval(input);
        }
      });
      python.run('main()').then(function(result) {
        self.postMessage(result);
      });
    } catch (err) {
      self.postMessage(err.message);
    }
  }, false);