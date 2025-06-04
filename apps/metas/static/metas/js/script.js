document.getElementById('logout').addEventListener('click', function(e) {
      e.preventDefault();
      if(confirm('Tem certeza que deseja sair?')) {
        window.location.href = '{% url "usuario:logout" %}';
      }
    });

	 function editarMeta(id) {
    // Se quiser, use o id para carregar dados via AJAX futuramente
    location.hash = '#editarMeta';
  }

  function abrirModalViaHash() {
    fecharTodosModais();
    const hash = window.location.hash;
    if (hash === '#editarMeta') {
      document.getElementById('modalEditarMeta')?.classList.add('ativo');
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

  document.getElementById("formEditarMeta")?.addEventListener("submit", function(e) {
    e.preventDefault();
    const dados = new FormData(this);
    alert(`Meta atualizada:\nCategoria: ${dados.get("categoria")}\nTipo: ${dados.get("tipo")}\nValor: R$ ${parseFloat(dados.get("valor")).toFixed(2)}\nData: ${dados.get("data_inicio")} a ${dados.get("data_fim")}\nDescrição: ${dados.get("descricao")}`);
    fecharModalHash();
    this.reset();
  });