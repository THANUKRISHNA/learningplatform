async function runCode() {
  const input = document.getElementById("code").value;
  const worker = new Worker('C:\Users\lenovo\OneDrive\Documents\learningplatform\frontend\static\js\python-worker.js');
  worker.postMessage(input);

  r
  worker.onmessage = function(event) {
    document.getElementById("output").textContent = event.data;
  };

  worker.terminate();
}

function scrollFunction() {
    if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
      document.getElementById("imageContainer").style.transform = "scale(1.05)";
    } else {
      document.getElementById("imageContainer").style.transform = "scale(1)";
    }
  }
  
  document.addEventListener("DOMContentLoaded", function() {

    setTimeout(function() {
      var modal = document.getElementById("myModal");
      if (modal) {
        modal.style.display = "block";
      }
    }, 10000);
    var closeBtn = document.querySelector(".close");
    if (closeBtn) {
      closeBtn.addEventListener("click", function() {
        var modal = document.getElementById("myModal");
        if (modal) {
          modal.style.display = "none";
        }
      });
    }
  
    window.onscroll = function() {
      scrollFunction();
    };
  });
  
 