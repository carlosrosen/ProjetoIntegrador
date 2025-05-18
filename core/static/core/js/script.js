let modoGrafico = "gastos";
const ctx = document.getElementById("graficoGastos").getContext("2d");

const dadosGastos = {
  labels: ["Alimentação", "Viagem", "Saúde", "Casa"],
  datasets: [{
    label: "Gastos por Categoria",
    data: [56.00, 10.00, 14.00, 20.00],
    backgroundColor: ["#f39c12", "#1abc9c","red","lightBlue"]
  }]
};

const dadosGanhos = {
  labels: ["Salário", "Freelancer"],
  datasets: [{
    label: "Ganhos por Categoria",
    data: [89.00, 11.00],
    backgroundColor: ["#2ecc71","blue"]
  }]
};

let meuGrafico = new Chart(ctx, {
  type: "doughnut",
  data: dadosGastos,
  options: {
    responsive: true,
    plugins: {
      legend: { position: 'bottom' }
    }
  }
});

function alternarGrafico() {
  if (modoGrafico === "gastos") {
    meuGrafico.data = dadosGanhos;
    document.getElementById("btnAlternar").innerText = "Ver Gastos";
    modoGrafico = "ganhos";
  } else {
    meuGrafico.data = dadosGastos;
    document.getElementById("btnAlternar").innerText = "Ver Ganhos";
    modoGrafico = "gastos";
  }
  meuGrafico.update();
}

// Modal - abrir e fechar
function fecharModal() {
  const modal = document.getElementById("modalTransacao");
  modal.classList.remove("ativo");
}

// Lista de transações
let transacoes = [];

document.getElementById("formTransacao").addEventListener("submit", function(event) {
  event.preventDefault();
  const formData = new FormData(event.target);
  const descricao = formData.get("descricao");
  const valor = parseFloat(formData.get("valor"));
  const tipo = formData.get("tipo");

  if (!descricao || isNaN(valor)) {
    alert("Preencha os campos corretamente.");
    return;
  }

  // Adiciona a transação com o tipo correto (entrada ou saída)
  transacoes.push({
    id: Date.now(),
    descricao,
    valor,
    tipo
  });

  alert(`Transação adicionada:\n${descricao} - R$ ${valor.toFixed(2)} (${tipo})`);

  atualizarSaldo(); // Atualizar saldo após adicionar
  fecharModal();
  event.target.reset();
});

function atualizarSaldo() {
  const totalReceitas = transacoes
    .filter(t => t.tipo === "entrada")
    .reduce((acc, t) => acc + t.valor, 0);

  const totalDespesas = transacoes
    .filter(t => t.tipo === "saida")
    .reduce((acc, t) => acc + t.valor, 0);

  const saldo = totalReceitas - totalDespesas;
  const campoSaldo = document.getElementById("saldoTotal");

  if (campoSaldo) {
    campoSaldo.textContent = `R$ ${saldo.toFixed(2)}`;
    campoSaldo.className = saldo >= 0 ? "verde" : "vermelho";
  }
}

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

      // Verifica qual aba foi clicada e exibe os campos corretos
      if (tipo === "saida") {
        camposDespesa.style.display = "block";
        camposReceita.style.display = "none";
      } else {
        camposDespesa.style.display = "none";
        camposReceita.style.display = "block";
      }
    });
  });

  condicaoPagamento.addEventListener("change", () => {
    campoParcelas.style.display = condicaoPagamento.value === "parcelado" ? "block" : "none";
  });

  btnAbrir.addEventListener("click", () => {
    modal.classList.add("ativo");
  });
});

// Abrir modal de meta
document.getElementById("abrirModalMeta").addEventListener("click", function (e) {
  e.preventDefault();
  document.getElementById("modalMeta").classList.add("ativo");
});

// Fechar modal
function fecharModalMeta() {
  document.getElementById("modalMeta").classList.remove("ativo");
}

// Mostrar/ocultar campo de data baseado na opção de exclusão
document.getElementById("exclusaoMeta").addEventListener("change", function () {
  const campoData = document.getElementById("campoDataMeta");
  campoData.style.display = this.value === "data" ? "block" : "none";
});

// Capturar dados do formulário de meta
document.getElementById("formMeta").addEventListener("submit", function (event) {
  event.preventDefault();
  const formData = new FormData(event.target);
  const nome = formData.get("nomeMeta");
  const tipo = formData.get("tipoMeta");
  const valor = parseFloat(formData.get("valorMeta"));
  const exclusao = formData.get("exclusaoMeta");
  const data = formData.get("dataMeta");

  alert(`Meta adicionada:
  Nome: ${nome}
  Tipo: ${tipo}
  Valor: R$ ${valor.toFixed(2)}
  Exclusão: ${exclusao}${exclusao === "data" ? ` até ${data}` : ""}`);

  fecharModalMeta();
  event.target.reset();
});
//ADICIONADO A PARTIR DAQUI DIA 16/06/2025
// Abrir modal de objetivo
document.querySelector("a[href='#']").addEventListener("click", function (e) {
  if (e.target.textContent.includes("Adicionar Objetivo")) {
    e.preventDefault();
    document.getElementById("modalObjetivo").classList.add("ativo");
  }
});

// Fechar modal de objetivo
function fecharModalObjetivo() {
  document.getElementById("modalObjetivo").classList.remove("ativo");
}

// Capturar dados do formulário de objetivo
document.getElementById("formObjetivo").addEventListener("submit", function (event) {
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

document.getElementById("abrirModalObjetivo").addEventListener("click", function (e) {
  e.preventDefault();
  document.getElementById("modalObjetivo").classList.add("ativo");
});

