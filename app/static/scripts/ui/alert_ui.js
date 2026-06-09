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