let verMais = document.getElementById("ver-mais");
let mostrarMais = document.getElementById("mostrar-todos");

const mostrarMaisAlunos = () => {
    verMais.style.display = 'inline';
    
};

mostrarMais.addEventListener('click', mostrarMaisAlunos);