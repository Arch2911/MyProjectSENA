

import { obtenerPedidos } from '../api/orders_api.js';
import { renderPedidos } from '../ui/orders_ui.js';

export async function initPedidos() {

    const data = await obtenerPedidos();

    if (!data) {
        renderPedidos(null);
        return;
    }

    if (data.status !== 'success') {
        renderPedidos([]);
        return;
    }

    renderPedidos(data.data);
}