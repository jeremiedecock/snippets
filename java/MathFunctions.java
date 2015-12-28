/*
 * This snippet uses some useful Math functions.
 *
 * Usage:
 * - compile: javac MathFunctions.java
 * - execute: java MathFunctions
 */

public class MathFunctions {

	/**
	 * @param args
	 */
	public static void main(String[] args) {
		
		System.out.println( Math.PI );
		
		System.out.println( Math.floor(1.99) );
		System.out.println( Math.ceil(1.01) );
		
		System.out.println( Math.round(1.4) );
		System.out.println( Math.round(1.5) );
		System.out.println( Math.round(1.6) );
		
		System.out.println( Math.abs(1.5) );
		
		System.out.println( Math.cos(1.0) );
		System.out.println( Math.sin(1.0) );
		System.out.println( Math.tan(1.0) );
		
		System.out.println( Math.exp(1.0) );
		System.out.println( Math.log(1.0) );
		System.out.println( Math.log10(1.0) );
		
		System.out.println( Math.max(1, 2) );
		System.out.println( Math.min(1, 2) );
		
		System.out.println( Math.pow(3, 2) );
		System.out.println( Math.sqrt(9) );
		
		System.out.println( Math.random() );
		
		System.out.println( Math.toDegrees(1.0) );
		System.out.println( Math.toRadians(90.0) );
	}

}
