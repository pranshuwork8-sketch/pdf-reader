const BACKEND = "https://YOUR-BACKEND-URL.onrender.com";

function uploadPDF() {
  let file = document.getElementById("file").files[0];
  let data = new FormData();
  data.append("file", file);

  fetch(BACKEND + "/upload/pdf", {
    method: "POST",
    body: data
  }).then(res => res.json()).then(alert);
}

function uploadImage() {
  let file = document.getElementById("file").files[0];
  let data = new FormData();
  data.append("file", file);

  fetch(BACKEND + "/upload/image", {
    method: "POST",
    body: data
  }).then(res => res.json()).then(alert);
}

function getSummary() {
  let level = document.getElementById("level").value;

  fetch(`${BACKEND}/summary?level=${level}`)
    .then(res => res.json())
    .then(data => {
      document.getElementById("summary").innerText =
        data.summary.join(". ");
    });
}

function ask() {
  let q = document.getElementById("question").value;

  fetch(BACKEND + "/ask", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({question: q})
  })
  .then(res => res.json())
  .then(data => {
    document.getElementById("answer").innerText = data.answer;
  });
}

function getChart() {
  fetch(BACKEND + "/chart")
    .then(res => res.json())
    .then(data => {
      document.getElementById("chart").src =
        "data:image/png;base64," + data.image;
    });
}
