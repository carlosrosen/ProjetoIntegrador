// Espera o carregamento do DOM
window.addEventListener('DOMContentLoaded', () => {
    const mensagem = document.getElementById('mensagem');
  
    // Adiciona a classe de animação depois de um pequeno tempo, se quiser
    setTimeout(() => {
      mensagem.style.display = "none";
    }, 5000); // tempo em milissegundos antes de iniciar a animação
  });