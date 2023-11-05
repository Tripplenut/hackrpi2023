const output = document.getElementById("output");

(async () => {
  const link = "https://python-chess.readthedocs.io/en/latest/"
  const query = "working chess engine"
  const xhr = new XMLHttpRequest();
  const url = `https://b17e-2620-0-2820-220e-2bb5-9ab1-2502-f436.ngrok-free.app/?q=${query}&url=${link}`;
  console.log(url);

  xhr.onreadystatechange = () => {
    if (xhr.readyState == XMLHttpRequest.DONE) {
      output.innerText = xhr.responseText
    }
  }

  xhr.open("GET", url, true);
  xhr.setRequestHeader("Content-Type", "text/plain");
  xhr.send();
})();
