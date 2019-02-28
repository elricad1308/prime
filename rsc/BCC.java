/**
 * Implementa la cadena de Markov construida a partir del funcionamiento del
 * protocolo de comunicaciones BCC (Blocked Customer Cleared).
 * 
 * @author Jose Aguilar-Canepa.
 */
public class BCC {
    
    /**
     * El umbral de error deseado.
     */
    public static final double ERROR = 1.0E-6;
    
    private double alpha;    
    public double[] pi;
    private double[][] p;
    public int servers;
    
    /**
     * Crea una nueva simulación del protocolo BCC.
     * 
     * @param servers el número de servidores de la simulación.
     * @param alpha el cociente de la probabilidad de arribo entre la 
     * probabilidad de atencion.
     */
    public BCC(int servers, double alpha) {
        this.servers = servers;
        this.alpha = alpha;
    }
    
    /**
     * Recupera el valor de lambda.
     * 
     * @return el valor de lambda.
     */
    public double getAlpha() {
        return this.alpha;
    }
    
    /**
     * Inicializa los componentes necesarios para la simulación.
     */
    public void init() {
        // Crea una nueva matriz del tamaño indicado.
        p = new double[servers][servers];
        
        // Crea el vector pi vacío.
        pi = new double[servers];
        
        // Llena la matriz con sus probabilidades correspondientes.
        for(int i = 0; i < servers; i++) {
            for(int j = 0; j < servers; j++) {
                if(j == i + 1)
                    p[i][j] = this.alpha;
                else if(j == i - 1)
                    p[i][j] = (j * this.alpha);
                else
                    p[i][j] = 0.0;
            }
        }
    }
    
    /**
     * Cambia el valor de lambda.
     * 
     * @param alpha el nuevo valor de lambda.
     */
    public void setAlpha(double alpha) {
        this.alpha = alpha;
    }
    
    /**
     * Cambia el valor de mu.
     * 
     * @param servers el nuevo valor de mu.
     */
    public void setS(int servers) {
        this.servers = servers;
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
        int[] hits = new int[servers];
        double t1, t2;
        
        // Realiza la simulación de la cadena.
        for(int i = 0; i < iterations; i++) {
            t1 = Util.exp(this.alpha);
            t2 = Util.exp(currentState * this.alpha);
            
            if(t1 < t2)
                currentState++;
            else
                currentState--;
            
            if(currentState < 0)
                currentState = 0;
            
            if(currentState >= servers)
                currentState = (servers - 1);
            
            hits[currentState]++;
        }
        
        // Calcula el vector pi a partir de los resultados de la simulación.
        for(int i = 0; i < servers; i++)
            pi[i] = hits[i] / iterations;
    }
    
    /**
     * Halla los valores del vector pi utilizando el método Gauss-Seidel.
     */
    public void solveByGaussSeidel() {
        double[] aux = new double[servers];
        double suma;
        double error = 1.0;
        
        // Asignamos a cada elemento de pi una probabilidad uniforme.
        for(int i = 0; i < pi.length; i++) {
            pi[i] = 1.0 / (servers + 1);
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
        double denominator = 0.0;
        
        // Calcula el denominador de la división.
        for(int i = 0; i < servers; i++) {
            denominator += (Math.pow(alpha, i) / Util.factorial(i).longValue());
        }
        
        // Calcula el valor de pi de manera recursiva.
        for(int i = 0; i < servers; i++) {
            this.pi[i] = (Math.pow(alpha, i) / Util.factorial(i).longValue()) / denominator;
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
        
        // Ejecuta la simulación variando los valores de lambda y mu desde
        // 0 hasta 1 en incrementos de 0.05
        for(int i = 0; i < 10; i++) {            
            for(int j = 1; j <= 10; j++) {
                sim.setS(j);
                sim.init();
                
                // Des-comenta la forma por la que quieras resolver la cadena.
                //sim.solveByGaussSeidel();
                //sim.simulate(100000, 1);
                sim.solveRecursively();
                
                // La probabilidad de bloqueo es pi_s
                resultado[i][j - 1] = sim.pi[sim.servers - 1];
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