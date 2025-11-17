let dateTimeMinimo;

const PoblarRegiones = () => {
    let SelectRegion = document.getElementById("region");
    
    datos_regiones_comunas.forEach(region => {
        let option = document.createElement("option");
        option.value = region.id;
        option.text = region.nombre;
        SelectRegion.appendChild(option);
    });
}

const updateComunas = () => {
    const SelectRegion = document.getElementById("region");
    const SelectComuna = document.getElementById("comuna");
    const RegionSeleccionadaId = SelectRegion.value;

    // Definimos el mensaje por defecto
    SelectComuna.innerHTML = '<option value="">Elige una comuna</option>';

    // Si se seleccionó una region válida (No por defecto)
    if (RegionSeleccionadaId){
        // Encontramos la region seleccionada en array de datos segun su ID
        const region_encontrada = datos_regiones_comunas.find(region => region.id == RegionSeleccionadaId);

        // Si la region fue encontrada, y tiene comunas, las poblamos
        if (region_encontrada && region_encontrada.comunas){
            region_encontrada.comunas.forEach(comuna => {
                let option = document.createElement("option");
                option.value = comuna.id;
                option.text = comuna.nombre;
                SelectComuna.appendChild(option);
            });
        }
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

const toggleRedes = () => {
    let valorWhatsapp = document.getElementById("whatsapp").checked;
    let valorTelegram = document.getElementById("telegram").checked;
    let valorTwitter = document.getElementById("twitter").checked;
    let valorInstagram = document.getElementById("instagram").checked;
    let valorTiktok = document.getElementById("tiktok").checked;
    let valorOtra = document.getElementById("otra").checked;

    let inputWhatsapp = document.getElementById("whatsapp-input");
    let inputTelegram = document.getElementById("telegram-input");
    let inputTwitter = document.getElementById("twitter-input");
    let inputInstagram = document.getElementById("instagram-input");
    let inputTiktok = document.getElementById("tiktok-input");
    let inputOtra = document.getElementById("other-input");

    inputWhatsapp.hidden = !valorWhatsapp;
    inputTelegram.hidden = !valorTelegram;
    inputTwitter.hidden = !valorTwitter;
    inputInstagram.hidden = !valorInstagram;
    inputTiktok.hidden = !valorTiktok;
    inputOtra.hidden = !valorOtra;

    if (inputWhatsapp.hidden){
        inputWhatsapp.value = "";
    }
    if (inputTelegram.hidden){
        inputTelegram.value = "";
    }
    if (inputTwitter.hidden){
        inputTwitter.value = "";
    }
    if (inputInstagram.hidden){
        inputInstagram.value = "";
    }
    if (inputTiktok.hidden){
        inputTiktok.value = "";
    }
    if (inputOtra.hidden){
        inputOtra.value = "";
    }
    
}

// Agregamos eventListeners para actuar ante cambios en la seleccion.
document.getElementById("region").addEventListener("change", updateComunas);
document.getElementById("whatsapp").addEventListener("change", toggleRedes);
document.getElementById("telegram").addEventListener("change", toggleRedes);
document.getElementById("twitter").addEventListener("change", toggleRedes);
document.getElementById("instagram").addEventListener("change", toggleRedes);
document.getElementById("tiktok").addEventListener("change", toggleRedes);
document.getElementById("otra").addEventListener("change", toggleRedes);

window.onload = () => {
    PoblarRegiones();
    PoblarFechaHora();
    toggleRedes();
    updateComunas();
}