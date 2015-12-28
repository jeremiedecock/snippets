/*
 * This snippet returns the number of cores (CPU units) available.
 *  
 * Usage:
 * - compile: javac GetNumCores.java
 * - execute: java GetNumCores
 */

public class GetNumCores {

	/**
	 * @param args
	 */
	public static void main(String[] args) {
		int nbProc = Runtime.getRuntime().availableProcessors();
		
		System.out.println(nbProc);
	}

}
