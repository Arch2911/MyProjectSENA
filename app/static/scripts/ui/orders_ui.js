
export function renderPedidos(pedidos) {
    const container = document.getElementById('pedidos-container');

    if (!container) return;

    container.innerHTML = '';

    // 1. Manejo de errores de conexión o HTTP
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

    // 2. Estado cuando el cliente SI está autenticado pero NO tiene pedidos
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

    // 3. Renderizado de la tabla cuando SÍ existen pedidos
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

        row.innerHTML = `
            <td><strong>#${pedido.numero_pedido}</strong></td>
            <td>${pedido.fecha || 'N/A'}</td>
            <td>
                <span class="order-status status-${estadoClase}">
                    ${pedido.estado}
                </span>
            </td>
            <td>$${pedido.total}</td>
            <td>
                <button class="btn-action" data-id="${pedido.numero_pedido}">
                    <i class="fa-solid fa-eye"></i> Ver
                </button>
            </td>
        `;

        tbody.appendChild(row);
    });

    container.appendChild(table);
}