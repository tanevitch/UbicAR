const formulario = document.getElementById('formulario');
const inputs = document.querySelectorAll('#formulario input') //obtengo arreglo de todos los inputs
const expresiones = {
    nombre: /^[a-zA-ZÀ-ÿ\s]{1,100}$/, //nombres de 1 a 100 caracteres
    email:  /^(?=^.{1,100}$)^[\w-\.]+@([\w-]+\.)+[\w-]{2,4}$/,
    telefono: /^(?:(?:00)?549?)?0?(?:11|[2368]\d)(?:(?=\d{0,2}15)\d{2})??\d{8,10}$/,
    direccion: /^(.{1,100})$/,

}
var campos;
const validateForm = (e) => {
    switch (e.target.name) {//con e.target.name obterngo el campo que el usuario toco
        case "nombre":
            validateYield(expresiones.nombre, e.target, "nombre");
            if (campos["nombre"]){
                document.querySelector(`#grupo_nombre p`).innerText= ""
            }
            else{
                document.querySelector(`#grupo_nombre p`).innerText= "El nombre debe contener solo letras, entre 1 y 46 caracteres"
            }
        break;
        case "email":
            validateYield(expresiones.email, e.target, "email");
            if (campos["email"]){
                document.querySelector(`#grupo_email p`).innerText= ""
            }
            else{
                document.querySelector(`#grupo_email p`).innerText= "El mail no tiene un formato válido"
            }
        break;
        case "telefono":
            validateYield(expresiones.telefono, e.target, "telefono");
            if (campos["telefono"]){
                document.querySelector(`#grupo_telefono p`).innerText= ""
            }
            else{
                document.querySelector(`#grupo_telefono p`).innerText= "El teléfono debe ser ingresado solo de manera numérica"
            }
        break;
        case "direccion":
            validateYield(expresiones.direccion, e.target, "direccion");
            if (campos["direccion"]){
                document.querySelector(`#grupo_direccion p`).innerText= ""
            }
            else{
                document.querySelector(`#grupo_direccion p`).innerText= "La dirección puede tener a lo sumo 100 caracteres"
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
    if (campos.nombre && campos.email && campos.telefono && campos.direccion) {
        formulario.reset
    }
    else {
        e.preventDefault();//si lo preciona me chupo el request y evito que se mande al serv
        return alert('Rellená el formulario con datos válidos')
    }
});



document.addEventListener('DOMContentLoaded', function(){

    if (window.location.href.includes('new')){
        campos = {
            nombre: false,
            email:false, 
            telefono: false,
            direccion: false,
        }
    }
    else{
        campos = {
            nombre: true,
            email:true,
            telefono: true,
            direccion: true,
        }

        for (campo in campos){
            
            document.getElementById(`grupo_${campo}`).classList.add('form-correcto');
            document.querySelector(`#grupo_${campo} i`).classList.remove('fa-times-circle');
            document.querySelector(`#grupo_${campo} i`).classList.add('fa-check-circle');
     
        }

    }
}
)