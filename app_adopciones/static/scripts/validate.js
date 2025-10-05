const validarRegionComuna = (region_id, comuna_id) => {
    if (!region_id || !comuna_id) return false;

    const region_encontrada = datos_regiones_comunas.find(region => region.id == region_id);
    
    if (!region_encontrada) return false;

    const comuna_encontrada = region_encontrada.comunas.find(comuna => comuna.id == comuna_id);
    
    return comuna_encontrada !== undefined;
}

const validarSector = (sector) => {
    if (sector){
        let largoValido = sector.trim().length <= 100;
        return largoValido;
    }

    return true;
}

const validarNombre = (nombre) => {
    if (!nombre) return false;
    let largo = nombre.trim().length
    let largoValido = largo >= 3 && largo <= 200;

    return largoValido;
}

const validarEmail = (email) => {
    if (!email) return false;
    let largoValido = email.length <= 100;

    // Se valida formato con regex
    const regex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
    let formatoValido = regex.test(email);

    return largoValido && formatoValido;
}

const validarTelefono = (telefono) => {
    if (telefono){
        let largoValido = telefono.length == 13;

        // Se valida formato con regex
        let regex = /^\+\d{3}\.\d{8}$/;
        let formatoValido = regex.test(telefono);

        return largoValido && formatoValido;
    }
    return true;
}

const validarContacto = (contacto) => {
    let largo = contacto.trim().length;
    let largoValido = largo >= 4 && largo <= 50;

    return largoValido;
}

const validarContactos = (contactos) => {
    if (contactos.length != 0){
        if (contactos.length > 6) return false;
        
        for (const contacto of contactos){
            let valido = validarContacto(contacto);
            if (!valido) return false;
        }
        
        return true
    }

    return true
}

const validarTipo = (tipo) => {
    if (!tipo) return false;

    let tipos = ["Perro", "Gato"];
    if (!(tipos.includes(tipo))) return false;
    
    return true;
}

const validarUnidad = (unidad) => {
    if (!unidad) return false;

    let unidades = ["Meses", "Años"];
    if (!(unidades.includes(unidad))) return false;
    
    return true;
}

const validarEntero = (cantidad) => {
    if (!cantidad) return false;
    let cantidadValida = cantidad > 0;

    return cantidadValida;
}

const validarDateTime = (datetime_string) => {
    const dateTimeUsuario = new Date(datetime_string);

    //Chequeamos si la fecha era válida
    if (isNaN(dateTimeUsuario)) return false;

    if (dateTimeUsuario < dateTimeMinimo) return false

    return true;
}

const validarArchivos = (archivos) => {
    if (!archivos) return false;
    let largo = archivos.length
    let largoValido = largo >= 1 && largo <= 5;

    let tipoValido = true;
    for (const archivo of archivos){
        let fileFamily = archivo.type.split("/")[0];
        tipoValido &&= fileFamily == "image";
    }

    return largoValido && tipoValido
}

const validateForm = () => {
    
    console.log("Ejecutando validación");

    let Formulario = document.forms["formulario"];
    let region = Formulario["region"].value;
    let comuna = Formulario["comuna"].value;
    let sector = Formulario["sector"].value;

    let nombre = Formulario["nombre"].value;
    let email = Formulario["email"].value;
    let telefono = Formulario["telefono"].value;
    
    let redes = [];
    let whatsapp = Formulario["whatsapp-input"].value;
    let telegram = Formulario["telegram-input"].value;
    let twitter = Formulario["twitter-input"].value;
    let instagram = Formulario["instagram-input"].value;
    let tiktok = Formulario["tiktok-input"].value;
    let otra = Formulario["other-input"].value;

    if (whatsapp) redes.push(whatsapp);
    if (telegram) redes.push(telegram); 
    if (twitter) redes.push(twitter); 
    if (instagram) redes.push(instagram); 
    if (tiktok) redes.push(tiktok); 
    if (otra) redes.push(otra); 

    let tipo = Formulario["tipo"].value;
    let cantidad = Formulario["cantidad"].value;
    let edad = Formulario["edad"].value;
    let unidad = Formulario["unidad"].value;
    let fecha = Formulario["fecha"].value;
    let fotos = Formulario["fotos"].files;
    

    // variables auxiliares de validación y función.
    let invalidInputs = [];
    let isValid = true;
    const setInvalidInput = (inputName) => {
        invalidInputs.push(inputName);
        isValid &&= false;
    };

    // lógica de validación
    if (!validarRegionComuna(region, comuna)){
        setInvalidInput("Región y/o Comuna");
    }
    if (!validarSector(sector)){
        setInvalidInput("Sector (A lo mas 100 caracteres)");
    }
    if (!validarNombre(nombre)) {
        setInvalidInput("Nombre (Entre 3 y 200 caracteres)");
    }
    if (!validarEmail(email)) {
        setInvalidInput("Email");
    }
    if (!validarTelefono(telefono)) {
        setInvalidInput("Teléfono (+569.12345678)");
    }
    if (!validarContactos(redes)){
        setInvalidInput("Redes Sociales");
    }
    if (!validarTipo(tipo)){
        setInvalidInput("Tipo de mascota");
    }
    if (!validarEntero(cantidad)){
        setInvalidInput("Cantidad");
    }
    if (!validarEntero(edad)){
        setInvalidInput("Edad");
    }
    if (!validarUnidad(unidad)){
        setInvalidInput("Unidad de tiempo");
    }
    if (!validarDateTime(fecha)){
        setInvalidInput("Fecha de entrega (No menos de 3 horas en el futuro)");
    }
    if (!validarArchivos(fotos)) {
        setInvalidInput("Fotos");
    }

    // finalmente mostrar la validación
    let validationBox = document.getElementById("val-box");
    let validationMessageElem = document.getElementById("val-msg");
    let validationListElem = document.getElementById("val-list");
    
    let confirmationBox = document.getElementById("confirm-box");
    let confirmationMessageElem = document.getElementById("confirm-msg");
    let confirmationListElem = document.getElementById("confirm-list");


    if (!isValid) {
        validationListElem.textContent = "";
        // agregar elementos inválidos al elemento val-list.
        for (input of invalidInputs) {
        let listElement = document.createElement("li");
        listElement.innerText = input;
        validationListElem.append(listElement);
        }
        // establecer val-msg
        validationMessageElem.innerText = "Los siguientes campos son inválidos:";

        // aplicar estilos de error
        validationBox.style.backgroundColor = "#ffdddd";
        validationBox.style.borderLeftColor = "#f44336";

        // hacer visible el mensaje de validación
        validationBox.hidden = false;
    } else {
        // Ocultar el formulario
        Formulario.style.display = "none";

        // establecer mensaje de éxito
        confirmationMessageElem.innerText = "¿Está seguro que desea agregar este aviso de adopción?";
        confirmationListElem.textContent = "";

        // aplicar estilos de éxito
        confirmationBox.style.backgroundColor = "#ddffdd";
        confirmationBox.style.borderLeftColor = "#4CAF50";

        // Agregar botones para enviar el formulario o volver
        let submitButton = document.createElement("button");
        submitButton.innerText = "Sí, estoy seguro";
        submitButton.style.marginRight = "10px";
        submitButton.addEventListener("click", () => {
            Formulario.submit();
            confirmationBox.hidden = true;
            mostrarPantallaExito();
        });

        let backButton = document.createElement("button");
        backButton.innerText = "No, no estoy seguro, quiero volver al formulario";
        backButton.addEventListener("click", () => {
        // Mostrar el formulario nuevamente
        Formulario.style.display = "flex";
        confirmationBox.hidden = true;
        });

        confirmationListElem.appendChild(submitButton);
        confirmationListElem.appendChild(backButton);

        // hacer visible el mensaje de validación
        confirmationBox.hidden = false;
    }
}

const mostrarPantallaExito = () => {
    let successBox = document.getElementById("success-box");
    let successMessageElem = document.getElementById("success-msg");
    let successListElem = document.getElementById("success-list");

    successMessageElem.innerText = "Hemos recibido la información de adopción, muchas gracias y suerte";
    successListElem.textContent = "";

    let submitButton = document.createElement("button");
    submitButton.innerText = "Volver al inicio";
    submitButton.style.marginRight = "10px";
    submitButton.addEventListener("click", () => {
        window.location.href = '/';
    });

    successListElem.appendChild(submitButton);
    successBox.hidden = false;
}

let submitBtn = document.getElementById("submit-btn");
submitBtn.addEventListener("click", validateForm);