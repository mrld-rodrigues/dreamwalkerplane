/* PEgar o ano corrente */

const currentYear = new Date().getFullYear();
document.getElementById("current-year").textContent = currentYear;



/* Função para abrir e fechar o aside */

const menuMobile = document.querySelector('.menu-mobile');
const body = document.querySelector('body');

menuMobile.addEventListener('click', () => {
    menuMobile.classList.contains("bi-list")    
        ? menuMobile.classList.replace("bi-list", "bi-x")
        : menuMobile.classList.replace("bi-x", "bi-list");

    body.classList.toggle("menu-responsive-active")
        
}); 


/* Animação de todos os itens com o atributo data-anime */

const item = document.querySelectorAll("[data-anime]");

const animeScroll = () => {
    const windowTop = window.scrollY + window.innerHeight * 1.85;
    // console.log(windowTop)
    item.forEach((element) => {
        if (windowTop > element.offsetTop) {
            element.classList.add("animate");
        } else {
            element.classList.remove("animate");
        }
    });
}
animeScroll()

window.addEventListener("scroll", ()=>{
    animeScroll();
})


/* Ativar o carregamento do botão enviar */

const form = document.querySelector('.custom-form');
const btnEnviar = document.querySelector('#btn-send')
const btnEnviarLoader = document.querySelector('#btn-send-loader')

form.addEventListener("submit", (event) => {
    btnEnviarLoader.style.display = "block";
    btnEnviar.style.display = "none";
})



