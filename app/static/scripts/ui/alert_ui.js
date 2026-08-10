// función para mostrar alerta de errores y según el caso se redirige.

export function mostrarAlertaError({icon = 'question', title = 'Error', text, redirect = null}) {
    Swal.fire({
        icon,
        title,
        text
    })

    .then(() => {
        if (redirect) {
            window.location.href = redirect;
        }
    });
}

// Función para mostrar alerta de exito.

export function mostrarAlertaOk({icon = 'success', title = 'Exitoso', showConfirmButton = false, timer = 1500, redirect = null}) {
    Swal.fire({
        icon,
        title,
        showConfirmButton,
        timer
    })

    .then(() => {
        if (redirect) {
            window.location.href = redirect;
        }
    });
}

// Función para mostrar alerta al procesar el pedido que se mostrará al cliente.

export function mostrarAlertaTiempo({title = 'Procesando...', timer = 2000, redirect = null}) {

    let tiempoIntervalo;

    Swal.fire({
        title,
        html: 'Cargando pedidos <b></b> ms...',
        timer,
        timerPogressBar: true,

        didOpen: () => {

            Swal.showLoading();

            const b = swal.getPopup().querySelector('b');

            tiempoIntervalo = setInterval(() => {
                
                if (b) {

                    b.textContent = Swal.getTimerLeft();
                }
            }, 100)
        },

        willClose: () => {
            
            clearInterval(tiempoIntervalo);
        }
    })

    .then (() => {

        if (redirect) {

            window.location.href = redirect;
        }
    });
}

// Función para manejar error de sesión invalida

export function mostrarAlertaSesion() {
    mostrarAlertaError({
        icon: 'info',
        title: 'Sesión expirada',
        text: 'Tu sesión ha expirado. Inicia sesión nuevamente.'
    });

    setTimeout(() => {
        window.location.replace = ('/');
    }, 1500);
}

// Función que genera y muestra la ventana flotante alineada a tus datos
export function mostrarModalDetalle(pedido) {
    const numPedido = pedido.numero_pedido || pedido.id;

    // Recorremos el arreglo 'detalles' que ahora sí envía Python
    let filasProductos = '';
    
    if (pedido.detalles && pedido.detalles.length > 0) {
        filasProductos = pedido.detalles.map(det => `
            <tr>
                <td style="padding: 6px 0;">${det.nombre_producto}</td>
                <td style="text-align: center;">x${det.cantidad}</td>
                <td style="text-align: right;">$${det.precio_unitario}</td>
                <td style="text-align: right; font-weight: bold;">$${det.subtotal}</td>
            </tr>
        `).join('');
    } else {
        filasProductos = `<tr><td colspan="4" style="color: #888; text-align: center; padding: 10px;">Sin detalles registrados.</td></tr>`;
    }

    Swal.fire({
        title: `Pedido #${numPedido}`,
        html: `
            <div style="text-align: left; font-size: 13px; color: #333; line-height: 1.6;">
                <p style="margin-bottom: 5px;"><strong>Estado actual:</strong> 
                    <span style="color: #28a745; font-weight: bold;">${pedido.estado || 'PENDIENTE'}</span>
                </p>
                <p style="margin-bottom: 12px;"><strong>Fecha:</strong> ${pedido.fecha_pedido || 'N/A'}</p>
                
                <h4 style="font-size: 14px; border-bottom: 1px solid #eee; padding-bottom: 5px; margin-bottom: 10px; color: #801AF5;">
                    Productos del Pedido
                </h4>

                <table style="width: 100%; border-collapse: collapse; font-size: 13px; margin-bottom: 15px;">
                    <thead>
                        <tr style="border-bottom: 1px solid #ddd; text-align: left; color: #666;">
                            <th>Producto</th>
                            <th style="text-align: center;">Cantidad</th>
                            <th style="text-align: right;">Precio</th>
                            <th style="text-align: right;">Subtotal</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${filasProductos}
                    </tbody>
                </table>

                <div style="text-align: right; font-size: 15px; border-top: 1px solid #ddd; padding-top: 8px;">
                    <strong>Total General: </strong> 
                    <span style="color: #801AF5; font-size: 16px; font-weight: bold;">$${pedido.total}</span>
                </div>
            </div>
        `,
        icon: 'info',
        confirmButtonText: 'Cerrar',
        confirmButtonColor: '#801AF5',
        width: '500px'
    });
}