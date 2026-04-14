import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
public class Teclado
 {
  public static BufferedReader t = new BufferedReader(new
  InputStreamReader(System.in))  ;
  //Metodos
   public int leeInt()
   {
    int resultado = 0 ;
    try
    {
     resultado = Integer.parseInt( t.readLine() ) ;
    }
     catch(IOException e)
     {
      System.out.println("Error X: "+e);
      java.lang.System.exit(1);//termina con un gracioso error
     }
     return resultado ;
   }  //fin de int
   
  public float leeFloat()
   {
    float resultado = (float) 0.0 ;
    try
    {
     Float f = new Float( t.readLine() );
     resultado = f.floatValue() ;
    }
     catch(IOException e)
      {
      System.out.println("Error X: "+e);
      java.lang.System.exit(1);//termina con un gracioso error
      }
      return resultado ;
   }//fin de float

  public double leeDouble()
   {
    double resultado = 0.0;
    try
     {
      Double d = new Double(t.readLine() ) ;
      resultado = d.doubleValue() ;
     }
      catch(IOException e)
       {
        System.out.println("Error X: "+e);
        java.lang.System.exit(1);//termina con un gracioso error
       }
       return resultado ;
   } //fin de double

  public String leeString()
   {
    String resultado = new String() ;
    try
     {
      resultado = t.readLine() ;
     }
      catch(IOException e)
       {
        System.out.println("Error X: "+e);
        java.lang.System.exit(1);//termina con un gracioso error
       }
       return resultado ;
   } //fin de string

  public char leeChar(){
    char c = leeString().charAt(0);
    return c;
  }

 }//fin de programa     
      