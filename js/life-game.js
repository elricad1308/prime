/**
* life-game.js
* 
* Una implementacion del Juego de la Vida de Conway en JavaScript.
* Utiliza el algoritmo List Life de Tony Finch y una interfaz canvas
* de HTML5 para el dibujado.
*/

/** La cantidad inicial de celulas vivas en el mundo. */
var INITIAL_PROB = 0.1;

/** El objeto utilizado para implementar el Juego de la Vida. */
var LifeGame = {

    /** Determina si el canvas debe limpiarse o no. */
    clear : false,

    /** La cantidad de celulas en cada fila del canvas. */
    columns : 0,

    /** La generacion actual en la que se encuentra el algoritmo. */
    generation : 0,

    /** La cantidad de celulas en cada columna del canvas. */
    rows : 0,

    /** Determina si la animacion se esta ejecutando o no. */
    running : false,

    /** Tiempo de espera entre cada paso del algoritmo. */
    waitTime : Math.ceil(1000 / 15),

    /** Colors used to draw the cells. */
    colors : {
        /** The color used for empty cells. */
        empty : '#fff',

        /** The color used for dead cells. */
        dead : '#ccc',

        /** The colors used for alive cells. */
        alive : [
            '#9898FF', '#8585FF', '#7272FF', '#5F5FFF', 
            '#4C4CFF', '#3939FF', '#2626FF', '#1313FF', 
            '#0000FF', '#1313FF', '#2626FF', '#3939FF', 
            '#4C4CFF', '#5F5FFF', '#7272FF', '#8585FF'
        ]
    },

    /** The different sizes of the canvas. */
    sizes : {
        /** The size currently in use by the canvas. */
        current : -1,

        /** The sizes of canvas supported. */
        schemes : [
            /** The size used for phones. */
            {
                columns : 40, 
                rows : 30, 
                cellSize : 4
            },

            /** The size used for tablets. */
            {
                columns : 120,
                rows : 90,
                cellSize : 4
            },

            /** The size used for desktop computers. */
            {
                columns : 100,
                rows : 75,
                cellSize : 8
            }
        ]
    },

    /**
    * Prepara la simulacion para la ejecucion del siguiente paso.
    *
    * @returns {void} nada.
    */
    cleanUp : function() {
        this.listLife.init();
        this.prepare();
    },

    /**
    * Inicializa los parametros de la simulacion.
    *
    * @returns {void} nada.
    */
    init : function() {
        try {
            // Inicializa el algoritmo.
            this.listLife.init();

            // Establece el tamaño del canvas
            this.rows = this.sizes.schemes[this.sizes.current].rows;
            this.columns = this.sizes.schemes[this.sizes.current].columns;

            // Crea el estado inicial aleatorio del mapa.
            this.randomState();
            this.canvas.init();

            // Prepara la interfaz de usuario.
            this.prepare();
        } catch(e) {
            console.log("Error: " + e);
        }
    },

    /**
    * Calcula la posicion del cursor del mouse.
    *
    * @param {object} e el evento de la interfaz que involucra al
    *    mouse, normalmente un evento 'click'.
    *
    * @returns {array} un arreglo [x, y] con dos elementos, el primero
    *   de ellos corresponde a la coordenada en X del puntero, y el
    *   segundo corresponde a la coordenada en Y del cursor.
    */
    mousePosition : function(e) {
        var cellSize = LifeGame.sizes.schemes
          [LifeGame.sizes.current].cellSize + 1;
        var posx = 0, posy = 0, top = 0, left = 0;
        var event, x, y, domObject;

        // Forzamos la obtencion del evento.
        event = e;
        if(!event) event = window.event;
        
        // Recuperamos las coordenadas del puntero.
        if(event.pageX || event.pageY) {
            posx = event.pageX;
            posy = event.pageY;
        } else if(event.clientX || event.clientY) {
            posx = event.clientX + document.body.scrollLeft 
              + document.documentElement.scrollLeft;
            posy = event.clientY + document.body.scrollTop 
              + document.documentElement.scrollTop;
        }

        // Ajustamos la posicion para adaptarse a la escala del canvas.
        domObject = event.target || event.srcElement;

        while(domObject.offsetParent) {
            left += domObject.offsetLeft;
            top += domObject.offsetTop;
            domObject = domObject.offsetParent;
        }

        domObject.pageTop = top;
        domObject.pageLeft = left;

        // Calculamos las coordenadas finales.
        x = Math.ceil(((posx - domObject.pageLeft) / cellSize) - 1);
        y = Math.ceil(((posy - domObject.pageTop) / cellSize) - 1);

        return [x, y];
    },

    /**
    * Ejecuta un paso entero del algoritmo.
    *
    * @returns {void} nada.
    */
    nextStep : function() {
        var i, x, y, r, liveCellNumber;

        // Ejecuta el paso del algoritmo.
        liveCellNumber = this.listLife.nextGeneration();

        // Redibuja el estado de las celulas que cambiaron de estado.
        for(i = 0; i < this.listLife.redrawList.length; i++) {
            x = this.listLife.redrawList[i][0];
            y = this.listLife.redrawList[i][1];

            if(this.listLife.redrawList[i][2] === 1)
                this.canvas.changeCellToAlive(x, y);
            else if(this.listLife.redrawList[i][2] === 2)
                this.canvas.keepCellAlive(x, y);
            else
                this.canvas.changeCellToDead(x, y);
        }

        // Muestra la informacion del algoritmo.
        this.generation++;
        $('#gen_lbl').html(this.generation);
        $('#cells_lbl').html(liveCellNumber);            

        // Continue ejecutando la simulacion.
        if(this.running)
            setTimeout(function() { LifeGame.nextStep(); }, this.waitTime);
        else if(this.clear) 
            this.cleanUp(); 
    },

    /**
    * Prepara los elementos de la interfaz para una nueva simulacion.
    *
    * @returns {void} nada.
    */
    prepare : function() {
        this.generation = 0;
        this.clear = false;

        $('#gen_lbl').html('0');
        $('#cells_lbl').html('0');

        this.canvas.clearWorld();
        this.canvas.drawWorld();
    },

    /**
    * Genera un numero aleatorio entero entre el intervalo dado.
    *
    * @param {number} min el extremo inferior del intervalo.
    * @param {number} max el extremo superior del intervalo.
    *
    * @param {number} un entero escogido al azar entre el intervalo
    *   indicado.
    */
    random : function(min, max) {
        return min + Math.round(Math.random() * (max - min));
    },

    /**
    * Crea un estado inicial aleatorio para la simulacion.
    *
    * @returns {void} nada.
    */
    randomState : function() {
        var i, liveCells = (this.rows * this.columns) * INITIAL_PROB;

        // Aleatoriamente crea celulas vivas
        for(i = 0; i < liveCells; i++) 
            this.listLife.addCell(
                this.random(0, this.columns - 1), 
                this.random(0, this.rows - 1), 
                this.listLife.actualState
            );

        this.listLife.nextGeneration();
    },

    /** El objeto canvas utilizado para representar el algoritmo. */
    canvas : {
        
        /** Matriz utilizada para registrar la edad de las celulas. */
        age : null,

        /** El tamaño de las celulas en el canvas. */
        cellSize : null,

        /** El espacio entre celulas del canvas. */
        cellSpace : null,

        /** El objeto context2d del canvas. */
        context : null,

        /** La altura (en pixeles) del canvas. */
        height : null,

        /** La anchura (en piexeles) del canvas. */
        width : null,
        
        /**
        * Cambia el estado de la celula en la posicion indicada a
        * 'viva'.
        *
        * @param {number} i la fila de la celula.
        * @param {number} j la columna de la celula.
        *
        * @returns {void} nada.
        */
        changeCellToAlive : function(i, j) {
            if(i>=0 && i < LifeGame.columns && j>=0 && j < LifeGame.rows) {
                this.age[i][j] = 1;
                this.drawCell(i, j, true);
            }
        },

        /** 
        * Cambia el estado de la celula en la posicion indicada a
        * 'muerta'.
        *
        * @param {number} i la fila de la celula.
        * @param {number} j la columna de la celula.
        *
        * @returns {void} nada.
        */
        changeCellToDead : function(i, j) {
            if(i>=0 && i < LifeGame.columns && j>=0 && j < LifeGame.rows) {
                this.age[i][j] = -this.age[i][j];
                this.drawCell(i, j, false)
            }
        },

        /**
        * Limpia el canvas.
        * 
        * @returns {void} nada.
        */
        clearWorld : function() {
            var i, j;

            this.age = [];
            for(i = 0; i < LifeGame.columns; i++) {
                this.age[i] = [];
                for(j = 0; j < LifeGame.rows; j++)
                    this.age[i][j] = 0;                
            }
        },

        /**
        * Dibuja una celula en el canvas.
        *
        * @param {number} i la fila de la celula.
        * @param {number} j la columna de la celula.
        * @param {boolean} alive indica si la celula esta viva o no.
        *
        * @returns {void} nada.
        */
        drawCell : function(i, j, alive) {
            // Determina el color a utilizar para la celula.
            if(alive) {
                if(this.age[i][j] > -1)
                    this.context.fillStyle = LifeGame.colors.alive[
                      Math.floor(this.age[i][j] / LifeGame.colors.alive.length) 
                      % LifeGame.colors.alive.length
                    ];
            } else {
                if(this.age[i][j] < 0) 
                    this.context.fillStyle = LifeGame.colors.dead;
                else
                    this.context.fillStyle = LifeGame.colors.empty;
            }

            // Dibuja la celula
            this.context.fillRect(
              this.cellSpace + (this.cellSpace * i) + (this.cellSize * i), 
              this.cellSpace + (this.cellSpace * j) + (this.cellSize * j), 
              this.cellSize, 
              this.cellSize
            );
        },

        /**
        * Dibuja el estado actual en el que se encuentra el mundo.
        *
        * @returns {void} nada.
        */
        drawWorld : function() {
            var i, j;
            this.width = this.height = 1;

            // Determina de manera dinamica el tamaño del canvas.
            this.width = this.width + (this.cellSpace * LifeGame.columns) 
              + (this.cellSize * LifeGame.columns);
            this.canvas.setAttribute('width', this.width);

            this.height = this.height + (this.cellSpace * LifeGame.rows) 
              + (this.cellSize * LifeGame.rows);
            this.canvas.setAttribute('height', this.height);

            // Dibuja el fondo del canvas.
            this.context.fillStyle = '#f3f3f3';
            this.context.fillRect(0, 0, this.width, this.height);

            // Dibuja las celulas del algoritmo
            for(i = 0; i < LifeGame.columns; i++) 
                for(j = 0; j < LifeGame.rows; j++) 
                    if(LifeGame.listLife.isAlive(i, j))
                        this.drawCell(i, j, true);
                    else 
                        this.drawCell(i, j, false);
        },

        /**
        * Inicializa los parametros del canvas.
        *
        * @returns {void} nada.
        */
        init : function() {
            this.canvas = document.getElementById('lifegame');
            this.context = this.canvas.getContext('2d');

            this.cellSize = LifeGame.sizes.schemes
              [LifeGame.sizes.current].cellSize;
            this.cellSpace = 1;

            $('#lifegame').mousedown(LifeGame.handlers.canvasMouseDown);
            this.clearWorld();
        },

        /**
        * Mantiene viva a una celula. 
        *
        * @param {number} i la fila de la celula.
        * @param {number} j la columna de la celula.
        * 
        * @returns {void} nada.
        */
        keepCellAlive : function(i, j) {
            if(i>=0 && i < LifeGame.columns && j>=0 && j < LifeGame.rows) {
                this.age[i][j]++;
                this.drawCell(i, j, true);
            }
        },

        /**
        * Alterna el estado de una celula: si esta viva la mata, y si
        * esta muerta la revive.
        *
        * @param {number} i la fila de la celula.
        * @param {number} j la columna de la celula.
        *
        * @returns {void} nada.
        */
        switchCell : function(i, j) {
            if(LifeGame.listLife.isAlive(i, j)) {
                this.changeCellToDead(i, j);
                LifeGame.listLife.removeCell
                  (i, j, LifeGame.listLife.actualState);
            } else {
                this.changeCellToAlive(i, j);
                LifeGame.listLife.addCell
                  (i, j, LifeGame.listLife.actualState);
            }
        }
    },

    /** La lista de manejadores de eventos de la interfaz de usuario. */
    handlers : {
        
        /**
        * El manejador para el evento 'mouseDown' del canvas. Esta 
        * funcion alterna el estado de la celula presionada.
        *
        * @param {MouseEvent} event el evento 'mousedown' a manejar.
        *
        * @returns {void} nada.
        */
        canvasMouseDown : function(event) {
            var position = LifeGame.mousePosition(event);
            LifeGame.canvas.switchCell(position[0], position[1]);
        },

        /**
        * El manejador para el evento 'click' del boton para limpiar
        * el mundo. Esta funcion limpia completamente el canvas.
        *
        * @returns {void} nada.
        */
        clear : function() {
            if(LifeGame.running) {
                LifeGame.clear = true;
                LifeGame.running = false;
                $('#buttonRun').text('Run');
            } else 
                LifeGame.cleanUp();
        },
            
        /**
        * El manejador para el evento 'click' del boton para iniciar la
        * simulacion. Esta funcion inicia la simulacion (o la detiene,
        * si es que ya esta corriendo).
        *
        * @returns {void} nada.
        */
        run : function() {
            LifeGame.running = !LifeGame.running;

            if(LifeGame.running) {
                LifeGame.nextStep();
                $('#buttonRun').text('Stop');                    
            } else
                $('#buttonRun').text('Run');
        },

        /** 
        * El manejador para el evento 'click' del boton para ejecutar
        * un solo paso del algoritmo. Esta funcion realiza la ejecucion
        * completa de un paso del algoritmo.
        *
        * @returns {void} nada.
        */
        step : function() {
            if(!LifeGame.running)
                LifeGame.nextStep();
        },      
    },

    /** El objeto que implementa el algoritmo List Life. */
    listLife : {

        /** El estado actual en el que se encuentra el algoritmo. */
        actualState : [],

        /** Puntero inferior (utilizado al buscar vecinos). */
        bottomPointer : 1,

        /** Puntero medio (utilizado al buscar vecinos). */        
        middlePointer : 1,

        /** Lista de todas las celulas que modificaron su estado. */
        redrawList : [],

        /** Puntero superior (utilizado al buscar vecinos). */
        topPointer : 1,

        /** 
        * Agrega una nueva celula al estado del algoritmo. 
        *
        * @param {number} x la fila de la nueva celula.
        * @param {number} y la columna de la nueva celula.
        * @param {array} el estado actual del algoritmo.
        *
        * @returns {void} nada.
        */
        addCell : function(x, y, state) {
            if(state.length === 0) {
                state.push([y, x]);
                return;
            }

            var k, n, m, tempRow, newState = [], added;

            if(y < state[0][0]) {
                newState = [[y,x]];
                for(k = 0; k < state.length; k++) {
                    newState[k+1] = state[k];
                }

                for(k = 0; k < newState.length; k++) {
                    state[k] = newState[k];
                }

                return;
            } else if(y > state[state.length - 1][0]) {
                state[state.length] = [y, x];
            } else {
                for(n = 0; n < state.length; n++) {
                    if(state[n][0] === y) {
                        tempRow = [];
                        added = false;
                        for(m = 1; m < state[n].length; m++) {
                            if((!added) && (x < state[n][m])) {
                                tempRow.push(x);
                                added = !added;
                            }
                            tempRow.push(state[n][m]);
                        }
                        tempRow.unshift(y);
                        if(!added) {
                            tempRow.push(x);
                        }
                        state[n] = tempRow;
                        return;
                    }

                    if(y < state[n][0]) {
                        newState = [];
                        for(k = 0; k < state.length; k++) {
                            if(k === n) {
                                newState[k] = [y, x];
                                newState[k+1] = state[k];
                            } else if(k < n) {
                                newState[k] = state[k];
                            } else if(k > n) {
                                newState[k+1] = state[k];
                            }
                        }

                        for(k = 0; k < newState.length; k++) {
                            state[k] = newState[k];
                        }

                        return;
                    }
                }
            }
        },

        /**
        * Calcula la cantidad de vecinos vivos de la celula indicada.
        *
        * @param {number} x la fila de la celula.
        * @param {number} y la columna de la celula.
        * @param {i} el índice de la celula en el estado del algoritmo.
        * @param {array} possibleNeighbors un arreglo con las 
        *   coordenadas de todos las celulas que rodean a la celula.
        *
        * @returns {number} la cantidad de vecinos vivos alrededor de 
        *   la celula.
        */
        getNeighborsFromAlive : function(x, y, i, possibleNeighborsList) {
            var neighbors = 0, k;

            // Celulas que se encuentran arriba
            if(this.actualState[i-1] !== undefined) {
                if(this.actualState[i-1][0] === (y - 1)) {
                    for(k = this.topPointer; k < this.actualState[i-1].length; k++) {
                        if(this.actualState[i-1][k] >= (x-1)) {
                            if(this.actualState[i-1][k] === (x - 1)) {
                                possibleNeighborsList[0] = undefined;
                                this.topPointer = k + 1;
                                neighbors++;
                            }

                            if(this.actualState[i-1][k] === x) {
                                possibleNeighborsList[1] = undefined;
                                this.topPointer = k;
                                neighbors++;
                            }

                            if(this.actualState[i-1][k] === (x + 1)) {
                                possibleNeighborsList[2] = undefined;

                                if(k == 1)
                                    this.topPointer = 1;
                                else
                                    this.topPointer = k - 1;                                

                                neighbors++;
                            }

                            if(this.actualState[i-1][k] > (x + 1)) 
                                break;
                        }
                    }
                }
            }

            // Celulas que se encuentran en la misma fila.
            for(k = 1; k < this.actualState[i].length; k++) {
                if(this.actualState[i][k] >= (x - 1)) {
                    if(this.actualState[i][k] === (x - 1)) {
                        possibleNeighborsList[3] = undefined;
                        neighbors++;
                    }

                    if(this.actualState[i][k] === (x + 1)) {
                        possibleNeighborsList[4] = undefined;
                        neighbors++;
                    }

                    if(this.actualState[i][k] > (x + 1)) 
                        break;
                }
            }
                
            // Celulas que se encuentran abajo.
            if(this.actualState[i+1] !== undefined) {
                if(this.actualState[i+1][0] === (y + 1)) {
                    for(k = this.bottomPointer; k < this.actualState[i+1].length; k++) {
                        if(this.actualState[i+1][k] >= (x - 1)) {
                            if(this.actualState[i+1][k] === (x - 1)) {
                                possibleNeighborsList[5] = undefined;
                                this.bottomPointer = k +1;
                                neighbors++;
                            }

                            if(this.actualState[i+1][k] === x) {
                                possibleNeighborsList[6] = undefined;
                                this.bottomPointer = k;
                                neighbors++;
                            }

                            if(this.actualState[i+1][k] === (x + 1)) {
                                possibleNeighborsList[7] = undefined;

                                if(k == 1) 
                                    this.bottomPointer = 1;
                                else 
                                    this.bottomPointer = k - 1;

                                neighbors++;
                            }

                            if(this.actualState[i+1][k] > (x + 1)) 
                                break;
                        }
                    }
                }
            }

            return neighbors;
        },

        /** 
        * Inicializa el algoritmo.
        *
        * @returns {void} nada.
        */
        init : function() {
            this.actualState = [];
        }, 

        /** 
        * Determina si la celula en la posicion indicada esta viva.
        *
        * @param {number} x la fila de la celula.
        * @param {number} y la columna de la celula.
        *
        * @returns {boolean} true si la celula esta viva. false en caso
        *   contrario.
        */
        isAlive : function(x, y) {
            var i, j;
            for(i = 0; i < this.actualState.length; i++) 
                if(this.actualState[i][0] === y) 
                    for(j = 1; j < this.actualState[i].length; j++) 
                        if(this.actualState[i][j] === x) 
                            return true;

            return false;
        },

        /**
        * Realiza la ejecucion de un paso del algoritmo.
        *
        * @returns {number} la cantidad de celulas vivas en este paso
        *   del algoritmo.
        */
        nextGeneration : function() {
            var x, y, i, j, m, n, key, t1, t2, alive = 0, neighbors, deadNeighbors, allDeadNeighbors = {}, newState = [];
            this.redrawList = [];

            for(i = 0; i < this.actualState.length; i++) {
                this.topPointer = 1;
                this.bottomPointer = 1;

                for(j = 1; j < this.actualState[i].length; j++) {
                    x = this.actualState[i][j];
                    y = this.actualState[i][0];

                    deadNeighbors = [[x-1, y-1, 1], [x, y-1, 1], [x+1, y-1, 1], [x-1, y, 1], [x+1, y, 1], [x-1, y+1, 1], [x, y+1, 1], [x+1, y+1, 1]];

                    neighbors = this.getNeighborsFromAlive(x, y, i, deadNeighbors);
                    
                    for(m = 0; m < 8; m++) {
                        if(deadNeighbors[m] !== undefined) {
                            key = deadNeighbors[m][0] + ',' + deadNeighbors[m][1];

                            if(allDeadNeighbors[key] === undefined) 
                                allDeadNeighbors[key] = 1;
                            else 
                                allDeadNeighbors[key]++;
                        }
                    }

                    if(!(neighbors === 0 || neighbors === 1 || neighbors > 3)) {
                        this.addCell(x, y, newState);
                        alive++;
                        this.redrawList.push([x, y, 2]);
                    } else 
                        this.redrawList.push([x, y, 0]);
                }
            }
            
            for(key in allDeadNeighbors) {
                if(allDeadNeighbors[key] === 3) {
                    key = key.split(',');
                    t1 = parseInt(key[0], 10);
                    t2 = parseInt(key[1], 10);

                    this.addCell(t1, t2, newState);
                    alive++;
                    this.redrawList.push([t1, t2, 1]);
                }
            }

            this.actualState = newState;

            return alive;
        },

        /** 
        * Remueve una celula del estado del algoritmo. 
        *
        * @param {number} x la fila de la celula.
        * @param {number} y la columna de la celula.
        * @param {array} state el estado actual del algoritmo.
        *
        * @returns {void} nada.
        */
        removeCell : function(x, y, state) {
            var i, j;

            for(i = 0; i < state.length; i++) 
                if(state[i][0] === y) {
                    if(state[i].length === 2)
                        state.splice(i, 1);
                    else 
                        for(j = 1; j < state[i].length; j++) 
                            if(state[i][j] === x) 
                                state[i].splice(j, 1);
                }
        }
    }
};

$(document).ready(function(){

    $(window).resize(redraw);
    $('#buttonRun').click(LifeGame.handlers.run);
    $('#buttonStep').click(LifeGame.handlers.step);
    $('#buttonClear').click(LifeGame.handlers.clear);


    redraw();
});

function redraw() {
    var winWidth = window.innerWidth;
    var tempSize;

    if(winWidth > 900)
        tempSize = 2;
    else if(winWidth > 550)
        tempSize = 1;
    else
        tempSize = 0;

    

    if(tempSize != LifeGame.sizes.current) {
        LifeGame.running = false;
        LifeGame.sizes.current = tempSize;
        LifeGame.init();

        setTimeout(function(){
            LifeGame.running = true;
            LifeGame.nextStep();
            $('#buttonRun').text('Stop');
        }, 1000);
    }
}