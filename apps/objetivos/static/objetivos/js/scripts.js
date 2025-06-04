function abrirModalViaHash() {
    fecharTodosModais();
    const hash = window.location.hash;
    if (hash === '#deposito') {
      document.getElementById('modalDeposito')?.classList.add('ativo');
    } else if (hash === '#resgate') {
      document.getElementById('modalResgate')?.classList.add('ativo');
    } else if (hash === '#editar') {
      document.getElementById('modalEditar')?.classList.add('ativo');
    } else if (hash === '#apagar') {
      document.getElementById('modalApagar')?.classList.add('ativo');
    }
  }

  function fecharTodosModais() {
    document.querySelectorAll('.modal').forEach(modal => modal.classList.remove('ativo'));
  }

  function fecharModalHash() {
    location.hash = '';
  }

  window.addEventListener('DOMContentLoaded', abrirModalViaHash);
  window.addEventListener('hashchange', abrirModalViaHash);

  document.getElementById("formDeposito")?.addEventListener("submit", function(e) {
    e.preventDefault();
    const valor = parseFloat(new FormData(this).get("valorDeposito"));
    alert(`Dep sito de R$ ${valor.toFixed(2)} registrado!`);
    fecharModalHash();
    this.reset();
  });

  document.getElementById("formResgate")?.addEventListener("submit", function(e) {
    e.preventDefault();
    const valor = parseFloat(new FormData(this).get("valorResgate"));
    alert(`Resgate de R$ ${valor.toFixed(2)} registrado!`);
    fecharModalHash();
    this.reset();
  });

  document.getElementById("formEditar")?.addEventListener("submit", function(e) {
    e.preventDefault();
    const dados = new FormData(this);
    alert(`Objetivo atualizado para:\nT tulo: ${dados.get("novoTitulo")}\nValor: R$ ${parseFloat(dados.get("novoValor")).toFixed(2)}\nData final: ${dados.get("novaData")}`);
    fecharModalHash();
    this.reset();
  });

  function confirmarApagarObjetivo() {
    alert("Objetivo apagado com sucesso.");
    fecharModalHash();
    // Aqui voc  pode redirecionar ou atualizar a p gina
  }