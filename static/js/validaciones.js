function validatePunto(num) {
    const r = /[0-9]\.[0-9]{2}$/;
    if (r.test(num)) {
        return true
    }
    return false
}

function validatePlaca(num) {
    // const r = /^([A-Z]{3})-([0-9]{3})$/;

    if (num.length==8) {
        return true
    }
    return false
}

function validateAño(num) {
    if (parseInt(num) > 1700 && parseInt(num) <3000) {
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

function numbersDigits(val, digitos) {
    let value = val.trim()
    var digits = /^[0-9]*$/;
    let data = {
        status: 200
    }
    if(value.length!=digitos){
        data.status = 500
        data.mensaje = `Este campo debe tener ${digitos} dígitos.`
    }
    if (!digits.test(value)) {
        data.status = 500
        data.mensaje = "Este número es inválido."
    }
    return data

}
function docDigits(tipo, num) {
    let value = num.trim()
    var digits = /^[0-9]*$/;

    let data = {
        status: 200
    }
    if (tipo == 1) {
        if (value.length != 8) {
            data.status = 500
            data.mensaje = "El DNI tiene que tener 8 dígitos."
        }
        if (!digits.test(value)) {
            data.status = 500
            data.mensaje = "El DNI es inválido."
        }
    } else
    if (tipo == 2) {
        if (value.length != 9) {
            data.status = 500,
                data.mensaje = "El Carnet de extranjería tiene que tener 9 dígitos."
        }
        if (!digits.test(value)) {
            data.status = 500
            data.mensaje = "El DNI es inválido."
        }
    } else
    if (tipo == 4) {
        if (value.length != 11) {
            data.status = 500,
                data.mensaje = "El RUC debe tener 11 dígitos."

        }
        if (!digits.test(value)) {
            data.status = 500
            data.mensaje = "El RUC es inválido."
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
    let data = {}
    console.log(re.exec(valor.value));
    if (re.exec(valor.value) != null) {
        if (valor.value.search("gmail") != -1 || valor.value.search("hotmail") != -1) {
            console.log("entro al gmail");
            data.status = 200
        } else {
            console.log("no tiene gmail o hotmail");
            data.status = 500
            data.mensaje = "Ingrese un email válido."

        }

    } else {
        data.status = 500
        data.mensaje = "Ingrese un correo válido."

        if (valor.value == "") {
            data.mensaje = "Este campo es requerido."

        } 
       
    }
    return data

}