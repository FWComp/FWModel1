// Función para cambiar la visibilidad de los formularios y los botones de radio
function cambiarVisibilidad(formularioMostrar, radioMostrar, formularioOcultar, radioOcultar) {
    document.getElementById(formularioMostrar).style.display = 'block';
    document.getElementById(formularioOcultar).style.display = 'none';
    document.getElementById(radioMostrar).checked = true;
    document.getElementById(radioOcultar).checked = false;
}

// Función para manejar el clic en los botones de radio en el formulario de inicio de sesión
function handleClickRadioLogin(arg) {
    var radioOption2_Login = document.getElementById('radioOption2_Login');
    if (arg) {
        radioOption2_Login.checked = true
    }
    if (radioOption2_Login.checked) {
        cambiarVisibilidad('SignUp', 'radioOption2_SignUp', 'LogIn', 'radioOption1_Login');
    }
}

// Función para manejar el clic en los botones de radio en el formulario de registro
function handleClickRadioSignUp(arg) {
    var radioOption1_SignUp = document.getElementById('radioOption1_SignUp');
    if (arg) {
        radioOption1_SignUp.checked = true
    }
    if (radioOption1_SignUp.checked) {
        cambiarVisibilidad('LogIn', 'radioOption1_Login', 'SignUp', 'radioOption2_SignUp');
    }
}

function handleKeyPress(event) {
    switch(event.key) {
        case 'ArrowLeft':
            const callLogIn = (document.getElementById('LogIn').style.display === 'none') ? handleClickRadioSignUp(1) : handleClickRadioLogin(1);
            break;
        
        case 'ArrowRight':
            const callSignUp = (document.getElementById('SignUp').style.display === 'none') ? handleClickRadioLogin(1) : handleClickRadioSignUp(1);
            break
    }
}

// Asignar los manejadores de eventos
document.getElementById('radioOption2_Login').addEventListener('click', handleClickRadioLogin);
document.getElementById('radioOption1_SignUp').addEventListener('click', handleClickRadioSignUp);
document.addEventListener('keydown', handleKeyPress);
