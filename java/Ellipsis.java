/*
 * An example of ellipsis.
 * 
 * Usage:
 * - compile: javac GetNumCores.java
 * - execute: java GetNumCores
 */

public class Ellipsis {
	
	/**
	 * The ellipsis example
	 * 
	 * @param args
	 */
	public static void ellipsisMethod(String... args) {
		// args is a table of String
		System.out.println(args.length);
		
		for(String arg : args) {
			System.out.println(arg);
		}
	}

	/**
	 * @param args
	 */
	public static void main(String[] args) {
		Ellipsis.ellipsisMethod();
		Ellipsis.ellipsisMethod("param1");
		Ellipsis.ellipsisMethod("param1", "param2");
	}

}
