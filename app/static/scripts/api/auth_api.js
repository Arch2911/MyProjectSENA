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

        if (!response.ok) {
            console.error('Error HTTP: ', response.status);
            return data;
        }

        return data;

    } catch (error) {
        console.error('Error buscarCliente:', error);
        return null;
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

        if (!response.ok) {
            console.error('Error HTTP: ', response.status);
            return data;
        }

        return data;

    } catch (error) {
        console.error('Error verificarOtp:', error);
        return null;
    }
}
