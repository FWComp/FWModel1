const add = document.getElementById('newCharacter')
const Form = document.getElementById('FormCharacter')
const exit = document.getElementById('cancel')
const Section = document.getElementById('sectionCharacters')
const consola = document.getElementById('console');
const profile = document.getElementById('profile_menu')
const spanRange = document.getElementById('rangeSpan')
const inputRange = document.getElementById('range')
const menu_ajustes = document.getElementById('menu_ajustes_prin');
const abrir_menu_btn = document.getElementById('abrir_menu');
const cerrar_menu_btn = document.getElementById('cerrar_menu');
const profile_menu_open = document.getElementById('profile_menu_open')
const menu_desp_lateral = document.getElementById('menu_desplegable_lateral');
const exit_profile_menu = document.getElementById('exit_profile_menu')
const abrir_menu_ajustes = document.getElementById('abrir_menu_ajustes');
const cerrar_menu_ajustes = document.getElementById('exit_menu_ajustes');

const countriesUnique = [
    { code: 'af', name: 'Afganistán' },
    { code: 'al', name: 'Albania' },
    { code: 'dz', name: 'Argelia' },
    { code: 'ad', name: 'Andorra' },
    { code: 'ao', name: 'Angola' },
    { code: 'ar', name: 'Argentina' },
    { code: 'am', name: 'Armenia' },
    { code: 'au', name: 'Australia' },
    { code: 'at', name: 'Austria' },
    { code: 'az', name: 'Azerbaiyán' },
    { code: 'bs', name: 'Bahamas' },
    { code: 'bh', name: 'Baréin' },
    { code: 'bd', name: 'Bangladés' },
    { code: 'by', name: 'Bielorrusia' },
    { code: 'be', name: 'Bélgica' },
    { code: 'bz', name: 'Belice' },
    { code: 'bj', name: 'Benín' },
    { code: 'bt', name: 'Bután' },
    { code: 'bo', name: 'Bolivia' },
    { code: 'ba', name: 'Bosnia y Herzegovina' },
    { code: 'bw', name: 'Botsuana' },
    { code: 'br', name: 'Brasil' },
    { code: 'bn', name: 'Brunéi' },
    { code: 'bg', name: 'Bulgaria' },
    { code: 'bf', name: 'Burkina Faso' },
    { code: 'bi', name: 'Burundi' },
    { code: 'kh', name: 'Camboya' },
    { code: 'cm', name: 'Camerún' },
    { code: 'ca', name: 'Canadá' },
    { code: 'cv', name: 'Cabo Verde' },
    { code: 'td', name: 'Chad' },
    { code: 'cl', name: 'Chile' },
    { code: 'cn', name: 'China' },
    { code: 'co', name: 'Colombia' },
    { code: 'km', name: 'Comoras' },
    { code: 'cg', name: 'Congo' },
    { code: 'cr', name: 'Costa Rica' },
    { code: 'hr', name: 'Croacia' },
    { code: 'cu', name: 'Cuba' },
    { code: 'cy', name: 'Chipre' },
    { code: 'cz', name: 'República Checa' },
    { code: 'dk', name: 'Dinamarca' },
    { code: 'dj', name: 'Yibuti' },
    { code: 'dm', name: 'Dominica' },
    { code: 'do', name: 'República Dominicana' },
    { code: 'ec', name: 'Ecuador' },
    { code: 'eg', name: 'Egipto' },
    { code: 'sv', name: 'El Salvador' },
    { code: 'gq', name: 'Guinea Ecuatorial' },
    { code: 'er', name: 'Eritrea' },
    { code: 'ee', name: 'Estonia' },
    { code: 'et', name: 'Etiopía' },
    { code: 'fj', name: 'Fiyi' },
    { code: 'fi', name: 'Finlandia' },
    { code: 'fr', name: 'Francia' },
    { code: 'ga', name: 'Gabón' },
    { code: 'gm', name: 'Gambia' },
    { code: 'ge', name: 'Georgia' },
    { code: 'de', name: 'Alemania' },
    { code: 'gh', name: 'Ghana' },
    { code: 'mx', name: 'México' },
    { code: 'us', name: 'Estados Unidos' },
    { code: 'jp', name: 'Japón' },
    { code: 'gr', name: 'Grecia' },
    { code: 'gd', name: 'Granada' },
    { code: 'gt', name: 'Guatemala' },
    { code: 'gn', name: 'Guinea' },
    { code: 'gw', name: 'Guinea-Bisáu' },
    { code: 'gy', name: 'Guyana' },
    { code: 'ht', name: 'Haití' },
    { code: 'hn', name: 'Honduras' },
    { code: 'hu', name: 'Hungría' },
    { code: 'is', name: 'Islandia' },
    { code: 'in', name: 'India' },
    { code: 'id', name: 'Indonesia' },
    { code: 'ir', name: 'Irán' },
    { code: 'iq', name: 'Irak' },
    { code: 'ie', name: 'Irlanda' },
    { code: 'il', name: 'Israel' },
    { code: 'it', name: 'Italia' },
    { code: 'ci', name: 'Costa de Marfil' },
    { code: 'jm', name: 'Jamaica' },
    { code: 'jo', name: 'Jordania' },
    { code: 'kz', name: 'Kazajistán' },
    { code: 'ke', name: 'Kenia' },
    { code: 'ki', name: 'Kiribati' },
    { code: 'kw', name: 'Kuwait' },
    { code: 'kg', name: 'Kirguistán' },
    { code: 'la', name: 'Laos' },
    { code: 'lv', name: 'Letonia' },
    { code: 'lb', name: 'Líbano' },
    { code: 'ls', name: 'Lesoto' },
    { code: 'lr', name: 'Liberia' },
    { code: 'ly', name: 'Libia' },
    { code: 'li', name: 'Liechtenstein' },
    { code: 'lt', name: 'Lituania' },
    { code: 'lu', name: 'Luxemburgo' },
    { code: 'mk', name: 'Macedonia del Norte' },
    { code: 'mg', name: 'Madagascar' },
    { code: 'mw', name: 'Malaui' },
    { code: 'my', name: 'Malasia' },
    { code: 'mv', name: 'Maldivas' },
    { code: 'ml', name: 'Malí' },
    { code: 'mt', name: 'Malta' },
    { code: 'mh', name: 'Islas Marshall' },
    { code: 'mr', name: 'Mauritania' },
    { code: 'mu', name: 'Mauricio' },
    { code: 'md', name: 'Moldavia' },
    { code: 'mc', name: 'Mónaco' },
    { code: 'mn', name: 'Mongolia' },
    { code: 'me', name: 'Montenegro' },
    { code: 'ma', name: 'Marruecos' },
    { code: 'mz', name: 'Mozambique' },
    { code: 'mm', name: 'Myanmar' },
    { code: 'na', name: 'Namibia' },
    { code: 'nr', name: 'Nauru' },
    { code: 'np', name: 'Nepal' },
    { code: 'nl', name: 'Países Bajos' },
    { code: 'nz', name: 'Nueva Zelanda' },
    { code: 'ni', name: 'Nicaragua' },
    { code: 'ne', name: 'Níger' },
    { code: 'ng', name: 'Nigeria' },
    { code: 'kp', name: 'Corea del Norte' },
    { code: 'no', name: 'Noruega' },
    { code: 'om', name: 'Omán' },
    { code: 'pk', name: 'Pakistán' },
    { code: 'pw', name: 'Palaos' },
    { code: 'pa', name: 'Panamá' },
    { code: 'pg', name: 'Papúa Nueva Guinea' },
    { code: 'py', name: 'Paraguay' },
    { code: 'pe', name: 'Perú' },
    { code: 'ph', name: 'Filipinas' },
    { code: 'pl', name: 'Polonia' },
    { code: 'pt', name: 'Portugal' },
    { code: 'qa', name: 'Catar' },
    { code: 'ro', name: 'Rumanía' },
    { code: 'ru', name: 'Rusia' },
    { code: 'rw', name: 'Ruanda' },
    { code: 'kn', name: 'San Cristóbal y Nieves' },
    { code: 'lc', name: 'Santa Lucía' },
    { code: 'vc', name: 'San Vicente y las Granadinas' },
    { code: 'ws', name: 'Samoa' },
    { code: 'sm', name: 'San Marino' },
    { code: 'st', name: 'Santo Tomé y Príncipe' },
    { code: 'sa', name: 'Arabia Saudita' },
    { code: 'sn', name: 'Senegal' },
    { code: 'rs', name: 'Serbia' },
    { code: 'sc', name: 'Seychelles' },
    { code: 'sl', name: 'Sierra Leona' },
    { code: 'sg', name: 'Singapur' },
    { code: 'sk', name: 'Eslovaquia' },
    { code: 'si', name: 'Eslovenia' },
    { code: 'sb', name: 'Islas Salomón' },
    { code: 'za', name: 'Sudáfrica' },
    { code: 'kr', name: 'Corea del Sur' },
    { code: 'es', name: 'España' },
    { code: 'lk', name: 'Sri Lanka' },
    { code: 'sd', name: 'Sudán' },
    { code: 'sz', name: 'Suazilandia' },
    { code: 'se', name: 'Suecia' },
    { code: 'ch', name: 'Suiza' },
    { code: 'sy', name: 'Siria' },
    { code: 'tw', name: 'Taiwán' },
    { code: 'tj', name: 'Tayikistán' },
    { code: 'tz', name: 'Tanzania' },
    { code: 'th', name: 'Tailandia' },
    { code: 'tl', name: 'Timor Oriental' },
    { code: 'tg', name: 'Togo' },
    { code: 'to', name: 'Tonga' },
    { code: 'tt', name: 'Trinidad y Tobago' },
    { code: 'tn', name: 'Túnez' },
    { code: 'tr', name: 'Turquía' },
    { code: 'tm', name: 'Turkmenistán' },
    { code: 'tv', name: 'Tuvalu' },
    { code: 'ug', name: 'Uganda' },
    { code: 'ua', name: 'Ucrania' },
    { code: 'ae', name: 'Emiratos Árabes Unidos' },
    { code: 'gb', name: 'Reino Unido' },
    { code: 'uy', name: 'Uruguay' },
    { code: 'uz', name: 'Uzbekistán' },
    { code: 'vu', name: 'Vanuatu' },
    { code: 'va', name: 'Ciudad del Vaticano' },
    { code: 've', name: 'Venezuela' },
    { code: 'vn', name: 'Vietnam' },
    { code: 'ye', name: 'Yemen' },
    { code: 'zm', name: 'Zambia' },
    { code: 'zw', name: 'Zimbabue' },
    { code: 'eh', name: 'Sahara Occidental' },
    { code: 'mp', name: 'Islas Marianas del Norte' },
    { code: 'ps', name: 'Palestina' },
    { code: 'wf', name: 'Wallis y Futuna' },
    { code: 'fo', name: 'Islas Feroe' },
    { code: 'mf', name: 'San Martín' },
    { code: 'ss', name: 'Sudán del Sur' },
];


var ajustes_is_open = false
var SONG_PLAY = true

document.addEventListener('DOMContentLoaded', function () {
    // Obtener todos los elementos con la clase "change"
    var changeElements = document.querySelectorAll('.change');

    // Función que se llama al hacer clic en un elemento con la clase "change"
    function handleChangeClick(e) {
        var id = e.target.id;
        let html = null;

        if (id === 'change_tel') {
            html = `<form action="/cambiar_atributo?to=${encodeURIComponent('tel')}" method='GET'>
                        <input type="hidden" name="csrf_token" value="{{ csrf_token()}}">
                        <label for="change_attr">Nuevo Teléfono: </label>
                        <input type="tel" name='attr' placeholder='Escribe tu nuevo teléfono.' required id='change_attr'>
                        <button type="submit">Ok!</button>
                    </form>`;
        } else if (id === 'change_name') {
            html = `<form action="/cambiar_nombre" method='POST'>
                         <input type="hidden" name="csrf_token" value="{{ csrf_token()}}">
                        <label for="change_attr">Nuevo Nombre: </label>
                        <input type="text" name='attr' placeholder='Escribe tu nuevo nombre.' required id='change_attr' maxlength=40>
                        <button type="submit">Ok!</button>
                    </form>`;
        } else if (id === 'change_mail') {
            html = `<form action="/cambiar_atributo?to=mail" method='GET'>
                         <input type="hidden" name="csrf_token" value="{{ csrf_token()}}">
                        <label for="change_attr">Nuevo Correo: </label>
                        <input type="email" name='attr' placeholder='Escribe tu nuevo correo.' required id='change_attr'>
                        <button type="submit">Ok!</button>
                    </form>`;
        } else if (id === 'change_gender') {
            html = `<form action="/cambiar_atributo?to=Gender" method='GET'>
                         <input type="hidden" name="csrf_token" value="{{ csrf_token()}}">
                        <label for="change_attr">Género: </label>
                        <select name='attr'>
                            <option value="Male">Hombre</option>
                            <option value="Female">Mujer</option>
                            <option value="delete">Borrar</option>
                        </select>
                        <button type="submit">Ok!</button>
                    </form>`;
        } else if (id === 'change_orientation') {
            html = `<form action="/cambiar_atributo?to=OS" method='GET'>
                         <input type="hidden" name="csrf_token" value="{{ csrf_token()}}">
                        <label for="change_attr">Nueva Orientación: </label>
                        <select name='attr'>
                            <option value="Heterosexual">Heterosexual</option>
                            <option value="Homosexual">Homosexual</option>
                            <option value="Bisexual">Bisexual</option>
                            <option value="delete">Borrar</option>
                        </select>
                        <button type="submit">Ok!</button>
                    </form>`;
        } else if (id === 'change_birthday') {
            html = `<form action="/cambiar_atributo?to=birthday" method='GET'>
                        <input type="hidden" name="csrf_token" value="{{ csrf_token()}}">
                        <label for="change_attr">Tu cumpleaños </label>
                        <input type="date" name='attr' required id='change_attr'>
                        <button type="submit">Ok!</button>
                    </form>`;
        } else if (id === 'change_country') {
            // Agregando las opciones de país al formulario
            html = `<form action="/cambiar_atributo?to=country" method='GET'>
                          <input type="hidden" name="csrf_token" value="{{ csrf_token()}}">
                        <label for="change_attr">Región: </label>
                        <select name='attr' id='change_attr'>`;

            // Iterando sobre la lista de países y agregando cada opción al select
            countriesUnique.forEach(country => {
                html += `<option value="${country.code}">${country.name}</option>`;
            });

            // Agregando el resto del código del formulario
            html += `</select>
                        <button type="submit">Ok!</button>
                    </form>`;
        }

        // Actualizando el elemento con id 'console' para mostrar el formulario
        var consola = document.getElementById('console');
        consola.style.display = 'block';
        consola.innerHTML = html;
    }

    // Agregando el evento de clic a todos los elementos con la clase "change"
    changeElements.forEach(function (element) {
        element.addEventListener('click', handleChangeClick);
    });
});

function close_menu(time = 10, res = 10) {
    const computedStyles = window.getComputedStyle(menu_desp_lateral);
    let i = parseInt(computedStyles.width);

    const min_size_change = setInterval(() => {
        i -= res;
        menu_desp_lateral.style.width = i + 'px';

        if (i <= 0) {
            menu_desp_lateral.style.width = '0px';
            menu_desp_lateral.style.display = 'none'
            clearInterval(min_size_change);
        }
    }, time);
}

function minimizeMenu(menu, maxWidth, maxHeight, time = 10, res_x = 20, res_y = 20) {
    const computedStyles = window.getComputedStyle(menu);
    const currentWidth = parseInt(computedStyles.width);
    const currentHeight = parseInt(computedStyles.height);

    let i = currentWidth;
    let j = currentHeight;

    const minimized = setInterval(() => {
        i -= res_x;
        j -= res_y;

        menu.style.width = i - 2 + 'px';
        menu.style.height = j - 2 + 'px';

        if (i <= 0 && j <= 0) {
            menu.style.width = '0px';
            menu.style.height = '0px';
            menu.style.display = 'none';
            clearInterval(minimized);
        }
    }, time);
}

function maximizeMenu(menu, maxWidth, maxHeight, time = 10, res = 20) {
    let i = 0;
    let j = 0;
    const maximized = setInterval(() => {
        i += 20;
        j += 20;

        menu.style.width = i + 'px';
        menu.style.height = j + 'px';

        if (j >= maxHeight || (i >= maxWidth && maxWidth > 0)) {
            menu.style.width = maxWidth + 'px';
            menu.style.height = maxHeight + 'px';
            clearInterval(maximized);
        }
    }, time);
}

function close_profile_menu() {
    profile.style.display = 'none'
}

function open_profile_menu() {
    if (!ajustes_is_open) {
        profile.style.display = 'block'
    }
}

function change_size_menu_lateral() {
    if(!ajustes_is_open) {
        const anchoPagina = window.innerWidth || document.documentElement.clientWidth || document.body.clientWidth;
        menu_desp_lateral.style.display = 'flex'
        let currentMaxWidth = parseInt(window.getComputedStyle(menu_desp_lateral).maxWidth);
        const current_width = (parseInt(window.getComputedStyle(menu_desp_lateral).width));
        const minimized = (current_width >= currentMaxWidth)
        if (currentMaxWidth <= 100) {
            currentMaxWidth = (currentMaxWidth / 100) * anchoPagina
        }

        let i = current_width;
        const change_size = setInterval(() => {
            i = (!minimized) ? i + 15 : i - 15;
            menu_desp_lateral.style.width = (i < 0) ? 0 : i + 'px';

            if (i <= 0 || i >= currentMaxWidth) {
                if (i <= 0) {
                    menu_desp_lateral.style.display = 'none'
                }
                clearInterval(change_size);
            }
        }, 10);
    }
}

exit_profile_menu.addEventListener('click', () => {
    close_profile_menu()
})

profile_menu_open.addEventListener('click', () => {
    open_profile_menu()
})

cerrar_menu_ajustes.addEventListener('click', () => {
    minimizeMenu(menu_ajustes, 769, 0, 5, 20, 25);
    ajustes_is_open = false;
    // Realizar la solicitud fetch
    lang = document.getElementById('lang').value;
    theme = document.getElementById('theme_color').value;
    song_login = document.getElementById('login_song_volume').value;
    song = document.getElementById('login_song_files').value
    song_options = [
        song_login,
        song,
        SONG_PLAY,
    ]
    online_state = document.getElementById('on_line_state').value
    
    hidden_country = document.getElementById('hidden_country').value
    hidden_tel = document.getElementById('hidden_tel').value
    hidden_mail = document.getElementById('hidden_mail').value
    hidden_profile = document.getElementById('hidden_profile').value

    hiddes = [
        hidden_country,
        hidden_mail,
        hidden_profile,
        hidden_tel
    ]
    

    const request_data = {
        'lang': lang,
        'theme': theme,
        'song': song_options,
        'online_state': online_state,
        'hiddes': hiddes

    }

    const csrfToken = document.querySelector('meta[name="csrf-token"]').content;
    fetch('http://127.0.0.1:5000//config_js_endpoint', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'X-CSRFToken': csrfToken,
        },
        body: JSON.stringify(request_data),
    })
    .then(response => response.json())
    .then(data => {

        window.onload = function () {
            window.location.href = data.redirect_url;
        };
    })
    .catch(error => {
        window.onload = function () {
            window.location.href = data.redirect_url;
        };
    });
});

abrir_menu_ajustes.addEventListener('click', () => {
    change_size_menu_lateral();
    menu_ajustes.style.width = '0px';
    menu_ajustes.style.height = '0px';
    menu_ajustes.style.display = 'block';

    const anchoPagina = window.innerWidth || document.documentElement.clientWidth || document.body.clientWidth;
    const currentMaxWidth = parseInt(window.getComputedStyle(menu_ajustes).maxWidth);

    const e = (anchoPagina <= 768) ? 0 : 1;

    maximizeMenu(menu_ajustes, currentMaxWidth, 9999, 10, 20 * e);
    ajustes_is_open = true
});

abrir_menu_btn.addEventListener('click', () => {
    change_size_menu_lateral();
});

cerrar_menu_btn.addEventListener('click', () => {
    change_size_menu_lateral();
});

document.addEventListener('click', (e) => {
    if (e.target.id !== abrir_menu_btn.id && !menu_desp_lateral.contains(e.target) && e.target.className != 'span_button') {
        close_menu(2, 50);
    }

    if (e.target.id !== profile_menu_open.id && !profile.contains(e.target)) {
        close_profile_menu()
    }
});




const stopPanelSong = document.getElementById('stop/play');

stopPanelSong.addEventListener('click', function() {
    SONG_PLAY = (SONG_PLAY) ? false : true
});

