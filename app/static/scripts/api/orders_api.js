// Fetch para mostrar el pedido al cliente ya autenticado.
export async function obtenerPedidos() {
    
    try {
        const response = await fetch('/orders', {
            method: 'GET',
            credentials: 'include'
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
