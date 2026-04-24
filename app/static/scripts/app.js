
import { initAuth } from './modules/auth_modules.js';
import { initPedidos } from './modules/orders_modules.js';

document.addEventListener('DOMContentLoaded', () => {
    
    const rutaActual = window.location.pathname;

    if (rutaActual ==='/pedidos') {

        initPedidos(); // pagina de pedidos
    }

    if (rutaActual === '/') {
        
        initAuth(); // login + OTP
    }
})
