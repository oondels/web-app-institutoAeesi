let itemToshow = document.getElementsByClassName("itens-toShow")[0];
let buttonShow = document.getElementsByClassName("mostrar-itens")[0];

const mostrarMaisAlunos = () => {
    itemToshow.style.display = 'block';
    
};

buttonShow.addEventListener('click', mostrarMaisAlunos);