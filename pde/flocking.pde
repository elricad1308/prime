// Flock.pde
//
// Este script implementa un modelo de vuelo de las aves utilizando la
// libreria grafica processing.js
// 

// El peso de vector de alineacion.
float ALIGN_WEIGHT = 1.0f;

// El peso del vector de cohesion.
float COHESION_WEIGHT = 1.0f;

// La distancia minima deseada entre aves.
float DESIRED_SEPARATION = 25.0f;

// La altura (en pixeles) del canvas.
int HEIGHT = 140;

// La cantidad de aves que conforman a la parvada.
int FLOCK_SIZE = 10;

// El tamano (en pixeles) con el que se dibujan las aves en el canvas.
float RADIUS = 5.0f;

// La fuerza maxima con la que las aves pueden girar.
float MAX_FORCE = 0.05f;

// La velocidad maxima a la que las aves pueden volar.
float MAX_SPEED = 2.0f;

// La distancia maxima hasta la cual dos aves se consideran vecinas.
float NEIGHBOR_DISTANCE = 50.0f;

// El peso del vector de separacion.
float SEPARATION_WEIGHT = 2.0f;

// La anchura (en pixeles) del canvas.
int WIDTH = 240;

// Este objeto es la parvada.
Flock flock;

// Esta imagen se utiliza como fondo
PImage bg;

// Inicializa el canvas.
void setup() {
    // Escoge un tamano de canvas adecuado a la pantalla
    if(screen.width > 900) {
        HEIGHT = 600;
        WIDTH = 800;
        bg = requestImage("img/clouds-bg.jpg");
    } else if(screen.width > 550) {
        HEIGHT = 368;
        WIDTH = 480;
        bg = requestImage("img/clouds-bg-m.jpg");
    } else {
        HEIGHT = 184;
        WIDTH = 240;
        bg = requestImage("img/clouds-bg-s.jpg");
    }

    // Crea a la parvada.
    flock = new Flock();

    // Configura el area de dibujado.
    size(WIDTH, HEIGHT);
    colorMode(RGB, 255, 255, 255, 100);

    // Agrega el conjunto inicial de aves a la parvada.
    for(int i = 0; i < FLOCK_SIZE; i++) {
        flock.addBird(new Bird(new Vector3D(random(0, WIDTH), random(0, HEIGHT))));
    }

    // Suaviza el dibujado de las figuras en el canvas.
    smooth();
}

// Metodo llamado cada fotograma para dibujar a la parvada.
void draw() {
    // Dibuja el fondo 
    if(bg.width > 0)
        background(bg);
    else
        background(#66CCFF);

    flock.run();
}

// Agrega una nueva ave cuando se hace click sobre el canvas.
void mousePressed() {
    flock.addBird(new Bird(new Vector3D(mouseX, mouseY)));
    FLOCK_SIZE++;
}

// ----------------------------------------------------------------- //

// Esta clase representa a la parvada.
class Flock {

    // Esta lista contiene a todos las aves.
    ArrayList birds;

    // Crea una nueva parvada.
    Flock() {
        birds = new ArrayList();
    }

    // Agrega una nueva ave a la parvada.
    void addBird(Bird b) {
        birds.add(b);
    }

    // Realiza la simulación.
    void run() {
        for(int i = 0; i < FLOCK_SIZE; i++) {
            Bird b = (Bird)birds.get(i);
            b.run(birds);
        }
    }

}

// ----------------------------------------------------------------- //

// Esta clase representa a un ave.
class Bird {

    Vector3D loc;                 // La posicion del ave.
    Vector3D vel;                 // La velocidad del ave.
    Vector3D acc;                // La aceleracion del ave.

    // Crea una nueva ave.
    Bird(Vector3D l) {
        acc = new Vector3D(0, 0);
        vel = new Vector3D(random(-1, 1), random(-1, 1));
        loc = l.copy();
    }

    // Alinea al ave para mantenerla en la direccion de la parvada.
    Vector3D align(ArrayList birds) {
        Vector3D sum = new Vector3D(0, 0, 0);
        int count = 0;

        // Para cada ave de la parvada, determina si es un vecino.
        for(int i = 0; i < FLOCK_SIZE; i++) {
            Bird other = (Bird)birds.get(i);
            float d = loc.distance(other.loc);

            // Si el ave es un vecino, almacena su velocidad.
            if((d > 0) && (d < NEIGHBOR_DISTANCE)) {
                sum.add(other.vel);
                count++;
            }
        }

        // Promedia el vector de alineacion.
        if(count > 0) {
            sum.div((float)count);
            sum.limit(MAX_FORCE);
        }

        return sum;
    }

    // Modifica la posicion del ave para mantenerlo dentro del canvas.
    void borders() {
        if(loc.x < -RADIUS) loc.x = WIDTH + RADIUS;

        if(loc.y < -RADIUS) loc.y = HEIGHT + RADIUS;

        if(loc.x > WIDTH + RADIUS) loc.x = -RADIUS;

        if(loc.y > HEIGHT + RADIUS) loc.y = -RADIUS;
    }

    // Modifica la velocidad y direccion del ave para mantener a la parvada unida.
    Vector3D cohesion(ArrayList birds) {
        Vector3D sum = new Vector3D(0, 0, 0);
        int count = 0;

        // Para cada ave de la parvada, determina si es un vecino.
        for(int i = 0; i < FLOCK_SIZE; i++) {
            Bird other = (Bird)birds.get(i);
            float d = loc.distance(other.loc);

            // Si el ave es un vecino, almacena su posicion.
            if((d > 0) && (d < NEIGHBOR_DISTANCE)) {
                sum.add(other.loc);
                count++;
            }
        }

        // Promedia la posicion de los vecinos
        if(count > 0) {
            sum.div((float)count);

            // Gira hacia la direccion de la parvada
            return steer(sum, false);
        }

        return sum;
    }

    // Realiza los calculos para mantener al ave dentro de la parvada.
    void flock(ArrayList birds) {
        Vector3D sep = separate(birds);       // Separacion
        Vector3D ali = align(birds);                 // Alineacion
        Vector3D coh = cohesion(birds);       // Cohesion

        // Ponderamos los vectores
        sep.mult(SEPARATION_WEIGHT);
        ali.mult(ALIGN_WEIGHT);
        coh.mult(COHESION_WEIGHT);

        // Sumamos los vectores a la aceleracion
        acc.add(sep);
        acc.add(ali);
        acc.add(coh);
    }

    // Dibuja al ave en el canvas.
    void render() {
        // Calcula la orientacion del ave
        float theta = vel.heading2D() + radians(90);

        // Configura la apariencia del ave.
        fill(#FFFFFF);
        stroke(#222222);

        // Configura la posicion y orientacion.
        pushMatrix();
        translate(loc.x, loc.y);
        rotate(theta);

        // Dibuja al ave.
        beginShape();
        vertex(0.5, -3.0);
        vertex(1.0, -2.0);
        vertex(1.5, -1.0);
        vertex(3.0, -2.0);
        vertex(6.0, 0.0);
        vertex(3.0, -1.0);
        vertex(0.5, 1.0);
        vertex(1.0, 2.0);

        vertex(-1.0, 2.0);
        vertex(-0.5, 1.0);
        vertex(-3.0, -1.0);
        vertex(-6.0, 0.0);
        vertex(-3.0, -2.0);
        vertex(-1.5, -1.0);
        vertex(-1.0, -2.0);
        vertex(-0.5, -3.0);
        endShape();
        popMatrix();
    }

    // Mueve al ave.
    void run(ArrayList birds) {
        flock(birds);
        update();
        borders();
        render();
    }

    // Modifica la posicion del ave para evitar colisiones.
    Vector3D separate(ArrayList birds) {
        Vector3D sum = new Vector3D(0, 0, 0);
        int count = 0;

        // Para cada ave de la parvada, comprueba si esta muy cerca.
        for(int i = 0; i < FLOCK_SIZE; i++) {
            Bird other = (Bird)birds.get(i);
            float d = loc.distance(other.loc);

            // Si el ave es un vecino, se mueve para evitar chocar
            if((d > 0) && (d < DESIRED_SEPARATION)) {
                // Calcula el vector para alejarse del ave vecina.
                Vector3D diff = loc.sub(loc, other.loc);
        
                // Pondera el vector en base a la distancia.
                diff.normalize();
                diff.div(d);

                // Sumamos al vector total.
                sum.add(diff);
                count ++;
            }
        }

        // Promedia el vector de separacion.
        if(count > 0) {
            sum.div((float)count);
        }

        return sum;
    }

    // Calcula el angulo de girado hacia un objetivo.
    Vector3D steer(Vector3D target, boolean slowdown) {
        Vector3D steer;                                                      // El vector de girado
        Vector3D desired = target.sub(target, loc);   // La direccion de girado.
        float d = desired.magnitude();                             // La distancia al objetivo,

        // Si la distancia es mayor a 0, calcula el vector de girado.
        if(d > 0) {
            // Normaliza la direccion.
            desired.normalize();

            // Calcula la velocidad de giro.
            if((slowdown) && (d < 100.f))
                desired.mult(MAX_SPEED * (d/100.0f));
            else
                desired.mult(MAX_SPEED);

            // Calcula el angulo de girado.
            steer = target.sub(desired, vel);
            steer.limit(MAX_FORCE);
        } else {
            // Si la distancia es 0, el ave no debe girar.
            steer = new Vector3D(0, 0);
        }

        return steer;
    }

    // Actualiza la posicion del ave.
    void update() {
        // Actualiza la velocidad.
        vel.add(acc);

        // Regula la velocidad.
        vel.limit(MAX_SPEED);

        // Mueve al ave.
        loc.add(vel);

        // Reinicia la aceleracion a cero.
        acc.setXYZ(0, 0, 0);
    }

}

// ----------------------------------------------------------------- //

// Esta clase es un vector simple que las aves utilizan para moverse.
static class Vector3D {

    float x;                // El componente X.
    float y;                // El componente Y.
    float z;                // El componente Z.

    // Crea un Vector3D definiendo 3 componentes.
    Vector3D(float px, float py, float pz) {
        x = px;
        y = py;
        z = pz;
    }

    // Crea un Vector3D definiendo 2 componentes.
    Vector3D(float px, float py) {
        x = px;
        y = py;
        z = 0.0f;
    }

    // Suma el vector v y este vector.
    void add(Vector3D v) {
        x += v.x;
        y += v.y;
        z += v.z;
    }

    // Crea una copia de este vector.
    Vector3D copy() {
        return new Vector3D(x, y, z);
    }

    // Calcula la distancia entre este vector y el vector v.
    float distance(Vector3D v) {
        float dx = x - v.x;
        float dy = y - v.y;
        float dz = z - v.z;

        return (float)Math.sqrt(dx*dx + dy*dy + dz*dz);
    }

    // Divide los componentes de este vector entre el escalar n.
    void div(float n) {
        x /= n;
        y /= n;
        z /= n;
    }

    // Obtiene la orientacion del ave.
    float heading2D() {
        float angle = (float)Math.atan2(-y, x);
        return -1 * angle;
    }

    // Limita la magnitud de este vector para que no sobrepase el valor max.
    void limit(float max) {
        if(magnitude() > max) {
            normalize();
            mult(max);
        }
    }

    // Calcula la magnitud de este vector.
    float magnitude() {
        return (float)Math.sqrt(x*x + y*y + z*z);
    }

    // Multiplica este vector por el escalar n.
    void mult(float n) {
        x *= n;
        y *= n;
        z *= n;
    }

    // Normaliza este vector.
    void normalize() {
        float m = magnitude();
        if(m > 0) {
            div(m);
        }
    }

    // Establece los componentes de este vector.
    void setXYZ(float px, float py, float pz) {
        x = px;
        y = py;
        z = pz;
    }

    // Resta los elementos de dos vectores.
    Vector3D sub(Vector3D v1, Vector3D v2) {
        Vector3D v = new Vector3D(v1.x - v2.x, v1.y - v2.y, v1.z - v2.z);

        return v;
    }

}