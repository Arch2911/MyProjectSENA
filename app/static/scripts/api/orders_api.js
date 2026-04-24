// Fetch para mostrar el pedido al cliente ya autenticado.
export async function obtenerPedidos() {
    
    try {
        const response = await fetch('/orders', {
            method: 'GET',
            headers: {'Content-Type': 'application/json'},
            credentials: 'include'
        });

        const data = await response.json();

        if (!response.ok) {
            console.error('Error HTTP: ', response.status);
        }

        return data;

    } catch (error){
        console.error('Error', error);
        return null;
    }
}
