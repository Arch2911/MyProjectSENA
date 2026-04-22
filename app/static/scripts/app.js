
import { initAuth } from './modules/auth_modules.js';
import { initPedidos } from './modules/orders_modules.js';

document.addEventListener('DOMContentLoaded', () => {

    initAuth();     // login + OTP
    initPedidos();  // pedidos
});

