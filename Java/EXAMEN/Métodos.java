public class Métodos
{
    public void Agentes() {
    	
        Teclado X = new Teclado();

        int CogAg1, CogAg2;
        String NomAg1, NomAg2;

        int ComVend;
        int MontoAg1;
        int MontoAg2;
        double IngresoEmpresa;

        System.out.println("Capturar Nombre del agente1");
        NomAg1 = X.leeString();
        System.out.println("Capturar la cantidad de computadoras vendidas del agente1");
        CogAg1 = X.leeInt();
        System.out.println("Capturar Nombre del agente2");
        NomAg2 = X.leeString();
        System.out.println("Capturar la cantidad de computadoras vendidas del agente2");
        CogAg2 = X.leeInt();
        
        ComVend = CogAg1 + CogAg2;
        MontoAg1 = CogAg1 * 2800;
        MontoAg2 = CogAg2 * 2800;
        IngresoEmpresa = MontoAg1 + MontoAg2 * 0.80;
        
        System.out.println("Computadoras vendidas " + ComVend);
        System.out.println("El nonto de " + NomAg1 + " es " + MontoAg1);
        System.out.println("El nonto de " + NomAg2 + " es " + MontoAg2);
        System.out.println("El Imgreso de la empresa es " + IngresoEmpresa);
        
        //System.exit(0);
    }
	
	public void FactorialVector()
	{
		Teclado t=new Teclado();
		int Sum, cont, i, fact, c;
		Sum = 0;
		int n[]=new int[3];
		int f[]=new int[3];
		
		for  (i=0; i <=2; i++)
		{
			do 
			{
			System.out.println("Ingrese un numero:");
			n[i]=t.leeInt();
			cont = n[i];
			
			} while (cont % 1 != 0 || cont < 0);
			
				{
					fact=1;
					
					for (c=1;c<=cont;c++)
					{
						fact = fact*c;
					}
					f[i]=fact;
					
				}
			
		}	
				
		for (i=0; i <=2; i++)
			{
				System.out.println("Numero : "+ n[i]);
				System.out.println("Su factorial : "+ f[i]);
			}
	}
	
	public void Matriz3x3()
	{
		Teclado t=new Teclado();
		int f, c, In, Neg, Sum, Ln, i, o;
		Sum=0;
		In=0;
		Neg=0;
	
		int m[][] = new int[3][3];
		int v[] = new int[6];

		for (f=0;f<=2; f++)
		{
			for (c=0;c<=2;c++)
			{
				do
				{
				System.out.println("Ingrese un numero:");
				m[f][c]=t.leeInt();
				} while (m[f][c]%2!=0);
				
				//La suma
				Sum = m[f][c] + Sum;
				
				
				if (f!=2)
				{
					v[In]=m[f][c];
					In=In+1;
				}
				
				if (m[f][c]<0)
				{
					Neg++;
				}
			}
		}
		System.out.println("La suma de los elementos de la matriz :"+Sum);
		System.out.println("Elementos de la matriz contienen un número negativo :"+ Neg);
		
		System.out.println("Matriz");
		for  (f=0; f<=2; f++)
		{	
			for  (c=0; c <=2; c++)
			{
				System.out.print(m[f][c] + "\t");
			}
			System.out.println();		
		}
		System.out.println("Elementos de la primera y segunda fila (Vector)");
		for (i=0; i<=5; i++)
		{
			System.out.println(v[i] + "\t");
		}
		System.out.println();
	}
}
