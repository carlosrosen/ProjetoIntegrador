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



let tipoGraficoLinha = "saldo";
let graficoLinha;

function alternarGrafico() {
  tipoGraficoLinha = tipoGraficoLinha === "saldo" ? "fluxo" : "saldo";

  const novoDataset = tipoGraficoLinha === "saldo"
    ? {
        label: "Saldo",
        data: [1000, 1200, 1100, 1600, 1800, 2200, 2450],
        borderColor: "#2ecc71",
        backgroundColor: "rgba(46, 204, 113, 0.1)"
      }
    : {
        label: "Fluxo de Caixa",
        data: [200, -100, 500, 200, 400, 250],
        borderColor: "#3498db",
        backgroundColor: "rgba(52, 152, 219, 0.1)"
      };

  graficoLinha.data.datasets[0] = novoDataset;
  graficoLinha.update();

   const botao = document.querySelector(".grafico-switch button");
  botao.innerText = tipoGraficoLinha === "saldo" ? "Alternar para fluxo de caixa" : "Alternar para saldo";
}

let tipoPizza = "gastos";
let graficoPizza;

function alternarCategoria() {
  tipoPizza = tipoPizza === "gastos" ? "receitas" : "gastos";

  const novoData = tipoPizza === "gastos"
    ? {
        labels: ["Alimentação", "Transporte", "Lazer", "Educação", "Outros"],
        datasets: [{
          data: [22, 18, 15, 5, 40],
          backgroundColor: ["#e74c3c", "#f1c40f", "#9b59b6", "#3498db", "#95a5a6"]
        }]
      }
    : {
        labels: ["Salário", "Freelance", "Aluguel", "Investimentos", "Outros"],
        datasets: [{
          data: [45, 20, 10, 15, 10],
          backgroundColor: ["#2ecc71", "#1abc9c", "#f39c12", "#8e44ad", "#bdc3c7"]
        }]
      };

  graficoPizza.data = novoData;
  graficoPizza.update();

  const botao = document.querySelector(".grafico-categorias button");
  botao.innerText = tipoPizza === "gastos" ? "Alternar para categorias de receita" : "Alternar para categorias de despesa";
}

// Exemplo de gráficos com Chart.js (dados fictícios)
document.addEventListener("DOMContentLoaded", () => {
graficoLinha = new Chart(document.getElementById("graficoLinha"), {
type: "line",
data: {
	labels: ["01", "05", "10", "15", "20", "25", "30"],
	datasets: [{
	label: "Saldo",
	data: [1000, 1200, 1100, 1600, 1800, 2200, 2450],
	borderColor: "#2ecc71",
	backgroundColor: "rgba(46, 204, 113, 0.1)",
	fill: true,
	tension: 0.4
	}]
},
options: {
	responsive: true,
	maintainAspectRatio: false, // Adicionado para controlar o tamanho
	plugins: { legend: { display: false } }
}
});
const ctxBarras = document.getElementById("graficoBarras").getContext("2d");
graficoPizza = new Chart(document.getElementById("graficoPizza"), {
type: "pie",
data: {
	labels: ["Alimentação", "Transporte", "Lazer", "Educação", "Outros"],
	datasets: [{
	data: [22, 18, 15, 5, 40],
	backgroundColor: ["#e74c3c", "#f1c40f", "#9b59b6", "#3498db", "#95a5a6"]
	}]
},
options: {
	responsive: true,
	maintainAspectRatio: false, // Adicionado para controlar o tamanho
}
});


  graficoBarras = new Chart(ctxBarras, {
    type: "bar",
    data: {
      labels: ["Seg", "Ter", "Qua", "Qui", "Sex", "Sáb", "Dom"],
      datasets: [{
        label: "Gastos",
        data: [120, 200, 150, 300, 250, 180, 100],
        backgroundColor: "#e74c3c"
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false, // Adicionado para controlar o tamanho
      plugins: { legend: { display: false } }
    }
  });

  // 🎯 Adiciona o listener pro select
  const filtroPeriodo = document.getElementById("filtroPeriodo");
const filtroMes = document.getElementById("filtroMes");
const btnFiltrar = document.getElementById("btnFiltrar");

if (filtroPeriodo && filtroMes && btnFiltrar) {
  // Mostra ou esconde o select de mês
  filtroPeriodo.addEventListener("change", () => {
    if (filtroPeriodo.value === "anual") {
      filtroMes.style.display = "none";
    } else {
      filtroMes.style.display = "inline-block";
    }
  });

  btnFiltrar.addEventListener("click", () => {
    if (filtroPeriodo.value === "anual") {
      atualizarGraficoBarrasParaMeses();
    } else {
      atualizarGraficoBarrasParaDias();
    }
  });
}
});
function atualizarGraficoBarrasParaMeses() {
  graficoBarras.data.labels = ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun", "Jul", "Ago", "Set", "Out", "Nov", "Dez"];
  graficoBarras.data.datasets[0].data = [900, 1100, 1050, 980, 1200, 1300, 950, 1020, 990, 1120, 850, 970];
  graficoBarras.update();

  // Atualiza título
  const titulo = document.getElementById("tituloGraficoBarras");
  if (titulo) titulo.innerText = "Gastos por mês do ano";
}

function atualizarGraficoBarrasParaDias() {
  graficoBarras.data.labels = ["Seg", "Ter", "Qua", "Qui", "Sex", "Sáb", "Dom"];
  graficoBarras.data.datasets[0].data = [120, 200, 150, 300, 250, 180, 100];
  graficoBarras.update();

  // Atualiza título
  const titulo = document.getElementById("tituloGraficoBarras");
  if (titulo) titulo.innerText = "Gastos por dia da semana";
}