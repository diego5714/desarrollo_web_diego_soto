// Espera a que el DOM esté completamente cargado
document.addEventListener('DOMContentLoaded', () => {
    console.log("DOM Cargado");

    // Consigue todas las filas de la tabla en el body (tbody)
    const rows = document.querySelectorAll('tbody tr');

    rows.forEach(row => {
        row.addEventListener('click', () => {
            const url = row.getAttribute('data-href');
            console.log(url);

            if (url) {
                window.location.href = url;
            }
        });
    });
});