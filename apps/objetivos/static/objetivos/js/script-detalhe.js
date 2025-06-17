function abrirModalViaHash() {
  fecharTodosModais();
  const hash = window.location.hash;
  console.log(hash);
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