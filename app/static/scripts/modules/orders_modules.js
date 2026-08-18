

import { obtenerPedidos } from '../api/orders_api.js';
import { renderPedidos } from '../ui/orders_ui.js';
import { cerrarSesion } from '../api/auth_api.js';

export async function initPedidos() {

    const response = await obtenerPedidos();
    const data = response.data;

    if (response.status === 0) {
        renderPedidos({ error: 'network' });
        return;
    }

    if (!response.ok){
        renderPedidos({
            error: 'http',
            status: response.status
        });

        return;
    }

    if (data.status !== 'success') {
        renderPedidos({
            error: 'negocio',
            mensaje: response.data.error
        });
        return;
    }

    renderPedidos(data.data);

    // Módulo de Logout

    const btnLogout = document.getElementById('btn-logout');

    if (btnLogout) {
        btnLogout.addEventListener('click', async (e) => {
            //Detiene el comportamiento de enlace <a> al redireccionar automáticamente a la pagina princial
            e.preventDefault();

            // Se ejecuta la eliminación de sessión
            const response = await cerrarSesion()

            // Al cerrar se sessión se redirige
            if (!response.ok){
                console.error(`Error HTTP: ${response.status}`)
                return;
            }
        window.location.href = '/';
        })
    }

}
