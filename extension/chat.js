const API_BASE = "http://localhost:8000";

const loader = document.getElementById("loader");
const responseDiv = document.getElementById("response");

function addMessage(role, text) {
  const div = document.createElement("div");
  div.className = "msg";
  div.innerHTML = `<span class="${role}">${role === "user" ? "Você" : "IA"}:</span> <span class="${role === "user" ? "" : "bot"}">${text}</span>`;
  responseDiv.appendChild(div);
  responseDiv.scrollTop = responseDiv.scrollHeight;
}

async function transcribe() {
  const url = document.getElementById("videoUrl").value;
  loader.style.display = "block";
  responseDiv.innerHTML = "";

  try {
    const res = await fetch(`${API_BASE}/transcribe`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ url })
    });
    const data = await res.json();
    loader.style.display = "none";
    if (res.ok) {
      addMessage("bot", "✅ Transcrição concluída! Você pode perguntar sobre o vídeo.");
    } else {
      addMessage("bot", `Erro: ${data.detail}`);
    }
  } catch (err) {
    loader.style.display = "none";
    addMessage("bot", "Erro ao conectar com a API.");
  }
}

async function ask() {
  const question = document.getElementById("question").value;
  if (!question) return;

  addMessage("user", question);
  addMessage("bot", "⏳ Pensando...");

  try {
    const res = await fetch(`${API_BASE}/ask`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question })
    });
    const data = await res.json();

    responseDiv.removeChild(responseDiv.lastChild);

    if (res.ok) {
      addMessage("bot", data.answer);
    } else {
      addMessage("bot", `Erro: ${data.detail}`);
    }
  } catch (err) {
    responseDiv.removeChild(responseDiv.lastChild);
    addMessage("bot", "Erro ao conectar com a API.");
  }

  document.getElementById("question").value = "";
}

document.addEventListener("DOMContentLoaded", () => {
  document.getElementById("transcribeBtn").addEventListener("click", transcribe);
  document.getElementById("askBtn").addEventListener("click", ask);
});
