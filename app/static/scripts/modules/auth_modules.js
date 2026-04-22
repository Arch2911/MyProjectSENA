

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

            const data = await buscarCliente(cedula);

            if (!data) {
                alert('Error de conexión');
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

            const data = await verificarOtp(codigo);

            if (!data) {
                alert('Error de conexión');
                return;
            }

            if (data.status === 'success') {
                window.location.href = '/pedidos';
            }
        });
    }
}
