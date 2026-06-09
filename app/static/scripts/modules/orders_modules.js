

import { obtenerPedidos } from '../api/orders_api.js';
import { renderPedidos } from '../ui/orders_ui.js';

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
}