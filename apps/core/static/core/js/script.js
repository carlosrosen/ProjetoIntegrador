let modoGrafico = "gastos";
const ctx = document.getElementById("graficoGastos").getContext("2d");

let div = document.getElementById("grafico_despesa");

if (!div) {
  console.warn("#grafico_despesa não encontrado.");
}

const categorias_gasto = div.dataset.listaCategorias.split(',');
const valores_gasto = div.dataset.listaValores.split(',');

const cores_gastos = {
    "Alimentação": "#f39c12"
  , "Transporte": "#1abc9c"
  , "Educação": "#3498db"
  , "Moradia": "#9b59b6"
  , "Despesas pessoais": "#e74c3c"
  , "Saúde": "#2ecc71"
  , "Tarifas": "#34495e"
  , "Outras despesas": "#95a5a6"
};

let lista_cores_gastos = [];
let nome_categorias_gastos = [];

for(let i= 0; i < categorias_gasto.length; i++){
  let nome = categorias_gasto[i]
  lista_cores_gastos.push(cores_gastos[nome]);
  nome_categorias_gastos.push(nome);
}

let dadosGastos = {
  labels: nome_categorias_gastos,
  datasets: [{
    label: "Gastos por Categoria",
    data: valores_gasto,
    backgroundColor: lista_cores_gastos
  }]
};

div = document.getElementById("grafico_receita")

const categorias_ganhos = div.dataset.listaCategorias.split(',');
const valores_ganhos = div.dataset.listaValores.split(',');

const cores_ganhos = {
    "Salário": "#1f77b4"
  , "Aposentadoria": "#ff7f0e"
  , "Bolsa de estudos": "#2ca02c"
  , "Aluguel recebido": "#d62728"
  , "Rendimentos de investimentos": "#9467bd"
  , "Freelance": "#8c564b"
  , "Venda de produtos": "#e377c2"
  , "Comissão": "#7f7f7f"
  , "Prêmios": "#bcbd22"
  , "Presente": "#17becf"
  , "Doação": "#aec7e8"
  , "Herança": "#ffbb78"
  , "Outras Receita": "#95a5a6"
};


let lista_cores_ganhos = [];
let nome_categorias_ganhos = [];

for (let i = 0; i < categorias_ganhos.length; i++){
  let nome = categorias_ganhos[i];
  lista_cores_ganhos.push(cores_ganhos[nome]);
  nome_categorias_ganhos.push(nome);
}


const dadosGanhos = {
  labels: nome_categorias_ganhos,
  datasets: [{
    label: "Ganhos por Categoria",
    data: valores_ganhos,
    backgroundColor: lista_cores_ganhos
  }]
};

let meuGrafico = new Chart(ctx, {
   type: "doughnut",
   data: dadosGastos,
   options: {
     responsive: true,
     plugins: {
       legend: {position: 'bottom'}
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
    cancelarNavegacaoHash()
}

// Lista de transações
let transacao = [];

document.getElementById("formTransacaoReceita").addEventListener("submit", function(event) {
  const formData = new FormData(event.target);

  let valor = formData.get("valor_receita");
  let data = formData.get("data_receita");;
  let descricao = formData.get("descricao_receita");
  let pago = formData.get("pagamentoRE_receita");


  if (valor == null || data == null || pago == null){
    alert("Preencha os campos corretamente.");
    event.preventDefault();
 // Cancela a URL hash
  }
  cancelarNavegacaoHash();
});

document.getElementById("formTransacaoDespesa").addEventListener("submit",function (event){

  const formData = new FormData(event.target)

  const valor = formData.get("valor_despesa");
  const data = formData.get("data_despesa");
  const  descricao = formData.get("descricao_despesa");
  const  pago = formData.get("pagamentoRE_despesa");
  const  parcelas = formData.get("parcelas_despesa")

  if (valor == null || data == null || pago == null || parcelas == null){
    alert("Preencha os campos corretamente.");
    event.preventDefault();
  }
  cancelarNavegacaoHash();
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
    campoParcelas.style.display = (condicaoPagamento.value === "parcelado") ? "block" : "none";
  });

  btnAbrir.addEventListener("click", () => {
    modal.classList.add("ativo");
  });
});




// Fechar modal
function fecharModalMeta() {
  document.getElementById("modalMeta").classList.remove("ativo");
}

// Mostrar/ocultar campo de data baseado na opção de exclusão


// Capturar dados do formulário de meta
document.getElementById("formMeta").addEventListener("submit", function (event) {
  event.preventDefault();
  const formData = new FormData(event.target);
  const nome = formData.get("nomeMeta");
  const tipo = formData.get("tipoMeta");
  const valor = formData.get("valorMeta");
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

//ADICIONADO A PARTIR DAQUI DIA 16/06/2025

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

//---------------------------------------------------------------------------------

function cancelarNavegacaoHash() {
  history.pushState("", document.title, window.location.pathname + window.location.search);
  fecharTodosModais();
  location.reload()
}

function navegarParaHash(forcadoHash) {
  if (location.hash === forcadoHash) {
    // Força o hashchange manualmente se o hash já for igual
    location.hash = "";
    // Pequeno delay para garantir o reset e acionar o hashchange
    setTimeout(() => location.hash = forcadoHash, 1);
  } else {
    location.hash = forcadoHash;
  }
}

document.getElementById("abrirModalTransacao").addEventListener("click", function (e) {
  e.preventDefault();
  navegarParaHash("#transacao");
});

document.getElementById("abrirModalMeta").addEventListener("click", function (e) {
  e.preventDefault();
  navegarParaHash("#meta");
});

document.getElementById("abrirModalObjetivo").addEventListener("click", function (e) {
  e.preventDefault();
  navegarParaHash("#objetivo");
});



function abrirModalViaHash() {
  const hash = window.location.hash;

  fecharTodosModais();

  if (hash === "#transacao") {
    document.getElementById("modalTransacao").classList.add("ativo");
  } else if (hash === "#meta") {
    document.getElementById("modalMeta").classList.add("ativo");
  } else if (hash === "#objetivo") {
    document.getElementById("modalObjetivo").classList.add("ativo");
  }
}

function fecharTodosModais() {
  document.querySelectorAll(".modal").forEach(modal => modal.classList.remove("ativo"));
}

// Dispara quando hash muda (botão voltar, link direto etc.)
window.addEventListener("hashchange", abrirModalViaHash);

// Dispara ao carregar a página
window.addEventListener("DOMContentLoaded", abrirModalViaHash);

window.addEventListener("hashchange", abrirModalViaHash);
window.addEventListener("DOMContentLoaded", () => {
  abrirModalViaHash();
});

function fecharModalEditar() {
  document.getElementById("modalEditarTransacao")?.classList.remove("ativo");
}