

import { buscarCliente, verificarOtp } from '../api/auth_api.js';

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

        // buscar cliente
        btnBuscar.addEventListener('click', async () => {

            const cedula = inputCedula.value;

            const response = await buscarCliente(cedula);
            
            if (response.status === 0) {
                alert('Sin conexión de red o al servidor');
                return;
            }

            if (!response.ok) {
                alert(`Error HTTP: ${response.status}`);
                return;
            }

            const data = response.data;

            if (data.status === 'error') {

                // Se evalua los tipos de errores

                if (data.error === 'json_requerido') {
                    alert('No has ingresando ningún dato')
                }else if (data.error === 'cedula_requerida') {
                    alert('Por favor ingresa la cédula para la consulta')
                }else if (data.error === 'cliente_no_existe') {
                    alert('No se ha encontrado un cliente con esa cédula');
                }

                return;

            }

            if (data.status === 'success') {
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
                alert('Sin conexión de red o al servidor');
                return;
            }

            if (!response.ok) {
                alert(`Error HTTP: ${response.status}`);
                return;
            }

            const data = response.data;

            if (data.status === 'error') {

                // Se evalua los tipos de errores

                if (data.error === 'json_requerido') {
                    alert('No hay datos ingresados')
                } else if (data.error === 'sesion_invalida') {
                    alert('La sesión ha expirado, vuelve a iniciar sesión')
                    window.location.href = '/';
                } else if (data.error === 'cliente_no_existe') {
                    alert('No se ha encontrado un cliente esa cédula');
                } else if (data.error === 'codigo_requerido') {
                    alert('Por favor ingresa el código completo')
                } else if (data.error === 'codigo_invalido') {
                    alert('El código es incorrecto, intenta nuevamente')
                } else if (data.error === 'codigo_expirado') {
                    alert ('El código expiró, solicita uno nuevo')
                    window.location.href = '/';
                }

                return;

            }

            if (data.status === 'success') {

                window.location.href = '/pedidos';
            }
        });
    }
}
