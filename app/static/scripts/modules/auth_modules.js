

import { buscarCliente, verificarOtp } from '../api/auth_api.js';
import { mostrarAlertaError, mostrarAlertaOk, mostrarAlertaTiempo, mostrarAlertaSesion } from '../ui/alert_ui.js';

// Mostrar formulario OTP
function mostrarFormularioOTP() {
    document.getElementById('form-cedula').classList.add('oculto');
    document.getElementById('form-otp').classList.remove('oculto');
}

// Inicializar flujo completo de auth
export function initAuth() {

    const inputCedula = document.getElementById('cedula');
    const btnBuscar = document.getElementById('btn');

    const btnOtp = document.getElementById('btn-otp');
    const inputsOtp = [...document.querySelectorAll('.code-input')];

    // VALIDACIÓN INPUT CÉDULA
    if (inputCedula && btnBuscar) {
        inputCedula.addEventListener('input', () => {
            btnBuscar.disabled = inputCedula.value.trim() === '';
        });

        //Consultar con al presionar enter
        inputCedula.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' && !btnBuscar.disabled) {
                btnBuscar.click();
            }
        })

        // buscar cliente
        btnBuscar.addEventListener('click', async () => {

            const cedula = inputCedula.value;

            const response = await buscarCliente(cedula);
            
            if (response.status === 0) {
                mostrarAlertaError({
                    title: 'Sin conexión',
                    text: 'Falla en la red o servidor'
                })
                return;
            }

            if (!response.ok) {
                console.error(`Error HTTP: ${response.status}`);
            }

            const data = response.data;

            console.log('RESPUESTA COMPLETA:', data);
            console.log('ERROR:', data?.error);

            if (data?.status === 'error') {

                // Se evalua los tipos de errores

                if (data.error === 'cliente_no_existe') {
                    mostrarAlertaError({
                        icon : 'info',
                        title: 'Cliente no existe',
                        text: 'No se ha encontrado un cliente con esa cédula'
                    })
                    return;
                }

                console.warn('Error no esperado:', data.error);
                return;

            }

            if (data.status === 'success') {
                mostrarAlertaOk({
                    title: 'SMS enviado con exito'
                })

                mostrarFormularioOTP();
            }
        });
    }


    if (inputsOtp.length && btnOtp) {

        inputsOtp.forEach((input, index) => {

            // retroceso
            input.addEventListener('keydown', (e) => {
                if (e.key === 'Backspace' && !input.value) {
                    inputsOtp[Math.max(0, index - 1)].focus();
                }

                //Consultar con al presionar enter
                if (e.key === 'Enter' && !btnOtp.disabled) {
                    btnOtp.click(); // reutiliza la lógica existente
                }
            });

            // avance
            input.addEventListener('input', () => {

                input.value = input.value.replace(/\D/g, '');

                if (input.value && index < inputsOtp.length - 1) {
                    inputsOtp[index + 1].focus();
                }

                const completo = inputsOtp.every(i => i.value.length === 1);
                btnOtp.disabled = !completo;
            });
        });

        // verificar OTP
        btnOtp.addEventListener('click', async () => {

            const codigo = inputsOtp.map(i => i.value).join('');

            const response = await verificarOtp(codigo);

            if (response.status === 0) {
                    mostrarAlertaError({
                        icon: 'question',
                        title: 'Sin conexión de red o el servidor',
                        text: 'Verifica nuevamente.'
                    })
                return;
            }

            if (!response.ok) {
                console.error(`Error HTTP: ${response.status}`);
            }

            const data = response.data;

            if (data?.status === 'error') {

                // Se evalua los tipos de errores

                if (data.error === 'sesion_invalida') {
                    mostrarAlertaSesion();
                    return;
                }
                
                if (data.error === 'codigo_invalido') {
                    mostrarAlertaError({
                        icon: 'error',
                        title: 'El código ingresado es incorrecto',
                        text: 'Verifica nuevamente.'
                    })
                    return;
                }
                
                if (data.error === 'codigo_expirado') {
                    mostrarAlertaError({
                        icon: 'info',
                        title: 'El código ha expirado',
                        text: 'Intenta conseguir uno nuevo.',
                        redirect: '/'
                    })
                    return;
                }

                console.warn('Error no esperado:', data.error);
                return;

            }

            if (data.status === 'success') {

                mostrarAlertaTiempo({
                    title: 'Verificación exitosa',
                    timer: 2000,
                    redirect: '/pedidos'
                })
            }
        })
    }
}
