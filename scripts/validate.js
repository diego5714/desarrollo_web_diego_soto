const validarRegion = (region) => {
    if (!region) return false;
    if (!(region in region_comuna)) return false;

    return true;
}

const validarComuna = (comuna, region) => {
    if (!comuna) return false;
    if (!(comuna in region_comuna[region])) return false;

    return true;
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
    let largoValido = email.length >= 100;

    // Se valida formato con regex (No es perfecto pero funciona)
    let regex = /^[\w.]+@[a-zA-Z_]+?\.[a-zA-Z]{2,3}$/;
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
    if (contacto){
        
        //Falta logica aqui
        
        return true
    }

    return true
}

const validarSelect = (select) => {
    if (!select) return false;
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