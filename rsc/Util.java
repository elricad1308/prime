import java.math.BigInteger;

/**
 * Proporciona métodos utilitarios para usar durante la resolución de las
 * cadena.
 * 
 * @author Jose Aguilar-Canepa.
 */
public final class Util {

    /**
     * Calcula el numero de combinaciones posibles que pueden obtenerse de los
     * parámetros indicados.
     * 
     * @param from el total de elementos.
     * @param take los elementos que se tomarán del total.
     * 
     * @return las combinaciones posibles de los elementos indicados.
     */
    public static final long comb(int from, int take) {
        // Calcula los factoriales presentes en la formula
        BigInteger fromFact = factorial(from);                  // n!
        BigInteger takeFact = factorial(take);                  // r!
        BigInteger fromMinusTakeFact = factorial(from - take);  // (n - r)!
        
        // Calcula el denominador de la formula = [ r! * (n - r)! ]
        BigInteger denominator = takeFact.multiply(fromMinusTakeFact);        
        
        // Calcula la formula de las combinaciones = n! / [ r! * (n - r)! ]
        BigInteger result = fromFact.divide(denominator);
        
        return result.longValue();
    }
    
    /**
     * Obtiene un número pseudo-aleatorio, exponencialmente distribuido. El
     * número regresado por este método se obtiene desde una distribución
     * exponencial negativa, con el parámetro <i>lambda</i> especificado.
     * El número regresado además es escalado utilizando el factor <i>scale</i>
     * para ajustarlo a una cierta escala numérica.
     * 
     * @param lambda el parámetro lambda de la distribución exponencial 
     * negativa.
     * 
     * @return un número exponencialmente distribuido.
     */
    public static final double exp(double lambda) {
        return Math.log(Math.random()) * (-1/lambda);
    }
    
    /**
     * Calcula el factorial del número n proporcionado. Este método NO está
     * pensado para ser utilizado con números grandes, el límite es 20!.
     * 
     * @param n el entero al cual se calculará el factorial.
     * 
     * @return el factorial de n.
     */
    public static final BigInteger factorial(int n) {
        BigInteger bi = BigInteger.valueOf(1);
        
        for(int i = 2; i <= n; i++) {
            bi.multiply(BigInteger.valueOf(i));
        }
        
        return bi;
    }
}
