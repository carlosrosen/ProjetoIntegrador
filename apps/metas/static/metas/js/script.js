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

  function fecharModalHash() {
    location.hash = '';
  }

  window.addEventListener('DOMContentLoaded', abrirModalViaHash);
  window.addEventListener('hashchange', abrirModalViaHash);




function abrirModalConfirmacao(metaId) {
  console.log("Abrindo modal de confirmação para meta:", metaId) // Debug

  const modal = document.getElementById("modalConfirmacao")

  if (modal) {
    // Fecha outros modais primeiro
    fecharTodosModais()

    // Abre o modal de confirmação
    modal.classList.add("ativo")
  } else {
    console.error("Modal não encontrado")
  }
}

function fecharModalConfirmacao() {
  const modal = document.getElementById("modalConfirmacao")
  if (modal) {
    modal.classList.remove("ativo")
  }
}

// Event listener para fechar modal ao clicar fora dele
document.addEventListener("DOMContentLoaded", () => {
  const modalConfirmacao = document.getElementById("modalConfirmacao")
  if (modalConfirmacao) {
    modalConfirmacao.addEventListener("click", function (e) {
      if (e.target === this) {
        fecharModalConfirmacao()
      }
    })
  }
})

function fecharTodosModais() {
  const modals = document.querySelectorAll(".modal.ativo")
  modals.forEach((modal) => {
    modal.classList.remove("ativo")
  })
}
