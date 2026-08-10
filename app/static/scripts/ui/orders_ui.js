// Importamos la función modal desde tu archivo de alertas
import { mostrarModalDetalle } from './alert_ui.js';

export function renderPedidos(pedidos) {
    const container = document.getElementById('pedidos-container');

    if (!container) return;

    container.innerHTML = '';

    // Manejo de errores de conexión o HTTP
    if (pedidos?.error === 'network') {
        container.innerHTML = `<div class="error" style="display:block;">Error de conexión con el servidor.</div>`;
        return;
    }

    if (pedidos?.error === 'http') {
        container.innerHTML = `<div class="error" style="display:block;">Error del servidor (${pedidos.status}).</div>`;
        return;
    }

    if (pedidos?.error === 'negocio') {
        container.innerHTML = `<div class="error" style="display:block;">${pedidos.mensaje}</div>`;
        return;
    }

    // Estado cuando el cliente SÍ está autenticado pero NO tiene pedidos
    if (!Array.isArray(pedidos) || pedidos.length === 0) {
        container.innerHTML = `
            <div style="text-align: center; padding: 40px 10px; color: #777;">
                <i class="fa-solid fa-box-open" style="font-size: 48px; margin-bottom: 15px; color: #ccc;"></i>
                <h3 style="font-size: 18px; margin-bottom: 5px; color: #333;">No tienes pedidos registrados</h3>
                <p style="font-size: 14px;">Actualmente no hay compras asociadas a tu número de identificación.</p>
            </div>
        `;
        return;
    }

    // Renderizado de la tabla cuando SÍ existen pedidos
    const table = document.createElement('table');
    table.classList.add('orders-table');

    table.innerHTML = `
        <thead>
            <tr>
                <th>N° Pedido</th>
                <th>Fecha</th>
                <th>Estado</th>
                <th>Total</th>
                <th>Acción</th>
            </tr>
        </thead>
        <tbody></tbody>
    `;

    const tbody = table.querySelector('tbody');

    pedidos.forEach(pedido => {
        const row = document.createElement('tr');
        const estadoClase = pedido.estado ? pedido.estado.toLowerCase().trim() : 'default';

        // Agregamos la clase .btn-ver-detalle al botón
        row.innerHTML = `
            <td><strong>#${pedido.numero_pedido}</strong></td>
            <td>${pedido.fecha_pedido || 'N/A'}</td>
            <td>
                <span class="order-status status-${estadoClase}">
                    ${pedido.estado}
                </span>
            </td>
            <td>$${pedido.total}</td>
            <td>
                <button class="btn-action btn-ver-detalle" data-id="${pedido.numero_pedido}">
                    <i class="fa-solid fa-eye"></i> Ver
                </button>
            </td>
        `;

        tbody.appendChild(row);
    });

    container.appendChild(table);

    // ACTIVACIÓN: Llamamos a la función para activar el clic de los botones recién creados
    activarBotonesVer(pedidos);
}

// Escuchar los clics en los botones "Ver" de la tabla
function activarBotonesVer(pedidos) {
    const botones = document.querySelectorAll('.btn-ver-detalle');

    botones.forEach(btn => {
        btn.addEventListener('click', (e) => {
            // Obtenemos el identificador del pedido desde el data-id
            const idPedido = e.currentTarget.dataset.id;
            
            // Buscamos el pedido en el arreglo comparando numero_pedido o id
            const pedidoEncontrado = pedidos.find(p => (p.numero_pedido || p.id) == idPedido);

            if (pedidoEncontrado) {
                mostrarModalDetalle(pedidoEncontrado);
            }
        });
    });
}