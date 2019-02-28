/**
 * Implementa la cadena de Markov construida a partir del funcionamiento del 
 * protocolo de comunicaciones BCB (Blocked Customer Delay).
 * 
 * @author Jose Aguilar-Canepa
 */
public class BCD {
    
    /**
     * El umbral de error deseado.
     */
    public static final double ERROR = 1.0E-6;
    
    private double lambda;
    private double mu;
    private double[] pi;
    private double[][] p;
    private int servers;
    private int queue;
    private int clients;
    
    /**
     * Crea una nueva simulación del protocolo BCC.
     * 
     * @param servers el número de servidores de la simulación.
     * @param queue el tamaño de la cola de espera. Si el tamaño de la
     * cola es 0, el protocolo se reduce al BCC original. Si el tamaño de
     * la cola es negativo, se considera que la cola es infinita.
     * @param lambda la probabilidad que llegue un nuevo cliente.
     * @param mu la probabilidad que un cliente sea atendido.
     */
    public BCD(int servers, int queue, double lambda, double mu) {
        this.servers = servers;
        this.queue = queue;
        this.lambda = lambda;
        this.mu = mu;
    }
    
    /**
     * Recupera el valor de lambda.
     * 
     * @return el valor de lambda.
     */
    public double getLambda() {
        return this.lambda;
    }
    
    /**
     * Inicializa los componentes necesarios para la simulación.
     */
    public void init() {
        // Crea una nueva matriz del tamaño indicado.
        p = new double[servers + queue][servers + queue];
        
        // Crea el vector pi vacío.
        pi = new double[servers + queue];
        
        // Llena la matriz con sus probabilidades correspondientes.
        for(int i = 0; i < servers + queue; i++) {
            for(int j = 0; j < servers + queue; j++) {
                if(j == i + 1)
                    p[i][j] = this.lambda;
                else if(j == i - 1)
                    p[i][j] = (j * this.mu);
                else
                    p[i][j] = 0.0;
            }
        }
    }
    
    /**
     * Cambia el valor de lambda.
     * 
     * @param lambda el nuevo valor de lambda.
     */
    public void setLambda(double lambda) {
        this.lambda = lambda;
    }
    
    /**
     * Cambia el valor de mu.
     * 
     * @param mu el nuevo valor de mu.
     */
    public void setMu(double mu) {
        this.mu = mu;
    }
    
    /**
     * Realiza la simulación de la cadena.
     * 
     * @param iterations la cantidad de iteraciones que la simulación correrá.
     * @param initialState el índice de la cadena de Markov en la cual iniciará
     * la simulación.
     */
    public void simulate(int iterations, int initialState) {
        int currentState = initialState;
        int[] hits = new int[servers + queue];
        double t1, t2;
        
        // Realiza la simulación de la cadena.
        for(int i = 0; i < iterations; i++) {
            t1 = Util.exp(this.lambda + 0.001);
            if(currentState >= servers)
                t2 = Util.exp(servers * (this.mu + 0.001));
            else
                t2 = Util.exp(currentState * (this.mu + 0.001));
                        
            if(t1 < t2)
                currentState++;
            else
                currentState--;
            
            if(currentState < 0)
                currentState = 0;
            
            if(currentState >= (servers + queue))
                currentState = (servers + queue - 1);
            
            hits[currentState]++;
        }
        
        // Calcula el vector pi a partir de los resultados de la simulación.
        for(int i = 0; i < servers + queue; i++) {
            pi[i] = (double)hits[i] / (double)iterations;
        }
    }
    
    /**
     * Halla los valores del vector pi utilizando el método Gauss-Seidel.
     */
    public void solveByGaussSeidel() {
        double[] aux = new double[servers + queue];
        double suma;
        double error = 1.0;
        
        // Asignamos a cada elemento de pi una probabilidad uniforme.
        for(int i = 0; i < pi.length; i++) {
            pi[i] = 1.0 / (servers + queue + 1);
            aux[i] = 0.0;
        }
        
        // Resolvemos por Gauss-Seidel
        while(error > ERROR) {
            error = 0.0;
            
            // Calculamos el vector pi + 1
            for(int i = 0; i < pi.length; i++) {
                suma = 0.0;
                
                for(int j = 0; j < pi.length; j++) {
                    if(j != i)
                        suma += (pi[j] * p[j][i]);
                }
                
                aux[i] = suma / (1.0 - p[i][i]);
            }
            
            // Calculamos el error
            for(int i = 0; i < pi.length; i++)
                error += Math.abs(aux[i] - pi[i]);
            
            // Transferimos el contenido del vector auxiliar para la siguiente iteracion
            System.arraycopy(aux, 0, pi, 0, pi.length);
        }
    }
    
    /**
     * Halla los valores del vector pi utilizando el método recursivo.
     */
    public void solveRecursively() {
        double aux = this.lambda / this.mu;
        double denominator = 0.0;
        
        // Calcula el denominador de la división.
        for(int i = 0; i < servers + queue; i++) {
            if(i < servers)
                denominator += (Math.pow(aux, i) / Util.factorial(i).longValue());
            else
                denominator += (Math.pow(aux, servers) / Util.factorial(servers).longValue());
        }
        
        // Calcula el valor de pi de manera recursiva.
        for(int i = 0; i < servers + queue; i++) {
            if(i < servers)
                this.pi[i] = (Math.pow(aux, i) / Util.factorial(i).longValue()) / denominator;
            else
                this.pi[i] = (Math.pow(aux, servers) / Util.factorial(servers).longValue()) / denominator;
        }
    }
    
    /**
     * Ejecuta una simulación de prueba.
     * 
     * @param args los argumentos del programa.
     */
    public static void main(String[] args) {
        BCC sim = new BCC(10, 0.0);
        double[][] resultado = new double[10][10];
        
        // Ejecuta la simulación variando los valores de s            
        for(int i = 1; i <= 10; i++) {
            sim.setS(i);
            sim.init();
                
            // Des-comenta la forma por la que quieras resolver la cadena.
            //sim.solveByGaussSeidel();
            //sim.simulate(100000, 1);
            sim.solveRecursively();
                
            // La probabilidad de bloqueo es pi_s
            for(int j = 0; j < 10; j++) {
                try {
                    resultado[i - 1][j] = sim.pi[j] + (Math.random() / 10);
                } catch(ArrayIndexOutOfBoundsException e) {
                    resultado[i - 1][j] = 0.0;
                }
            }
            
            sim.setAlpha(sim.getAlpha() + 1);
        }
        
        // Imprime la matriz de resultados
        for(int i = 0; i < 10; i++) {
            System.out.print("[");
            for(int j = 0; j < 10; j++) {
                if(j != 9)
                    System.out.print(resultado[i][j] + ", ");
                else
                    System.out.print(resultado[i][j] + "],");
            }
            
            if(i != 9)
                System.out.print("\n");
        }
    }
}
