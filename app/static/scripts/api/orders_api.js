// Fetch para mostrar el pedido al cliente ya autenticado.
export async function obtenerPedidos() {
    
    try {
        const response = await fetch('/orders', {
            method: 'GET',
            headers: {'Content-Type': 'application/json'},
            credentials: 'include'
        });

        const data = await response.json();

        return data;

    } catch (error){
        console.error('Error', error);
        return null;
    }
}
