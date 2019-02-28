/**
 * Implementa la cadena de Markov construida a partir del funcionamiento del
 * protocolo de comunicaciones ALOHA.
 * 
 * @author Jose Aguilar-Canepa.
 */
public final class ALOHA {
    
    /**
     * El umbral de error deseado.
     */
    public static final double ERROR = 1.0E-6;
    
    private final int mu;
    private double sigma;
    private double tau;
    private double[][] p;
    private double[] pi;
    
    /**
     * Crea una nueva simulacion del protocolo ALOHA.
     * 
     * @param mu el número de nodos de la red.
     * @param sigma la probabilidad que un nodo tiene de transmitir un mensaje.
     * @param tau la probabilidad que un nodo tiene de intentar retransmitir un
     * mensaje colisionado.
     */
    public ALOHA(int mu, double sigma, double tau) {
        this.mu = mu;
        this.sigma = sigma;
        this.tau = tau;
        
        init();
    }
    
    /**
     * Recupera el valor de sigma.
     * 
     * @return el valor de sigma.
     */
    public double getSigma() {
        return this.sigma;
    }
    
    /**
     * Calcula la probabilidad de éxito particula definida para el protocolo
     * ALOHA.
     * 
     * @param k la cantidad de mensajes en retranmisión.
     * 
     * @return la probabilidad que el protocolo tenga éxito cuando k mensajes
     * están tratando de transmitirse.
     */
    public double getSuccessProbability(int k) {
        return (
          (
            (mu - k) *
            sigma *
            Math.pow(1.0 - sigma, mu - k - 1) *
            Math.pow(1.0 - tau, k)
          ) +
          (
            k *
            tau *
            Math.pow(1.0 - tau, k - 1) *
            Math.pow(1.0 - sigma, mu - k)
          )
        );
    }
    
    /**
     * Calcula el promedio de probabilidad de éxito (throughput) para el
     * protocolo ALOHA.
     * 
     * @return el throughput de la simulación.
     */
    public double getThroughput() {
        double throughput = 0.0;
        
        for(int i = 0; i < mu; i++) {
            throughput += (getSuccessProbability(i) * pi[i]);
        }
        
        return throughput;
    }
    
    /**
     * Inicializa los componentes necesarios para la simulación.
     */
    public void init() {
        // Crea una nueva matriz del tamaño indicado.
        p = new double[mu][mu];
        
        // Crea el vector pi vacío
        pi = new double[mu];
        
        // Llena la matriz con sus probabilidades correspondientes
        for(int i = 0; i < mu; i++) {
            for(int j = 0; j < mu; j++) {
                if(j <  i - 1) p[i][j] = 0.0;
                if(j == i - 1) p[i][j] = getProbA(i, j);
                if(j == i)     p[i][j] = getProbB(i, j);
                if(j == i + 1) p[i][j] = getProbC(i, j);
                if(j >  i + 1) p[i][j] = getProbD(i, j);                
            }
        }
    }
    
    /**
     * Cambia el valor de sigma.
     * 
     * @param sigma el nuevo valor de sigma.
     */
    public void setSigma(double sigma) {
        this.sigma = sigma;
    }
    
    /**
     * Cambia el valor de tau.
     * 
     * @param tau el nuevo valor de tau.
     */
    public void setTau(double tau) {
        this.tau = tau;
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
        int[] hits = new int[mu];
        double probability;
        
        // Inicializa el arreglo de aciertos
        for(int i = 0; i < mu; i++) {
            hits[i] = 0;
        }
        
        // Realiza la simulación de la cadena
        for(int i = 0; i < iterations; i++) {
            probability = 0.0;
            
            for(int j = 0; j < mu; j++) {
                probability += p[currentState][j];
                
                if(Math.random() < probability) {
                    currentState = j;                    
                }
                
                hits[currentState]++;
            }
        }
        
        // Calcula el vector pi a partir de los resultados de la simulación
        for(int i = 0; i < mu; i++) {
            pi[i] = hits[i] / iterations;
        }
    }
    
    /**
     * Halla los valores del vector pi utilizando el método Gauss-Seidel.
     */
    public void solveByGaussSeidel() {
        double[] aux = new double[mu];
        double suma;
        double error = 1.0;
        
        // Asignamos a cada elemento de pi una probabilidad uniforme.
        for(int i = 0; i < pi.length; i++) {
            pi[i] = 1.0 / (mu + 1);
            aux[i] = 0.0;
        }
        
        // Resolvemos por Gauss-Seidel
        while(error > ERROR) {            
            error = 0.0;
            
            // Calculamos el vector pi + 1
            for(int i = 0; i < pi.length; i++) {
                suma = 0.0;
            
                for(int j = 0; j < pi.length; j++) 
                    if(j != i) 
                        suma += (pi[j] * p[j][i]);               
            
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
     * Resuelve la cadena de manera directa.
     */
    public void solveDirectly() {
        double[] aux = new double[mu];
        double total = 0.0;
        
        // El primer valor se asigna de manera arbitraria.
        aux[0] = 1;
        total += aux[0];
        
        // El resto de valores se calcula de manera recursiva.
        for(int i = 1; i < mu; i++) {
            aux[i] = (1.0 - p[i - 1][i - 1]) / p[i][i - 1];
            total += aux[i];
        }
        
        // Finalmente para obtener pi, el valor auxiliar se normaliza.
        for(int i = 1; i < mu; i++)
            pi[i] = aux[i] / total;
    }
    
    /**
     * Obtiene la probabilidad de clase A para una celda de la matriz P. La 
     * probabilidad clase A la tienen todos los elementos en la matriz P 
     * donde la columna j es igual a la fila i - 1.
     * 
     * @param i el índice de la fila de la celda.
     * @param j el índice de la columna de la celda.
     * 
     * @return la probabilidad clase A para la celda de la matriz P indicada.
     */
    private double getProbA(int i, int j) {
        return (
          i * 
          tau * 
          Math.pow(1.0 - tau, i - 1) * 
          Math.pow(1.0 - sigma, mu - i)
        );
    }
    
    /**
     * Obtiene la probabilidad de clase B para una celda de la matriz P. La 
     * probabilidad clase B la tienen todos los elementos en la matriz P 
     * donde la columna j es igual a la fila i (la diagonal principal).
     * 
     * @param i el índice de la fila de la celda.
     * @param j el índice de la columna de la celda.
     * 
     * @return la probabilidad clase B para la celda de la matriz P indicada.
     */
    private double getProbB(int i, int j) {
        return (
          (
            (1.0 - i * tau * Math.pow(1.0 - tau, i -1)) * 
            Math.pow(1.0 - sigma, mu - i)
          ) +
          (
            (mu - i) * 
            sigma * 
            Math.pow(1.0 - sigma, mu - i) * 
            Math.pow(1.0 - tau, i)
          )
        );
    }
    
    /**
     * Obtiene la probabilidad de clase C para una celda de la matriz P. La
     * probabilidad clase C la tienen todos los elementos en la matriz P donde
     * la columna j es igual a la fila i + 1.
     * 
     * @param i el índice de la fila de la celda.
     * @param j el índice de la columa de la celda.
     * 
     * @return la probabilidad clase C para la celda de la matriz indicada.
     */
    private double getProbC(int i, int j) {
        return (
          (mu - i) * 
          sigma * 
          Math.pow(1.0 - sigma, mu - i - 1) * 
          (1.0 - Math.pow(tau, 0) * Math.pow(1.0 - tau, i))
        );
    }
    
    /**
     * Obtiene la probabilidad de clase D para una celda de la matriz P. La
     * probabilidad clase D la tienen todos los elementos en la matriz P donde
     * la columna j es mayor a la fila i + 1.
     * 
     * @param i el índice de la fila de la celda.
     * @param j el índice de la columna de la celda.
     * 
     * @return la probabilidad clase D para la celda de la matriz indicada.
     */
    private double getProbD(int i, int j) {
        return (
          Util.comb(mu - i, j - i) * 
          Math.pow(sigma, j - i) * 
          Math.pow(1.0 - sigma, mu - i - (1.0 - sigma))
        );
    }
    
    /**
     * Ejecuta una simulación de prueba.
     * 
     * @param args los argumentos del programa.
     */
    public static void main(String[] args) {
        ALOHA sim = new ALOHA(10, 0.0, 0.0);
        double[][] matriz = new double[20][20];        
        double value;
        
        // Ejecuta la simulacion variando los valores de tau y sigma desde
        // 0 hasta 1 en incrementos de 0.05
        for(int i = 0; i < 20; i++) {            
            value = 0.0;
            
            for(int j = 0; j < 20; j++) {
                sim.setTau(value);
                sim.init();
                
                // Des-comenta la forma por la que quieras resolver la cadena.
                //sim.solveByGaussSeidel();
                //sim.simulate(100000, 0);
                sim.solveDirectly();
                
                matriz[i][j] = sim.getThroughput();
                value += 0.05;
            }
            
            sim.setSigma(sim.getSigma() + 0.05);
        }
        
        // Imprime la matriz de resultados
        for(int i = 0; i < 20; i++) {
            System.out.print("[");
            for(int j = 0; j < 20; j++) {
                if(j != 19)
                    System.out.print(matriz[i][j] + ", ");
                else
                    System.out.print(matriz[i][j] + "],");
            }
            
            if(i != 19)
                System.out.print("\n");
        }
    }
}