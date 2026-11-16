const MENSAGEM_NO_AR = "Serviço no ar";
const MENSAGEM_INDISPONIVEL =
  "Serviço indisponível no momento. Tente novamente em instantes.";

async function mostrarEstadoDoServico() {
  const elemento = document.getElementById("estado-do-servico");
  try {
    const resposta = await fetch("/saude");
    elemento.textContent = resposta.ok ? MENSAGEM_NO_AR : MENSAGEM_INDISPONIVEL;
  } catch (erro) {
    elemento.textContent = MENSAGEM_INDISPONIVEL;
  }
}

mostrarEstadoDoServico();
