// Espera o conteúdo da página carregar completamente
document.addEventListener('DOMContentLoaded', function() {
    const modalEditar = document.getElementById('modalEditarMeta');
    const formEditar = document.getElementById('formEditarMeta');
    const modalConfirmacao = document.getElementById('modalConfirmacao');
    const formDeletar = document.getElementById('formDeletarMeta');

    const editButtons = document.querySelectorAll('.btn-editar-meta');

    editButtons.forEach(button => {
        button.addEventListener('click', function() {
            const id = this.dataset.id;
            const categoria = this.dataset.categoria;
            const tipo = this.dataset.tipo;
            const valor = this.dataset.valor;
            const inicio = this.dataset.inicio;
            const fim = this.dataset.fim;
            const descricao = this.dataset.descricao;

            const urlEditar = `editar-meta/${id}/`;
            const urlDeletar = `deletar-meta/${id}/`;

            formEditar.action = urlEditar;
            formEditar.querySelector('[name="categoria"]').value = categoria;
            formEditar.querySelector('[name="tipoMeta"]').value = tipo;
            formEditar.querySelector('[name="valor"]').value = valor;
            formEditar.querySelector('[name="data_inicio"]').value = inicio;
            formEditar.querySelector('[name="data_fim"]').value = fim;
            formEditar.querySelector('[name="descricao"]').value = descricao;

            formDeletar.action = urlDeletar;

            modalEditar.classList.add('ativo');
        });
    });

    window.abrirModalConfirmacao = function() {
        if (modalConfirmacao) {
            modalConfirmacao.classList.add('ativo');
        }
    }

    window.fecharModalEditar = function() {
        if (modalEditar) {
            modalEditar.classList.remove('ativo');
        }
    }

    window.fecharModalConfirmacao = function() {
        if (modalConfirmacao) {
            modalConfirmacao.classList.remove('ativo');
        }
    }

    [modalEditar, modalConfirmacao].forEach(modal => {
        if (modal) {
            modal.addEventListener('click', function(event) {
                if (event.target === modal) {
                    modal.classList.remove('ativo');
                }
            });
        }
    });
});