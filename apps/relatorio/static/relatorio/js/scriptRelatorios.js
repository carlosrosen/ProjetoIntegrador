// Modal - abrir e fechar
function fecharModal() {
  const modal = document.getElementById("modalTransacao");
  modal.classList.remove("ativo");
}

// Lista de transações
let transacoes = [];

document.getElementById("formTransacao")?.addEventListener("submit", function (event) {
  event.preventDefault();
  const formData = new FormData(event.target);
  const descricao = formData.get("descricao");
  const valor = parseFloat(formData.get("valor"));
  const tipo = formData.get("tipo");

  if (!descricao || isNaN(valor)) {
    alert("Preencha os campos corretamente.");
    return;
  }

  transacoes.push({
    id: Date.now(),
    descricao,
    valor,
    tipo
  });

  alert(`Transação adicionada:\n${descricao} - R$ ${valor.toFixed(2)} (${tipo})`);
  atualizarSaldo();
  fecharModal();
  event.target.reset();
});


document.addEventListener("DOMContentLoaded", () => {
  const tabs = document.querySelectorAll(".tab");
  const camposDespesa = document.getElementById("camposDespesa");
  const camposReceita = document.getElementById("camposReceita");
  const condicaoPagamento = document.getElementById("condicaoPagamento");
  const campoParcelas = document.getElementById("campoParcelas");
  const btnAbrir = document.getElementById("abrirModalTransacao");
  const modal = document.getElementById("modalTransacao");

  tabs.forEach(tab => {
    tab.addEventListener("click", () => {
      tabs.forEach(t => t.classList.remove("active"));
      tab.classList.add("active");

      const tipo = tab.getAttribute("data-tipo");

      if (tipo === "saida") {
        camposDespesa.style.display = "block";
        camposReceita.style.display = "none";
      } else {
        camposDespesa.style.display = "none";
        camposReceita.style.display = "block";
      }
    });
  });

  condicaoPagamento?.addEventListener("change", () => {
    campoParcelas.style.display = condicaoPagamento.value === "parcelado" ? "block" : "none";
  });

  btnAbrir?.addEventListener("click", () => {
    modal.classList.add("ativo");
  });
});

function fecharModalMeta() {
  document.getElementById("modalMeta")?.classList.remove("ativo");
}

document.getElementById("formMeta")?.addEventListener("submit", function (event) {
  event.preventDefault();
  const formData = new FormData(event.target);
  const nome = formData.get("nomeMeta");
  const tipo = formData.get("tipoMeta");
  const valor = parseFloat(formData.get("valorMeta"));
  const dataInicio = formData.get("dataInicio");
  const dataFinal = formData.get("dataFinal");

  alert(`Meta adicionada:
  Nome: ${nome}
  Tipo: ${tipo}
  Valor: R$ ${valor.toFixed(2)}
  Data Início: ${dataInicio}
  Data Final: ${dataFinal}`);

  fecharModalMeta();
  event.target.reset();
});

function fecharModalObjetivo() {
  document.getElementById("modalObjetivo")?.classList.remove("ativo");
}

document.getElementById("formObjetivo")?.addEventListener("submit", function (event) {
  event.preventDefault();
  const formData = new FormData(event.target);
  const titulo = formData.get("tituloObjetivo");
  const valorDesejado = parseFloat(formData.get("valorDesejado"));
  const valorGuardado = parseFloat(formData.get("valorGuardado"));
  const anoFinal = formData.get("anoFinal");

  alert(`Objetivo adicionado:\n
  Título: ${titulo}
  Valor desejado: R$ ${valorDesejado.toFixed(2)}
  Valor guardado: R$ ${valorGuardado.toFixed(2)}
  Ano final: ${anoFinal}`);

  fecharModalObjetivo();
  event.target.reset();
});

function navegarParaHash(forcadoHash) {
  if (location.hash === forcadoHash) {
    location.hash = "";
    setTimeout(() => location.hash = forcadoHash, 1);
  } else {
    location.hash = forcadoHash;
  }
}

document.getElementById("abrirModalTransacao")?.addEventListener("click", function (e) {
  e.preventDefault();
  navegarParaHash("#transacao");
});

document.getElementById("abrirModalMeta")?.addEventListener("click", function (e) {
  e.preventDefault();
  navegarParaHash("#meta");
});

document.getElementById("abrirModalObjetivo")?.addEventListener("click", function (e) {
  e.preventDefault();
  navegarParaHash("#objetivo");
});

function abrirModalViaHash() {
  const hash = window.location.hash;
  fecharTodosModais();

  if (hash === "#transacao") {
    document.getElementById("modalTransacao")?.classList.add("ativo");
  } else if (hash === "#meta") {
    document.getElementById("modalMeta")?.classList.add("ativo");
  } else if (hash === "#objetivo") {
    document.getElementById("modalObjetivo")?.classList.add("ativo");
  } else if (hash === "#editar") {
    document.getElementById("modalEditarTransacao")?.classList.add("ativo");
  }
}

function fecharTodosModais() {
  document.querySelectorAll(".modal").forEach(modal => modal.classList.remove("ativo"));
}

window.addEventListener("hashchange", abrirModalViaHash);
window.addEventListener("DOMContentLoaded", () => {
  abrirModalViaHash();
  atualizarTotais();
});

const tabela = document.getElementById("tabelaExtrato");
const saldoEl = document.getElementById("saldoTotal");

function atualizarTotais() {
  let ganhos = 0, gastos = 0;
  document.querySelectorAll("#tabelaExtrato tr").forEach(row => {
    const valorTD = row.querySelector("td:nth-child(5)");
    if (valorTD) {
      const texto = valorTD.textContent.replace(/[^\d,-]/g, "").replace(",", ".");
      const valor = parseFloat(texto);
      if (valorTD.classList.contains("valor-entrada")) ganhos += valor;
      else if (valorTD.classList.contains("valor-saida")) gastos += valor;
    }
  });
  const saldo = ganhos - gastos;
  if (saldoEl) saldoEl.textContent = `R$ ${saldo.toFixed(2)}`;
}

function fecharModalEditar() {
  document.getElementById("modalEditarTransacao")?.classList.remove("ativo");
}
