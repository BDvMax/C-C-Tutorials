public class MenuEJ2
{
	public static void main(String args[])
	{
		Teclado t=new Teclado();
		
		//Objeto
		Métodos m = new Métodos();
		
		int res;
		
		do 
		{
			System.out.println("Menu");
			System.out.println("1: Agentes de ventas");//unidad 1
			System.out.println("2: Vector cálculo de factorial de cada elemento");//un 4
			System.out.println("3: Matriz de 3 filas x 3 columnas");// No esta hecho
			System.out.println("4: Fin");
			System.out.println("Seleccione su opcion");
			res=t.leeInt();
			
			switch(res)
			{
				case 1: m.Agentes();
				break;
				
				case 2: m.FactorialVector();
				break;
				
				case 3: m.Matriz3x3();
				break;	
				
				case 4: System.out.println("Fin");
				break;
				
				default: System.out.println("Seleccion erronea, intente de nuevo");
			}
			
		} while (res != 4);
		
		System.out.println();		
		}	
}
