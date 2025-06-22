const tabela = document.getElementById("tabelaExtrato");
const saldoEl = document.getElementById("saldoTotal");

function atualizarTotais() {
  let ganhos = 0, gastos = 0;
  document.querySelectorAll("#tabelaExtrato tr").forEach(row => {
    const valorTD = row.querySelector("td:nth-child(5)");
    if (valorTD) {
      const texto = valorTD.textContent.replace(/[^\d,-]/g, "").replace(",", ".");
      const valor = parseFloat(texto);
      if (valorTD.classList.contains("valor-entrada")) ganhos += valor;
      else if (valorTD.classList.contains("valor-saida")) gastos += valor;
    }
  });
  const saldo = ganhos - gastos;
  if (saldoEl) saldoEl.textContent = `R$ ${saldo.toFixed(2)}`;
}

function fecharModalEditar() {
  document.getElementById("modalEditarTransacao")?.classList.remove("ativo");
}
