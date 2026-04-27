import { obtenerPedidos } from "../api/orders_api.js";

// Fetch para buscar el cliente.
export async function buscarCliente(cedula) {


    try {
        const response = await fetch('/auth/login', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            credentials: 'include',
            body: JSON.stringify({ cedula })
        });

        const data = await response.json();

        return {
            ok: response.ok,
            status: response.status,
            data
        };

    } catch (error){
        console.error('Error de red', error);
        return {
            ok: false,
            status: 0,
            error: 'network_error'
        };
    }

}

// Fetch para verificar y autenticar el cliente.
export async function verificarOtp(codigo) {

    try {
        const response = await fetch('/auth/verify', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        credentials: 'include',
        body: JSON.stringify({ codigo })
        });


        const data = await response.json();

        return {
            ok: response.ok,
            status: response.status,
            data
        };

    } catch (error){
        console.error('Error de red', error);
        return {
            ok: false,
            status: 0,
            error: 'network_error'
        };
    }
}
