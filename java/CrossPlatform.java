/*
 * This snippet uses some useful cross-platform properties.
 *
 * Usage:
 * - compile: javac CrossPlatform.java
 * - execute: java CrossPlatform
 */

public class CrossPlatform {

	/**
	 * @param args
	 */
	public static void main(String[] args) {
		
		// Get the file separator character
		System.out.println( System.getProperty("file.separator") );
		
		// Get the line separator character(s)
		System.out.println( System.getProperty("line.separator") );
		
		// Get the current user's name
		System.out.println( System.getProperty("user.name") );
		
		// Get the current user's home (directory) path
		System.out.println( System.getProperty("user.home") );

	}

}
