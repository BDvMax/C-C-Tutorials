//PARTICIPANTES
//Zyon Maximo Rodriguez Gonzalez
//Jarol Gael Lizama Chan
//José Javier Muñoz May
public class POO_02_01
{
	public static void main(String args[])
	{
		Teclado t=new Teclado();
		int f, c, In, Neg, Sum, Ln, i, o;
		Sum=0;
		In=0;
		Neg=0;
		int altura = 0;
		int anchura = 0;
		int entrada = 0;
	
		int v[] = new int[6];
		
		System.out.println("Ingrese la altura y ancho de la matriz:");
		entrada=t.leeInt();
		int m[][] = new int[entrada][entrada];
		
		
		for (f=0;f<entrada; f++)
		{
			for (c=0;c<entrada;c++)
			{
				if (f==c)
				{
					//Diagonal principal
					System.out.println("Ingrese un numero:");
					m[f][c]=t.leeInt();

				}
			}
		}
		
		System.out.println("Matriz");
		for  (f=0; f<entrada; f++)
		{	
			for  (c=0; c <entrada; c++)
			{
				System.out.print(m[f][c] + "\t");
			}
			System.out.println();		
		}
	}
}
