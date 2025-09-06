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
}