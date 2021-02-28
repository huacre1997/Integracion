function validatePunto(num) {
    const r=/[0-9]\.[0-9]{2}$/;
    if (r.test(num)) {
        return true
    }
    return false
}
function validatePlaca(num) {
    const r = /^([A-Z]{3})-([0-9]{3})$/;    
    
    if (r.test(num)) {
        return true
    }
    return false
}
function validateAño(num) {
    if(parseInt(num)>1900 && parseInt(num)<2010){
        return true
    }
    return false
}

function startPunto(num) {
    let val = num.trim().startsWith(".")
    if (val == false) {
        return false
    }
    return true
}

function hasLetters(num) {
    var regExp = /[a-zA-Z]/g;

    if (regExp.test(num)) {
        return true
    } else {
        return false
    }
}

function hasNUmbers(num) {
    var regExp = /[0-9]/g;

    if (regExp.test(num)) {
        return true
    } else {
        return false
    }
}

function AlfaNumerico(value) {
    if (hasLetters(value) && hasNUmbers(value)) {
        return true
    }
    return false
}

function docDigits(tipo, num) {
    let value = num.trim()
    let data = {
        status: 200
    }
    if (tipo == 1) {
        if (value.length != 8) {
            data.status = 500
            data.mensaje = "El DNI tiene que tener 8 dígitos."
        }
    } else
    if (tipo == 2) {
        if (value.length != 9) {
            data.status = 500,
            data.mensaje = "El Carnet de extranjería tiene que tener 9 dígitos."
        }

    } else
    if (tipo == 4) {
        if (value.length != 11) {
            data.status = 500,
            data.mensaje = "El RUC debe tener 11 dígitos."

        }
    } else {
        data = {
            status: 500,
            mensaje: "Ingrese un valor válido."
        }
    }
    return data
}

function validarEmail(valor) {
    re = /^([\da-z_\.-]+)@([\da-z\.-]+)\.([a-z\.]{2,6})$/
    if (valor.value.search("gmail") != -1 || valor.value.search("hotmail") != -1) {
        if (!re.exec(valor)) {
            data = {
                status: 200,
            }
            return data
        } else {
            data = {
                status: 500,
                mensaje: "Ingrese un email válido."
            }
            return data
        }
    } else {
        data = {
            status: 500,
            mensaje: "Ingrese un email válido."
        }
        return data
    }
}