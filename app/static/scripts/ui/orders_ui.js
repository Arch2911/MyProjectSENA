
export function renderPedidos(pedidos) {

    const container = document.getElementById('pedidos-container');

    if (!container) return;

    container.innerHTML = '';

    if (pedidos === null) {
        container.textContent = 'Error al cargar pedidos';
        return;
    }

    if (pedidos.length === 0) {
        container.textContent = 'No hay pedidos';
        return;
    }

    pedidos.forEach(pedido => {

        const card = document.createElement('div');
        card.classList.add('pedido-card');

        const title = document.createElement('h3');
        title.textContent = `Pedido #${pedido.numero_pedido}`;

        const estado = document.createElement('p');
        estado.textContent = `Estado: ${pedido.estado}`;

        const total = document.createElement('p');
        total.textContent = `Total: $${pedido.total}`;

        card.appendChild(title);
        card.appendChild(estado);
        card.appendChild(total);

        container.appendChild(card);
    });
}