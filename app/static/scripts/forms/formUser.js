const formulario = document.getElementById('formulario');
const inputs = document.querySelectorAll('#formulario input') //obtengo arreglo de todos los inputs
const expresiones = {
    fname:  /^[a-zA-ZÀ-ÿ\s]{1,100}$/, 
    email:  /^(?=^.{1,100}$)^[\w-\.]+@([\w-]+\.)+[\w-]{2,4}$/, 
    lname:  /^[a-zA-ZÀ-ÿ\s]{1,100}$/,
    password: /^(.{1,100})$/,
    username: /^(.{1,100})$/
}

const validateForm = (e) => {
    switch (e.target.name) {//con e.target.name obterngo el campo que el usuario toco
        case "email":
            validateYield(expresiones.email, e.target, "email");
            if (campos["email"]){
                document.querySelector(`#grupo_email p`).innerText= ""
            }
            else{
                document.querySelector(`#grupo_email p`).innerText= "El mail no tiene un formato válido"
            }
        break;
        case "fname":
            validateYield(expresiones.fname, e.target, "fname");
            if (campos["fname"]){
                document.querySelector(`#grupo_fname p`).innerText= ""
            }
            else{
                document.querySelector(`#grupo_fname p`).innerText= "El nombre debe contener solo letras, entre 1 y 100 caracteres"
            }
        break;
        case "lname":
            validateYield(expresiones.lname, e.target, "lname");
            if (campos["lname"]){
                document.querySelector(`#grupo_lname p`).innerText= ""
            }
            else{
                document.querySelector(`#grupo_lname p`).innerText= "El apellido debe contener solo letras, entre 1 y 100 caracteres"
            }
        break;
        case "password":
            // si el campo es requerido y puso algo, lo valido
            if (e.target.value || e.target.hasAttribute("required")){
                validateYield(expresiones.password, e.target, "password");
            } // si no es requerido y no puso nada, es porque está editando y va a tomar la pass anterior
            else if  (! e.target.hasAttribute("required")){
                campos["password"]=true
                document.getElementById(`grupo_password`).classList.remove('form-incorrecto');
                document.getElementById(`grupo_password`).classList.add('form-correcto');
                document.querySelector(`#grupo_password i`).classList.remove('fa-times-circle');
                document.querySelector(`#grupo_password i`).classList.add('fa-check-circle');
            }

            if (campos["password"]){
                document.querySelector(`#grupo_password p`).innerText= ""
            }
            else{
                document.querySelector(`#grupo_password p`).innerText= "La contraseña debe tener máximo 100 caracteres"
            }
            
        break;
        case "username":
            validateYield(expresiones.username, e.target, "username");
            if (campos["username"]){
                document.querySelector(`#grupo_username p`).innerText= ""
            }
            else{
                document.querySelector(`#grupo_username p`).innerText= "El nombre de usuario debe tener máximo 100 caracteres"
            }
        break;
    } 
}
const validateYield = (expresion,input,campo) => {
    if(expresion.test(input.value)){
        document.getElementById(`grupo_${campo}`).classList.remove('form-incorrecto');
        document.getElementById(`grupo_${campo}`).classList.add('form-correcto');
        document.querySelector(`#grupo_${campo} i`).classList.remove('fa-times-circle');
        document.querySelector(`#grupo_${campo} i`).classList.add('fa-check-circle');
        campos[campo]=true
    } else {
        document.getElementById(`grupo_${campo}`).classList.add('form-incorrecto');
        document.getElementById(`grupo_${campo}`).classList.remove('form-correcto');
        document.querySelector(`#grupo_${campo} i`).classList.add('fa-times-circle');
        document.querySelector(`#grupo_${campo} i`).classList.remove('fa-check-circle');
        campos[campo]=false
    }
}
inputs.forEach((input) => {
    input.addEventListener('keyup', validateForm); // si levanta tecla ejecuta la funcion esta
    input.addEventListener('blur', validateForm); // si cliquea fuera del campo tambien valida
});

formulario.addEventListener('submit', (e) => {//agrego un event para escuchar si el usuario precione el boton de submit
    if (campos.fname && campos.lname && campos.email && campos.password && campos.username) {
        formulario.reset
    }
    else {
        e.preventDefault()
        return alert('Rellená el formulario con datos válidos')
    }
});

document.addEventListener('DOMContentLoaded', function(){

    if (window.location.href.includes('new')){
        campos = {
            fname: false,
            email:false, 
            lname: false,
            password: false,
            username: false,
        }
    }
    else{
        campos = {
            username: true,
            lname: true,
            fname: true,
            email:true, 
            password: true,
        }

        for (campo in campos){
            
            document.getElementById(`grupo_${campo}`).classList.add('form-correcto');
            document.querySelector(`#grupo_${campo} i`).classList.remove('fa-times-circle');
            document.querySelector(`#grupo_${campo} i`).classList.add('fa-check-circle');
     
        }

    }
}
)
