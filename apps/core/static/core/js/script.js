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

  if (valor == null || data == null || pago == null) {
    event.preventDefault();
    alert("Preencha os campos corretamente.");
    // Cancela a URL hash
  }
  cancelarNavegacaoHash();
});

document.getElementById("formTransacaoDespesa").addEventListener("submit",function (event){
  const formData = new FormData(event.target);
  const valor = formData.get("valor_despesa");
  const data = formData.get("data_despesa");
  const  descricao = formData.get("descricao_despesa");
  const  pago = formData.get("pagamentoRE_despesa");
  const  parcelas = formData.get("parcelas_despesa")

  if (valor == null || data == null || pago == null || parcelas == null){
    event.preventDefault();
    alert("Preencha os campos corretamente.");
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
  cancelarNavegacaoHash();
}

// Mostrar/ocultar campo de data baseado na opção de exclusão


// Capturar dados do formulário de meta
document.getElementById("formMeta").addEventListener("submit", function (event) {
  event.preventDefault();
  const formData = new FormData(event.target);
  const tipo = formData.get("tipoMeta");
  const valor = parseFloat(formData.get("valorMeta"));
  const dataInicio = formData.get("dataInicio");
  const dataFinal = formData.get("dataFinal");
  const categoria = formData.get("categoria");

  console.log("Campo 'tipo':", tipo);
  console.log("Campo 'valor':", valor);
  console.log("Campo 'dataInicio':", dataInicio);
  console.log("Campo 'dataFinal':", dataFinal);
  console.log("Campo 'categoria':", categoria);

  if(!tipo || !valor || !dataInicio || !dataFinal || !categoria){
    alert("Insira as informações corretamente!")
    return;
  }

  alert(`Meta adicionada:\n
  Tipo: ${tipo}
  Valor: R$ ${valor.toFixed(2)}
  Data Início: ${dataInicio}
  Data Final: ${dataFinal}
  categoria: ${categoria}`);

  cancelarNavegacaoHash()
});

//ADICIONADO A PARTIR DAQUI DIA 16/06/2025

// Fechar modal de objetivo
function fecharModalObjetivo() {
  document.getElementById("modalObjetivo").classList.remove("ativo");
  cancelarNavegacaoHash();
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