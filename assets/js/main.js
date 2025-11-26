const menuButton = document.querySelector('.menu-button');
const closeButton = document.querySelector('.sidebar .close-button');
const sidebar = document.querySelector('.sidebar');
const overlay = document.querySelector('.overlay');

menuButton.addEventListener('click', () => {
    sidebar.classList.add('open');
    overlay.classList.add('active');
});

closeButton.addEventListener('click', () => {
    sidebar.classList.remove('open');
    overlay.classList.remove('active');
});

overlay.addEventListener('click', () => {
    sidebar.classList.remove('open');
    overlay.classList.remove('active');
});
