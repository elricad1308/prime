/** La lista con las posiciones actuales de cada peatón. */
var currentPositions = [];

/** La cantidad de pasos que un peatón da antes de salirse del mapa. */
var BOUNDS = 30;

/** Cantidad de grados que hay que girar para mirar al Norte. */
var DIR_NORTH = 90;

/** Cantidad de grados que hay que girar para mirar al Noreste. */
var DIR_NORTHEAST = 45;

/** Cantidad de grados que hay que girar para mirar al Este. */
var DIR_EAST = 0;

/** Cantidad de grados que hay que girar para mirar al Sureste. */
var DIR_SOUTHEAST = 315;

/** Cantidad de grados que hay que girar para mirar al Sur. */
var DIR_SOUTH = 270;

/** Cantidad de grados que hay que girar para mirar al Suroeste. */
var DIR_SOUTHWEST = 225;

/** Cantidad de grados que hay que girar para mirar al Oeste. */
var DIR_WEST = 180;

/** Cantidad de grados que hay que girar para mirar al Noroeste. */
var DIR_NORTHWEST = 135;

/** La altura (en pixeles) del canvas. */
var HEIGHT = 184;

/** La probabilidad que un peatón tenga prisa. */
var HURRY_PROB = 0.2;

/** La lista con todos los pasos que los peatones darán a continuación. */
var nextSteps = []

/** La cantidad de peatones que estarán en la simulación. */
var NUM_PEDESTRIANS = 25;

/** La lista con todos los peatones de la simulación. */
var pedestrians = [];

/** El tamaño (en pixeles) de las cuadrículas del canvas. */
var STEP_SIZE = 8;

/** La anchura (en pixeles) del canvas. */
var WIDTH = 240;

/** La referencia al canvas de la página. */
var canvas = document.getElementById('pedestrian');

/** La referencia al contexto del canvas. */
var context = canvas.getContext('2d');

/**
* Convierte grados a radianes.
*
* @param {float} degrees los grados.
*
* @returns {float} el equivalente en radianes de los grados.
*/
Math.radians = function(degrees) {
  return degrees * Math.PI / 180.0;
}

/**
* Convierte radianes a grados.
*
* @param {float} radians los radianes.
*
* @return {float} el equivalente en grados de los radianes.
*/
Math.degrees = function(radians) {
  return radians * 180.0 / Math.PI;
}

/**
* Obtiene el objeto utilizado para realizar las animaciones en el
* canvas
*/
window.requestAnimFrame = (function(callback) {
    return window.requestAnimationFrame 
      || window.webkitRequestAnimationFrame || window.mozRequestAnimationFrame 
      || window.oRequestAnimationFrame || window.msRequestAnimationFrame ||
      function(callback) {
        window.setTimeout(callback, 1000/60);
      }
})();

init();
drawQuads();

/**
 * Inicializa la simulación.
 * 
 * @returns {void} nada. 
 */
function init() {    
    // Inicializa las posiciones actuales y los pasos siguientes
    for(var i = 0; i < NUM_PEDESTRIANS; i++) {
        currentPositions.push(new Point(-100, -100));
        nextSteps.push(new Point(-100, -100));
    }

    // Crea a los peatones de la simulación
    for(var i = 0; i < NUM_PEDESTRIANS; i++) {
        var p = new Pedestrian(i);
        p.init();
        p.render();
        pedestrians.push(p);
    }

    // Dibuja la acera
    drawQuads();

    // Agrega el evento de cambio de tamaño
    $(window).resize(redraw);

    // Dibuja el canvas en el tamaño adecuado
    redraw();

    // Espera 5 segundos para iniciar la simulación
    setTimeout(animate, 5000);
}

function animate() {
    context.clearRect(0, 0, WIDTH, HEIGHT);
    drawQuads();

    for(var i = 0; i < NUM_PEDESTRIANS; i++) {
        pedestrians[i].updatePosition();
        pedestrians[i].render();
    }
    
    requestAnimFrame(function() {
        animate();
    });
}

/**
 * Determina si el punto proporcionado está siendo utilizado por otros
 * peatones en la simulación.
 * 
 * @param {int} pedId el ID del peatón que realiza la comprobación.
 * @param {Point} el punto que se desea comprobar.
 *
 * @returns {boolean} 'true' sí y solamente sí ningún peatón se 
 * encuentra en el punto indicado y ningún peatón ha expresado su
 * deseo de moverse a dicho punto. 'false' en caso contrario.
 */
function isAvailable(pedId, point) {
    var available = true;
    
    for(var i = 0; i < NUM_PEDESTRIANS; i++) {
        if(i != pedId) {
            available = (available && !currentPositions[i].equals(point));
            available = (available && !nextSteps[i].equals(point));
        }
            
        if(!available)
            return available;
    }
    
    return available;
}

/**
* Dibuja la cuadrícula del canvas.
*
* @return {void} nada.
*/
function drawQuads() {
    /*
    context.beginPath();
    context.strokeStyle = "black";

    // Dibuja las líneas verticales
    for(var i = 0; i <= WIDTH; i += STEP_SIZE) {
        context.moveTo(i, 0);
        context.lineTo(i, HEIGHT);
    }

    // Dibuja las líneas horizontales.
    for(var i = 0; i <= HEIGHT; i += STEP_SIZE) {
        context.moveTo(0, i);
        context.lineTo(WIDTH, i);
    }

    context.stroke();
    context.closePath();*/

    context.fillStyle = "slategray";
    context.fillRect(0, 0, WIDTH, HEIGHT);

    // Dibuja el paso peatonal.
    context.fillStyle = "gold";
    for(var i = 0; i <= WIDTH / STEP_SIZE; i++) {
        context.fillRect((STEP_SIZE * i) + (STEP_SIZE / 2) - (STEP_SIZE / 4), STEP_SIZE * 3, (STEP_SIZE / 2), HEIGHT - (STEP_SIZE * 6));
    }

    // Dibuja las aceras.
    context.fillStyle = "darkgray";
    context.strokeStyle = "dimgray";

    context.fillRect(0, 0, STEP_SIZE, HEIGHT);
    context.strokeRect(0, 0, STEP_SIZE, HEIGHT);

    context.fillRect(WIDTH - STEP_SIZE, 0, STEP_SIZE, HEIGHT);
    context.strokeRect(WIDTH - STEP_SIZE, 0, STEP_SIZE, HEIGHT);

    // Dibuja las líneas de la carretera.
    context.fillStyle = "yellow";
    context.fillRect((WIDTH / 2) - (STEP_SIZE / 8), 0, (STEP_SIZE / 4), STEP_SIZE * 2);
    context.fillRect((WIDTH / 2) - (STEP_SIZE / 8), (HEIGHT - (2 * STEP_SIZE)), (STEP_SIZE / 4), STEP_SIZE * 2);

    context.fillStyle = "white";
    context.fillRect((WIDTH / 4) - (STEP_SIZE / 8), STEP_SIZE, (STEP_SIZE / 8), STEP_SIZE);
    context.fillRect((3 * (WIDTH / 4)) - (STEP_SIZE / 8), STEP_SIZE, (STEP_SIZE / 8), STEP_SIZE);
    context.fillRect((WIDTH / 4) - (STEP_SIZE / 8), HEIGHT - (2 * STEP_SIZE), (STEP_SIZE / 8), STEP_SIZE);
    context.fillRect((3 * (WIDTH / 4)) - (STEP_SIZE / 8), HEIGHT - (2 * STEP_SIZE), (STEP_SIZE / 8), STEP_SIZE);
}

function redraw() {
    var tempHeight;
    var tempStepSize;
    var tempWidth;
    var winWidth = window.innerWidth;

    if(winWidth > 900) {
        tempHeight = 600;
        tempStepSize = 40;
        tempWidth = 800;
    } else if(winWidth > 550) {
        tempHeight = 368;
        tempStepSize = 16;
        tempWidth = 480;
    } else {
        tempHeight = 184;
        tempStepSize = 8;
        tempWidth = 240;
    }

    if(tempWidth != WIDTH) {
        var ctx = document.getElementById('pedestrian').getContext('2d');
        HEIGHT = tempHeight;
        STEP_SIZE = tempStepSize;
        WIDTH = tempWidth;
        ctx.canvas.height = HEIGHT;
        ctx.canvas.width = WIDTH;
        drawQuads();
    }
}

/**
* Crea un nuevo objeto Pedestrian. Cada objeto en el canvas es una
* instancia de esta clase.
* 
* @param {int} id el identificador único del peatón.
*
* @returns {Pedestrian} un objeto Pedestrian.
*/
function Pedestrian(pid) {
    /** El ángulo real del peatón. Es el que se usa en el canvas. */
    this.angle = 0;
    
    /** La dirección hacia la que se dirige el peatón. */
    this.direction = 0;
    
    /** Determina si el peatón tiene prisa o no. */
    this.hurry = false;

    /** El identificador único del peatón. */
    this.id = pid;
    
    /** El siguiente objetivo del peatón. */
    this.nextStep = new Point(0, 0);
    
    /** La posición real del peatón. Es la que se usa en el canvas. */
    this.position = new Point(0, 0);
    
    /** 
     * La cantidad de pasos horizontales que el peatón ha dado hacia
     * su siguiente objetivo. */
    this.stepsh = 0;
    
    /**
     * La cantidad de pasos verticales que el peatón ha dado hacia su
     * siguiente objetivo. 
     */
    this.stepsv = 0;
    
    /**
     * El destino final del peatón. 
     */
    this.target = new Point(0, 0);
    
    /** El ángulo al que el peatón debe girar para llegar a su
     * siguiente objetivo.
     */
    this.targetAngle = 0;
    
    /**
     * Calcula el siguiente paso que el peatón dará. El peatón siempre
     * buscará que su siguiente paso lo acerque a su objetivo final,
     * cuidando no chocar con otros peatones en el camino.
     * 
     * @returns {void} nada.
     */
    this.computeNextStep = function() {
        // La dirección del peatón determina su trayectoria.
        switch(this.direction) {
            // El peatón se dirige al NORTE.
            case DIR_NORTH :
                if(this.position.x != this.target.x) {
                    if(this.position.x < this.target.x)
                        this.nextStep.x = this.position.x + 1;
                    else 
                        this.nextStep.x = this.position.x - 1;
                }
                
                if(this.position.y != this.target.y) 
                    this.nextStep.y = this.position.y - 1;

                break;
                
            // El peatón se dirige al NORESTE.
            case DIR_NORTHEAST :
                if(this.position.x != this.target.x)
                    this.nextStep.x = this.position.x + 1;
                    
                if(this.position.y != this.target.y)
                    this.nextStep.y = this.position.y - 1;
                
                break;
                
            // El peatón se dirige al ESTE.
            case DIR_EAST :
                if(this.position.y != this.target.y) {
                    if(this.position.y < this.target.y)
                        this.nextStep.y = this.position.y + 1;
                    else
                        this.nextStep.y = this.position.y - 1;
                }
                
                if(this.position.x != this.target.x) 
                    this.nextStep.x = this.position.x + 1;

                break;
                
            // El peatón se dirige al SURESTE.
            case DIR_SOUTHEAST :
                if(this.position.x != this.target.x) 
                    this.nextStep.x = this.position.x + 1;
                    
                if(this.position.y != this.target.y)
                    this.nextStep.y = this.position.y + 1;
                
                break;
                
            // El peatón se dirige al SUR.
            case DIR_SOUTH :
                if(this.position.x != this.target.x) {
                    if(this.position.x < this.target.x) 
                        this.nextStep.x = this.position.x + 1;
                    else 
                        this.nextStep.x = this.position.x - 1;                    
                }
                
                if(this.position.y != this.target.y)
                    this.nextStep.y = this.position.y + 1;
                
                break;
                
            // El peatón se dirige al SUROESTE.
            case DIR_SOUTHWEST :
                if(this.position.x != this.target.x) 
                    this.nextStep.x = this.position.x - 1;
                    
                if(this.position.y != this.target.y)
                    this.nextStep.y = this.position.y + 1;

                break;
                
            // El peatón se dirige al OESTE.
            case DIR_WEST :
                if(this.position.y != this.target.y) {
                    if(this.position.y < this.target.y)
                        this.nextStep.y = this.position.y + 1;
                    else
                        this.nextStep.y = this.position.y - 1;
                }
                
                if(this.position.x != this.target.x) 
                    this.nextStep.x = this.position.x - 1;
                
                break;
                
            // El peatón se dirige al NOROESTE.
            case DIR_NORTHWEST:
                if(this.position.x != this.target.x)
                    this.nextStep.x = this.position.x - 1;
                    
                if(this.position.y != this.target.y)
                    this.nextStep.y = this.position.y - 1;
                
                break;
        }
        
        // Registra la siguiente posicion del peatón.
        nextSteps[this.id].x = this.nextStep.x;
        nextSteps[this.id].y = this.nextStep.y;
        
        // Gira al peatón hacia el siguiente paso.
        this.steer(this.nextStep);
    }

    /**
    * Modifica el siguiente paso del peatón para evitar que colisione con otros
    * peatones.
    */
    this.detour = function() {
        // La desviación depende de la dirección en la que se moverá el peatón
        switch(this.targetAngle) {
            // Desviación si el peatón va hacia el NORTE.
            case DIR_NORTH:
            if(!isAvailable(this.id, this.nextStep)) {
                this.nextStep.x++;
                if(!isAvailable(this.id, this.nextStep)) {
                    this.nextStep.x -= 2;
                    if(!isAvailable(this.id, this.nextStep)) {
                        this.nextStep.x += 2;
                        this.nextStep.y++;
                        if(!isAvailable(this.id, this.nextStep)) {
                            this.nextStep.x -= 2;
                            if(!isAvailable(this.id, this.nextStep)) {
                                this.nextStep.x += 2;
                                this.nextStep.y++;
                                if(!isAvailable(this.id, this.nextStep)) {
                                    this.nextStep.x--;
                                    if(!isAvailable(this.id, this.nextStep)) {
                                        this.nextStep.x--;
                                        if(!isAvailable(this.id, this.nextStep)) {
                                            this.nextStep.x = this.position.x;
                                            this.nextStep.y = this.position.y;
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }

            break;

            // Desviación si el peatón va al NORESTE.
            case DIR_NORTHEAST:
            if(!isAvailable(this.id, this.nextStep)) {
                this.nextStep.y++;
                if(!isAvailable(this.id, this.nextStep)) {
                    this.nextStep.y--;
                    this.nextStep.x--;
                    if(!isAvailable(this.id, this.nextStep)) {
                        this.nextStep.y += 2;
                        this.nextStep.x++;
                        if(!isAvailable(this.id, this.nextStep)) {
                            this.nextStep.y -= 2;
                            this.nextStep.x -= 2;
                            if(!isAvailable(this.id, this.nextStep)) {
                                this.nextStep.y += 2;
                                this.nextStep.x++;
                                if(!isAvailable(this.id, this.nextStep)) {
                                    this.nextStep.x--;
                                    if(!isAvailable(this.id, this.nextStep)) {
                                        this.nextStep.y--;
                                        if(!isAvailable(this.id, this.nextStep)) {
                                            this.nextStep.x = this.position.x;
                                            this.nextStep.y = this.position.y;
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }

            break;

            // Desviación si el peatón va al ESTE.
            case DIR_EAST:
            if(!isAvailable(this.id, this.nextStep)) {
                this.nextStep.y++;
                if(!isAvailable(this.id, this.nextStep)) {
                    this.nextStep.y -=2;
                    if(!isAvailable(this.id, this.nextStep)) {
                        this.nextStep.x--;
                        this.nextStep.y += 2;
                        if(!isAvailable(this.id, this.nextStep)) {
                            this.nextStep.y -= 2;
                            if(!isAvailable(this.id, this.nextStep)) {
                                this.nextStep.x--;
                                this.nextStep.y += 2;
                                if(!isAvailable(this.id, this.nextStep)) {
                                    this.nextStep.y--;
                                    if(!isAvailable(this.id, this.nextStep)) {
                                        this.nextStep.y--;
                                        if(!isAvailable(this.id, this.nextStep)) {
                                            this.nextStep.x = this.position.x;
                                            this.nextStep.y = this.position.y;
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }

            break;

            // Desviación si el peatón va al SURESTE.
            case DIR_SOUTHEAST:
            if(!isAvailable(this.id, this.nextStep)) {
                this.nextStep.x--;
                if(!isAvailable(this.id, this.nextStep)) {
                    this.nextStep.x++;
                    this.nextStep.y--;
                    if(!isAvailable(this.id, this.nextStep)) {
                        this.nextStep.y++;
                        this.nextStep.x -= 2;
                        if(!isAvailable(this.id, this.nextStep)) {
                            this.nextStep.x += 2;
                            this.nextStep.y -= 2;
                            if(!isAvailable(this.id, this.nextStep)) {
                                this.nextStep.y++;
                                this.nextStep.x -= 2;
                                if(!isAvailable(this.id, this.nextStep)) {
                                    this.nextStep.x++;
                                    this.nextStep.y--;
                                    if(!isAvailable(this.id, this.nextStep)) {
                                        this.nextStep.x--;
                                        if(!isAvailable(this.id, this.nextStep)) {
                                            this.nextStep.x = this.position.x;
                                            this.nextStep.y = this.position.y;
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }

            break;

            // Desviación si el peatón va al SUR.
            case DIR_SOUTH:
            if(!isAvailable(this.id, this.nextStep)) {
                this.nextStep.x--;
                if(!isAvailable(this.id, this.nextStep)) {
                    this.nextStep.x += 2;
                    if(!isAvailable(this.id, this.nextStep)) {
                        this.nextStep.y--;
                        this.nextStep.x -= 2;
                        if(!isAvailable(this.id, this.nextStep)) {
                            this.nextStep.x += 2;
                            if(!isAvailable(this.id, this.nextStep)) {
                                this.nextStep.y--;
                                this.nextStep.x -= 2;
                                if(!isAvailable(this.id, this.nextStep)) {
                                    this.nextStep.x++;
                                    if(!isAvailable(this.id, this.nextStep)) {
                                        this.nextStep.x++;
                                        if(!isAvailable(this.id, this.nextStep)) {
                                            this.nextStep.x = this.position.x;
                                            this.nextStep.y = this.position.y;
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }

            break;

            // Desviación si el peatón va al SUROESTE.
            case DIR_SOUTHWEST:
            if(!isAvailable(this.id, this.nextStep)) {
                this.nextStep.x++;
                if(!isAvailable(this.id, this.nextStep)) {
                    this.nextStep.y--;
                    this.nextStep.x--;
                    if(!isAvailable(this.id, this.nextStep)) {
                        this.nextStep.x += 2;
                        this.nextStep.y++;
                        if(!isAvailable(this.id, this.nextStep)) {
                            this.nextStep.x -= 2;
                            this.nextStep.y -= 2;
                            if(!isAvailable(this.id, this.nextStep)) {
                                this.nextStep.x += 2;
                                this.nextStep.y++;
                                if(!isAvailable(this.id, this.nextStep)) {
                                    this.nextStep.x--;
                                    this.nextStep.y--;
                                    if(!isAvailable(this.id, this.nextStep)) {
                                        this.nextStep.x++;
                                        if(!isAvailable(this.id, this.nextStep)) {
                                            this.nextStep.x = this.position.x;
                                            this.nextStep.y = this.position.y;
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }

            break;

            // Desviación si el peatón va al OESTE.
            case DIR_WEST:
            if(!isAvailable(this.id, this.nextStep)) {
                this.nextStep.y++;
                if(!isAvailable(this.id, this.nextStep)) {
                    this.nextStep.y -= 2;
                    if(!isAvailable(this.id, this.nextStep)) {
                        this.nextStep.x++;
                        this.nextStep.y += 2;
                        if(!isAvailable(this.id, this.nextStep)) {
                            this.nextStep.y -= 2;
                            if(!isAvailable(this.id, this.nextStep)) {
                                this.nextStep.x++;
                                this.nextStep.y += 2;
                                if(!isAvailable(this.id, this.nextStep)) {
                                    this.nextStep.y--;
                                    if(!isAvailable(this.id, this.nextStep)) {
                                        this.nextStep.y--;
                                        if(!isAvailable(this.id, this.nextStep)) {
                                            this.nextStep.x = this.position.x;
                                            this.nextStep.y = this.position.y;
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }

            break;

            // Desviación si el peatón va al NOROESTE.
            case DIR_NORTHWEST:
            if(!isAvailable(this.id, this.nextStep)) {
                this.nextStep.x++;
                if(!isAvailable(this.id, this.nextStep)) {
                    this.nextStep.x--;
                    this.nextStep.y++;
                    if(!isAvailable(this.id, this.nextStep)) {
                        this.nextStep.x += 2;
                        this.nextStep.y--;
                        if(!isAvailable(this.id, this.nextStep)) {
                            this.nextStep.x -= 2;
                            this.nextStep.y += 2;
                            if(!isAvailable(this.id, this.nextStep)) {
                                this.nextStep.x += 2;
                                this.nextStep.y--;
                                if(!isAvailable(this.id, this.nextStep)) {
                                    this.nextStep.y++;
                                    this.nextStep.x--;
                                    if(!isAvailable(this.id, this.nextStep)) {
                                        this.nextStep.x++;
                                        if(!isAvailable(this.id, this.nextStep)) {
                                            this.nextStep.x = this.position.x;
                                            this.nextStep.y = this.position.y;
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }

            break;
        }

        // Actualiza el siguiente paso del peatón
        nextSteps[this.id].x = this.nextStep.x;
        nextSteps[this.id].y = this.nextStep.y;
    }

    /**
    * Asigna al peatón una posición inicial aleatoria, y una posición
    * de destino apropiada para la misma.
    *
    * @returns {void} nada.
    */
    this.init = function() {
        // Determina si el peaton tiene prisa o no.
        this.hurry = (Math.random() < HURRY_PROB);

        // Determina si el peatón entrará horizontal o verticalmente.
        if(Math.random() < 0.5) {
            // El peatón entrará por el OESTE...
            if(Math.random() < 0.5) {
                this.position.x = -1;
                this.position.y = Math.floor(Math.random() * ((HEIGHT / STEP_SIZE) - 1));
                this.angle = DIR_EAST;

                // ...y saldrá por el ESTE.
                if(Math.random() < 0.5) {
                    this.target.x = WIDTH / STEP_SIZE;
                    this.target.y = Math.floor(Math.random() * ((HEIGHT / STEP_SIZE) - 1));
                    this.direction = DIR_EAST;
                } else {
                    // ...y saldrá por el NORTE.
                    if(Math.random() < 0.5) {
                        this.target.y = -1;
                        this.target.x = Math.floor(Math.random() * ((WIDTH / STEP_SIZE) - 1));
                        this.direction = DIR_NORTHEAST;
                    }
                    // ...y saldrá por el SUR. 
                    else {
                        this.target.y = HEIGHT / STEP_SIZE;
                        this.target.x = Math.floor(Math.random() * ((WIDTH / STEP_SIZE) - 1));
                        this.direction = DIR_SOUTHEAST;
                    }
                }
            } 
            // El peatón entrará por el ESTE...
            else {
                this.position.x = WIDTH / STEP_SIZE;
                this.position.y = Math.floor(Math.random() * ((HEIGHT / STEP_SIZE) - 1));
                this.angle = DIR_WEST;

                // ...y saldrá por el OESTE.
                if(Math.random() < 0.5) {
                    this.target.x = -1;
                    this.target.y = Math.floor(Math.random() * ((HEIGHT / STEP_SIZE) - 1));
                    this.direction = DIR_WEST;
                } else {
                    // ...y saldrá por el NORTE.
                    if(Math.random() < 0.5) {
                        this.target.y = -1;
                        this.target.x = Math.floor(Math.random() * ((WIDTH / STEP_SIZE) - 1));
                        this.direction = DIR_NORTHWEST;
                    }
                    // ...y saldrá por el SUR. 
                    else {
                        this.target.y = HEIGHT / STEP_SIZE;
                        this.target.x = Math.floor(Math.random() * ((WIDTH / STEP_SIZE) - 1));
                        this.direction = DIR_SOUTHWEST;
                    }
                }
            }
        } else {
            // El peatón entrará por el NORTE...
            if(Math.random() < 0.5) {
                this.position.y = -1;
                this.position.x = Math.floor(Math.random() * ((WIDTH / STEP_SIZE) - 1));
                this.angle = DIR_SOUTH;

                // ...y saldrá por SUR.
                if(Math.random() < 0.5) {
                    this.target.y = HEIGHT / STEP_SIZE;
                    this.target.x = Math.floor(Math.random() * ((WIDTH / STEP_SIZE) - 1));
                    this.direction = DIR_SOUTH;
                } else {
                    // ...y saldrá por el ESTE.
                    if(Math.random() < 0.5) {
                        this.target.x = WIDTH / STEP_SIZE;
                        this.target.y = Math.floor(Math.random() * ((HEIGHT / STEP_SIZE) - 1));
                        this.direction = DIR_SOUTHEAST;
                    }
                    // ...y saldrá por el OESTE.
                    else {
                        this.target.x= -1;
                        this.target.y = Math.floor(Math.random() * ((HEIGHT / STEP_SIZE) - 1));
                        this.direction = DIR_SOUTHWEST;
                    }
                }
            }
            // El peatón entrará por el SUR...
            else {
                this.position.y = HEIGHT / STEP_SIZE;
                this.position.x = Math.floor(Math.random() * ((WIDTH / STEP_SIZE) - 1));
                this.angle = DIR_NORTH;

                // ...y saldrá por el NORTE.
                if(Math.random() < 0.5) {
                    this.target.y = -1;
                    this.target.x = Math.floor(Math.random() * ((WIDTH / STEP_SIZE) - 1));
                    this.direction = DIR_NORTH;
                } else {
                    // ...y saldrá por el ESTE.
                    if(Math.random() < 0.5) {
                        this.target.x = WIDTH / STEP_SIZE;
                        this.target.y = Math.floor(Math.random() * ((HEIGHT / STEP_SIZE) - 1));
                        this.direction = DIR_NORTHEAST;
                    }
                    // ...y saldrá por el OESTE. 
                    else {
                        this.target.x = -1;
                        this.target.y = Math.floor(Math.random() * ((HEIGHT / STEP_SIZE) - 1));
                        this.direction = DIR_NORTHWEST;
                    }
                }
            }
        }
        
        // Calcula el siguiente paso a dar
        this.computeNextStep();
    }

    /**
    * Dibuja al peatón en el canvas.
    *
    * @returns {void} nada.
    */
    this.render = function() {
        /* Dibuja el "campo de vista" del peatón
        context.fillStyle = "green";
        context.fillRect(this.nextStep.x * STEP_SIZE, this.nextStep.y * STEP_SIZE, STEP_SIZE, STEP_SIZE);
        context.strokeRect(this.nextStep.x * STEP_SIZE, this.nextStep.y * STEP_SIZE, STEP_SIZE, STEP_SIZE);
        */
        // Dibuja el 'cuerpo' del peatón.
        context.beginPath();
        context.strokeStyle = 'black';
        context.fillStyle = 'red';
        context.arc(
          (this.position.x * STEP_SIZE) + (STEP_SIZE / 2) + this.stepsh, // Coordenada X del centro del peatón
          (this.position.y * STEP_SIZE) + (STEP_SIZE / 2) + this.stepsv, // Coordenada Y del centro del peatón
          STEP_SIZE / 4,                                                 // Radio del peatón
          0,                                                             // Ángulo inicial
          Math.PI * 2                                                    // Ángulo final
        );
        context.fill();
        context.stroke();
        context.closePath();

        // Dibuja la 'cara' del peatón.
        context.save();    
        context.translate((this.position.x * STEP_SIZE) + (STEP_SIZE / 2) + this.stepsh, (this.position.y * STEP_SIZE) + (STEP_SIZE / 2) + this.stepsv);    
        context.rotate(-Math.radians(this.angle));

        context.beginPath();
        context.moveTo(STEP_SIZE / 8, 3*(STEP_SIZE / 8));
        context.lineTo(3 * (STEP_SIZE / 8), 0);
        context.lineTo(STEP_SIZE / 8, -3*(STEP_SIZE / 8));
        context.lineWidth = 2;
        context.stroke();
        context.closePath();

        context.restore();
        
        
    }

    /**
     * Modifica el ángulo objetivo del peatón para que apunte hacia el
     * punto indicado.
     * 
     * @param {Point} opoint el punto hacia el cual se desea que gire
     *  el peatón.
     */
    this.steer = function(opoint) {
        this.targetAngle = this.position.steerTo(opoint);

        if(this.targetAngle == -1)
            this.targetAngle = this.angle;
    }

    /**
     * Actualiza la posición del peatón. Este método modifica el ángulo
     * del peatón para girar a su objetivo, y modifica su posición en
     * x e y para que lo alcance.
     * 
     * @returns {void} nada.
     */
    this.updatePosition = function() {
        // Verificamos si hemos alcanzado nuestro destino
        if(this.position.equals(this.target)) {
            // Un peatón que alcanza su objetivo sale del canvas
            this.init();

            return;
        }
        
        // El peatón primero debe orientarse.
        if(this.targetAngle != this.angle) {
            if(this.targetAngle > this.angle) {
                if((this.targetAngle - this.angle) < (this.angle + 360 - this.targetAngle)) {
                    if(this.hurry)
                        this.angle += 15;
                    else
                        this.angle += 5;
                } else {
                    if(this.hurry)
                        this.angle -= 15;
                    else
                        this.angle -= 5;
                }
            } else {
                if((this.angle - this.targetAngle) < (this.targetAngle + 360 - this.angle)) {
                    if(this.hurry)
                        this.angle -= 15;
                    else
                        this.angle -= 5;
                } else {
                    if(this.hurry)
                        this.angle += 15;
                    else
                        this.angle += 5;
                }
            }
            
            // Evita los angulos negativos
            if(this.angle < 0) this.angle = 360 + this.angle;
            
            // Evita los ángulos mayores a 360
            if(this.angle > 360) this.angle = this.angle % 360;
        } 
        // Si está orientado, entonces avanza.
        else if(!this.position.equals(this.nextStep)){
            // Mueve al peatón horizontalmente...
            if(this.position.x != this.nextStep.x) {
                if(this.position.x < this.nextStep.x) {
                    if(this.hurry)
                        this.stepsh += 2;
                    else
                        this.stepsh++;
                } else {
                    if(this.hurry)
                        this.stepsh -= 2;
                    else
                        this.stepsh--;
                }
            } 
            
            // ...y luego verticalmente.
            if(this.position.y != this.nextStep.y) {
                if(this.position.y < this.nextStep.y) {
                    if(this.hurry)
                        this.stepsv += 2;
                    else
                        this.stepsv++;
                } else {
                    if(this.hurry)
                        this.stepsv -= 2;
                    else
                        this.stepsv--;
                }
            }
            // Verificamos si el peatón ya avanzó un paso completo.
            if(this.stepsh == STEP_SIZE) {
                this.position.x++;
                this.stepsh = 0;
            }
            
            if(this.stepsh == -STEP_SIZE) {
                this.position.x--;
                this.stepsh = 0;
            }
            
            if(this.stepsv == STEP_SIZE) {
                this.position.y++;
                this.stepsv = 0;
            }
            
            if(this.stepsv == -STEP_SIZE) {
                this.position.y--;
                this.stepsv = 0;
            }
        }
        // Si el peaton llega a su meta local, se propone una nueva. 
        else {
            currentPositions[this.id].x = this.position.x;
            currentPositions[this.id].y = this.position.y;
            this.computeNextStep();
            this.detour();
        }

        // Finalmente, si el peatón se sale de los límites, lo reiniciamos.
        if(this.position.isOutOfBounds())
            this.init();
    }
}

/**
* Crea un nuevo objeto Point. Esta clase es utilizada por los
* objetos que se dibujan en el canvas para determinar su posición.
*
* @param {int} px la coordenada en X del Point.
* @param {int} py la coordenada en Y del Point.
*
* @returns {Point} un objeto Point.
*/
function Point(px, py) {
    this.x = px;
    this.y = py;

    /**
    * Determina si dos puntos tienen las mismas coordenadas, es decir,
    * comprueba si dos puntos son iguales.
    *
    * @param {Point} opoint el punto a comprobar.
    *
    * @returns {boolean} 'true' sí y solamente sí el objeto 'opoint' es
    *   una instancia de Point con los mismos componentes X y Y que
    *   este Point. 'false' si alguno de los dos componentes X o Y de
    *   'opoint' es diferente, o si 'opoint' no es un Point.
    */
    this.equals = function(opoint) {
        return (this.x === opoint.x) && (this.y === opoint.y);
    }

    /** 
    * Determina si el punto está fuera de los límites del canvas.
    *
    * @returns {boolean} 'true' si alguno de los componentes del punto
    *   sale de los límites establecidos del mapa.
    */
    this.isOutOfBounds = function() {
        return (Math.abs(this.x) > BOUNDS) || (Math.abs(this.y) > BOUNDS);
    }

    /**
    * Calcula el ángulo de rotación entre dos puntos. Dada la
    * teselación cuadrada del espacio de simulación, solo existen
    * ocho posibles ángulos de rotación (0, 45, 90, 135, 180, 225, 270
    * y 315 grados), que corresponde al ángulo que un peatón debe girar
    * para llegar hasta el punto 'opoint'. Si ambos puntos son iguales,
    * el peatón debe quedarse en su lugar, por lo que este método
    * regresa un número negativo.
    *
    * @param {Point} opoint el punto de destino.
    *
    * @returns {int} el ángulo de rotación entre los dos puntos (un
    * número entre 0 y 315 inclusive); o -1 si ambos puntos son 
    * iguales.
    */
    this.steerTo = function(opoint) {
        if(this.equals(opoint))
            return -1;

        // Los puntos están en el mismo valor de x
        if(this.x == opoint.x) {
            if(this.y > opoint.y)
                return DIR_NORTH;
            else
                return DIR_SOUTH;
        } // Los puntos están en el mismo valor de y
        else if(this.y == opoint.y) {
            if(this.x > opoint.x) 
                return DIR_WEST;
            else
                return DIR_EAST;
        }  // Los puntos son completamente diferentes
        else {
            if(this.x > opoint.x) {
                if(this.y > opoint.y)
                    return DIR_NORTHWEST;
                else 
                    return DIR_SOUTHWEST;
            } else {
                if(this.y > opoint.y)
                    return DIR_NORTHEAST;
                else
                    return DIR_SOUTHEAST;
            }
        }
    
        // Por algún motivo llegamos hasta aquí
        return -1;
    }
    
    /**
     * Crea una representación en cadena de este Punto, mostrando los
     * componentes x e y del mismo.
     * 
     * @returns {string} una cadena con las coordenadas del punto. 
     */
    this.toString = function() {
        return '(' + this.x + ', ' + this.y +')';
    }
}