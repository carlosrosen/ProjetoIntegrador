function editarTransacao(id) {
    location.hash = '#editarTransacao';
  }

  function abrirModalViaHash() {
    fecharTodosModais();
    const hash = window.location.hash;
    if (hash === '#editarTransacao') {
      document.getElementById('modalEditarTransacao')?.classList.add('ativo');
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

  document.getElementById("formEditarTransacao")?.addEventListener("submit", function(e) {
    e.preventDefault();
    const dados = new FormData(this);
    alert(`Transação atualizada:\nData: ${dados.get("data")}\nCategoria: ${dados.get("categoria")}\nDescrição: ${dados.get("descricao")}\nTipo: ${dados.get("tipo")}\nParcelas: ${dados.get("parcelas") || 'À vista'}\nValor: R$ ${parseFloat(dados.get("valor")).toFixed(2)}`);
    fecharModalHash();
    this.reset();
  });