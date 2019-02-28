/**
* automaton.js
*
* Este script contiene la lógica para mostrar el Autómata Celular
* Elemental.
*
* @author Christian Stigen Larsen
* @author Jose Aguilar-Canepa.
*/

/**
* Verifica que la regla introducida se encuentre en el rango válido.
*
* @param {int} rule la regla introducida.
*
* @return {int} la regla introducida, o 0 si no se introdujo un entero,
*   o 255 si se introdujo un numero demasiado grande.
*/
function check(rule) {
    if(isNaN(rule) || rule < 0) rule = 0;
    if(rule > 255) rule = 255;

    $('#rule').val(rule);
    $('#num').html(' = ' + rule);

    return rule;
}

/**
* Limpia el área del canvas con el color indicado.
*/
function clear(image, color) {
    for(var p = 0; p < image.data.length; ++p)
        image.data[p] = color;
}

/**
* Dibuja el autómata celular en el canvas.
*
* @param {array of int} rules la regla a dibujar.
*/
function draw(rules) {
    var canvas = document.getElementById('automaton-canvas');
    var context = canvas.getContext('2d');
    var i = context.getImageData(0, 0, canvas.width, canvas.height);

    clear(i, 255);

    var w4 = canvas.width << 2;
    var line = 0;

    i.data[0 + w4 >> 1] = i.data[1 + w4 >> 1] = i.data[2 + w4 >> 1] = 0;

    for(var x = 0; x < (i.data.length - w4); x += 4, line += 4) {
        var left = !(i.data[x - 4] & 0x1);
        var right = !(i.data[x + 4] & 0x1);

        // Manejamos los saltos de linea
        if(line == 0) { 
            left = 0; }
        else if (line == w4) {
            right = line = 0;
            continue;
        }

        i.data[x + w4 + 0] = 
        i.data[x + w4 + 1] = 
        i.data[x + w4 + 2] =
        rules[left << 2 | !(i.data[x] & 0x1) << 1 | right];
    }

    context.putImageData(i, 0, 0);
}

/**
* Genera el autómata celular para la regla indicada.
*
* @param {float} rule la regla a generar.
*/
function generate(rule) {
    draw(genRules(check(rule)));
}

function genRules(rule) {
    var rules=[0,0,0,0,0,0,0,0];

    for(var i = 0; i < rules.length; ++i) {
        // Almacena el valor para usarlo en el canvas.
        rules[i] = rule & (0x1<<i) ? 0 : 255;

        $('#p' + i).html(rules[i] ? '0' : '1');
    }

    return rules;
}

/** 
* Inicializa los elementos de la interfaz de usuario.
*/
function init() {
    $('#gen-btn').click(function() {
        generate($('#rule-txt').val());
    });

    $('#width-min').click(function() {
        document.getElementById('automaton-canvas').width /= 2;
        generate($('#rule-txt').val());
    });

    $('#width-plus').click(function() {
        document.getElementById('automaton-canvas').width *= 2;
        generate($('#rule-txt').val());
    });

    $('#height-min').click(function() {
        document.getElementById('automaton-canvas').height /= 2;
        generate($('#rule-txt').val());
    });

    $('#height-plus').click(function() {
        document.getElementById('automaton-canvas').height *= 2;
        generate($('#rule-txt').val());
    });

    generate($('#rule-txt').val());
}