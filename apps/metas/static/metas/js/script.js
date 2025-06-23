// ======================= Sistema de Hash Unificado =======================

const hashModalMap = {
    "#transacao": "modalTransacao",
    "#meta": "modalMeta",
    "#objetivo": "modalObjetivo",
    "#editarMeta": "modalEditarMeta",
    "#confirmacao": "modalConfirmacao"
};

function abrirModalViaHash() {
    fecharTodosModais();
    const modalId = hashModalMap[window.location.hash];
    if (modalId) {
        const modal = document.getElementById(modalId);
        if (modal) {
            modal.classList.add("ativo");
        }
    }
}

function fecharTodosModais() {
    document.querySelectorAll(".modal").forEach(modal => modal.classList.remove("ativo"));
}

function navegarParaHash(hash) {
    if (location.hash === hash) {
        location.hash = "";
        setTimeout(() => location.hash = hash, 1);
    } else {
        location.hash = hash;
    }
}

function cancelarNavegacaoHash() {
    history.pushState("", document.title, window.location.pathname + window.location.search);
    fecharTodosModais();
    location.reload();
}

// ======================= Listeners Manuais =======================

document.addEventListener("DOMContentLoaded", () => {
    document.getElementById("abrirModalTransacao").addEventListener("click", e => {
        e.preventDefault();
        navegarParaHash("#transacao");
    });

    document.getElementById("abrirModalMeta").addEventListener("click", e => {
        e.preventDefault();
        navegarParaHash("#meta");
    });

    document.getElementById("abrirModalObjetivo").addEventListener("click", e => {
        e.preventDefault();
        navegarParaHash("#objetivo");
    });
});

// ======================= Eventos Globais =======================

window.addEventListener("hashchange", abrirModalViaHash);
window.addEventListener("DOMContentLoaded", abrirModalViaHash);


// ======================= Tabs de Transação =======================

document.addEventListener("DOMContentLoaded", () => {
    const tabs = document.querySelectorAll(".tab");
    const camposDespesa = document.getElementById("camposDespesa");
    const camposReceita = document.getElementById("camposReceita");

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

    // Controle de parcelas
    const condicaoPagamento = document.getElementById("condicaoPagamento");
    const campoParcelas = document.getElementById("campoParcelas");

    condicaoPagamento.addEventListener("change", () => {
        campoParcelas.style.display = (condicaoPagamento.value === "parcelado") ? "block" : "none";
    });
});

// ======================= Formulários de Transação =======================

document.addEventListener("DOMContentLoaded", () => {
    document.getElementById("formTransacaoReceita").addEventListener("submit", e => {
        const formData = new FormData(e.target);
        const valor = formData.get("valor_receita");
        const data = formData.get("data_receita");
        const descricao = formData.get("descricao_receita");
        let pago = formData.get("pagamentoRE_receita");

        if (!valor || !data || !pago) {
            e.preventDefault();
            alert("Preencha os campos corretamente.");
            return;
        }

        if (parseFloat(valor) > 999999999) {
            e.preventDefault();
            alert("Valor muito grande.");
            return;
        }

        pago = pago === "true" ? "Sim" : "Não";

        alert(`Transação de receita adicionada:\n
Valor: 1x R$${valor}
Data: ${data}
Está pago?: ${pago}
Descrição: ${descricao}`);

        cancelarNavegacaoHash();
    });

    document.getElementById("formTransacaoDespesa").addEventListener("submit", e => {
        const formData = new FormData(e.target);
        const valor = parseFloat(formData.get("valor_despesa"));
        const data = formData.get("data_despesa");
        const descricao = formData.get("descricao_despesa");
        let pago = formData.get("pagamentoRE_despesa");
        const parcelas = parseInt(formData.get("parcelas_despesa"));

        if (!valor || !data || !pago || !parcelas) {
            e.preventDefault();
            alert("Preencha os campos corretamente.");
            return;
        }

        if (valor > 999999999) {
            e.preventDefault();
            alert("Valor muito grande.");
            return;
        }

        pago = pago === "true" ? "Sim" : "Não";

        alert(`Transação de despesa adicionada:\n
Valor: ${parcelas}x R$${(valor / parcelas).toFixed(2)}
Data: ${data}
Está pago?: ${pago}
Descrição: ${descricao}`);

        cancelarNavegacaoHash();
    });
});

// ======================= Formulário de Meta =======================

document.addEventListener("DOMContentLoaded", () => {
    document.getElementById("formMeta").addEventListener("submit", e => {
        const formData = new FormData(e.target);
        const tipo = formData.get("tipoMeta");
        const valor = parseFloat(formData.get("valorMeta"));
        const dataInicio = formData.get("dataInicio");
        const dataFinal = formData.get("dataFinal");
        const categoria = formData.get("categoria");

        if (!tipo || !valor || !dataInicio || !dataFinal || !categoria) {
            e.preventDefault();
            alert("Insira as informações corretamente!");
            return;
        }

        alert(`Meta adicionada:\n
Tipo: ${tipo}
Valor: R$${valor.toFixed(2)}
Data Início: ${dataInicio}
Data Final: ${dataFinal}
Categoria: ${categoria}`);

        cancelarNavegacaoHash();
    });
});

// ======================= Formulário de Objetivo =======================

document.addEventListener("DOMContentLoaded", () => {
    document.getElementById("formObjetivo").addEventListener("submit", e => {
        const formData = new FormData(e.target);
        const titulo = formData.get("tituloObjetivo");
        const valorDesejado = parseFloat(formData.get("valorDesejado"));
        const valorGuardado = parseFloat(formData.get("valorGuardado"));
        const anoFinal = formData.get("anoFinal");

        if (!titulo || !valorDesejado || !valorGuardado || !anoFinal) {
            e.preventDefault();
            alert("Insira as informações corretamente!");
            fecharModalObjetivo();
            return;
        }

        alert(`Objetivo adicionado:\n
Título: ${titulo}
Valor desejado: R$${valorDesejado.toFixed(2)}
Valor guardado: R$${valorGuardado.toFixed(2)}
Ano final: ${anoFinal}`);

        fecharModalObjetivo();
    });
});

// ======================= Edição e Exclusão de Meta =======================

document.addEventListener('DOMContentLoaded', () => {
    const modalEditar = document.getElementById('modalEditarMeta');
    const formEditar = document.getElementById('formEditarMeta');
    const modalConfirmacao = document.getElementById('modalConfirmacao');
    const formDeletar = document.getElementById('formDeletarMeta');

    const editButtons = document.querySelectorAll('.btn-editar-meta');

    editButtons.forEach(button => {
        button.addEventListener('click', () => {
            const { id, categoria, tipo, valor, inicio, fim, descricao } = button.dataset;

            formEditar.action = `editar-meta/${id}/`;
            formEditar.querySelector('[name="categoria"]').value = categoria;
            formEditar.querySelector('[name="tipoMeta"]').value = tipo;
            formEditar.querySelector('[name="valor"]').value = valor;
            formEditar.querySelector('[name="data_inicio"]').value = inicio;
            formEditar.querySelector('[name="data_fim"]').value = fim;
            formEditar.querySelector('[name="descricao"]').value = descricao;

            formDeletar.action = `deletar-meta/${id}/`;

            modalEditar.classList.add('ativo');
        });
    });

    [modalEditar, modalConfirmacao].forEach(modal => {
        if (modal) {
            modal.addEventListener('click', e => {
                if (e.target === modal) {
                    modal.classList.remove('ativo');
                }
            });
        }
    });
});

// ======================= Funções Globais de Fechamento =======================

function fecharModalTransacao() {
    document.getElementById("modalTransacao").classList.remove("ativo");
    cancelarNavegacaoHash();
}

function fecharModalMeta() {
    document.getElementById("modalMeta").classList.remove("ativo");
    cancelarNavegacaoHash();
}

function fecharModalObjetivo() {
    document.getElementById("modalObjetivo").classList.remove("ativo");
    cancelarNavegacaoHash();
}

window.abrirModalConfirmacao = function() {
    const modal = document.getElementById('modalConfirmacao');
    if (modal) modal.classList.add('ativo');
};

window.fecharModalEditar = function() {
    const modal = document.getElementById('modalEditarMeta');
    if (modal) modal.classList.remove('ativo');
};

window.fecharModalConfirmacao = function() {
    const modal = document.getElementById('modalConfirmacao');
    if (modal) modal.classList.remove('ativo');
};
