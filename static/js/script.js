document.addEventListener("DOMContentLoaded", function () {
  initDragAndDrop();
  initClipboard();
  handleAutoScroll();
});

// --- Upload (Drag & Drop) ---
function initDragAndDrop() {
  const dropZone = document.getElementById("drop-zone");
  const fileInput = document.getElementById("file-input");
  const fileName = document.getElementById("file-name");

  if (!dropZone) return;

  dropZone.addEventListener("click", () => fileInput.click());
  dropZone.addEventListener("dragover", (e) => {
    e.preventDefault();
    dropZone.classList.add("dragover");
  });

  dropZone.addEventListener("dragleave", () =>
    dropZone.classList.remove("dragover")
  );

  dropZone.addEventListener("drop", (e) => {
    e.preventDefault();
    dropZone.classList.remove("dragover");
    if (e.dataTransfer.files.length > 0) {
      fileInput.files = e.dataTransfer.files;
      updateFileName(fileInput, fileName);
    }
  });

  fileInput.addEventListener("change", () =>
    updateFileName(fileInput, fileName)
  );
}

function updateFileName(input, displayElement) {
  if (input.files.length > 0) {
    displayElement.textContent = "Arquivo selecionado: " + input.files[0].name;
    displayElement.style.display = "block";
  }
}

// --- Feedback e Interação ---

function mostrarLoading() {
  const btn = document.getElementById("btn-enviar");
  const load = document.getElementById("loading");
  if (btn) btn.style.display = "none";
  if (load) load.style.display = "block";
}

function initClipboard() {
  window.copiarTexto = function () {
    const textoElement = document.getElementById("texto-resposta");
    const btnCopy = document.querySelector(".btn-copy");

    if (textoElement && btnCopy) {
      const texto = textoElement.innerText;
      const originalHtml = btnCopy.innerHTML;

      navigator.clipboard
        .writeText(texto)
        .then(() => {
          // feedback visual de sucesso
          btnCopy.innerHTML = '<i class="fa-solid fa-check"></i> Copiado!';
          btnCopy.classList.add("success");

          // reverte estado após 2s
          setTimeout(() => {
            btnCopy.innerHTML = originalHtml;
            btnCopy.classList.remove("success");
          }, 2000);
        })
        .catch((err) => console.error("Clipboard error:", err));
    }
  };
}

// --- Validação do Formulário ---
// garante que o usuário enviou PDF OU texto
function validarEnvio() {
  const texto = document.getElementById("email_texto").value.trim();
  const arquivoInput = document.getElementById("file-input");
  const temArquivo = arquivoInput.files.length > 0;

  // nada preenchido
  if (!texto && !temArquivo) {
    alert("⚠️ Atenção: Cole um texto ou anexe um arquivo PDF.");
    return false;
  }

  // arquivo Gigante (mais de 2MB)
  if (temArquivo) {
    const arquivo = arquivoInput.files[0];
    const limiteMB = 2;
    const limiteBytes = limiteMB * 1024 * 1024;

    if (arquivo.size > limiteBytes) {
      alert(
        `⚠️ Arquivo muito grande! O limite é de ${limiteMB}MB.\nO seu arquivo tem ${(
          arquivo.size /
          1024 /
          1024
        ).toFixed(2)}MB.`
      );
      return false;
    }
  }
  mostrarLoading();
  return true;
}

// --- Auto-Scroll para Resultados ---
function handleAutoScroll() {
  // delay para garantir renderização completa
  setTimeout(function () {
    const card = document.getElementById("box-principal");
    const resultado = document.querySelector(".resultado-box");
    const urlParams = new URLSearchParams(window.location.search);

    // rola se houver resultado ou se for um reset (param ?limpar=true)
    if ((resultado || urlParams.has("limpar")) && card) {
      card.scrollIntoView({ behavior: "smooth", block: "start" });
    }
  }, 100);
}
