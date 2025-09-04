let dateTimeMinimo;

const PoblarRegiones = () => {
    let SelectRegion = document.getElementById("region");
    for (const region in region_comuna){
        let option = document.createElement("option");
        option.value = region;
        option.text = region;
        SelectRegion.appendChild(option);
    }
}

const updateComunas = () => {
    let SelectRegion = document.getElementById("region");
    let SelectComuna = document.getElementById("comuna");
    let RegionSeleccionada = SelectRegion.value;

    // Definimos el mensaje por defecto
    SelectComuna.innerHTML = '<option value="">Elige una comuna</option>';

    // Si existen datos de comuna para la region seleccionada, iteramos colocando
    // las opciones de comuna
    if (region_comuna[RegionSeleccionada]){
        region_comuna[RegionSeleccionada].forEach(comuna => {
            let option = document.createElement("option");
            option.value = comuna;
            option.text = comuna;
            SelectComuna.appendChild(option);
        });
    }
}

const PoblarFechaHora = () => {
    let inputDateTime = document.getElementById("fecha");

    const ahora = new Date();
    ahora.setMinutes(ahora.getMinutes() - ahora.getTimezoneOffset());
    ahora.setHours(ahora.getHours() + 3);

    dateTimeMinimo = ahora;
    inputDateTime.value = ahora.toISOString().slice(0,16);
}

// Agregamos eventListeners para actuar ante cambios en la seleccion.
document.getElementById("region").addEventListener("change", updateComunas)

window.onload = () => {
    PoblarRegiones();
    PoblarFechaHora();
}