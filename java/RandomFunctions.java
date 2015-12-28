import java.util.Random;

/*
 * This snippet uses some useful random functions.
 *
 * Usage:
 * - compile: javac RandomFunctions.java
 * - execute: java RandomFunctions
 */

public class RandomFunctions {

	/**
	 * @param args
	 */
	public static void main(String[] args) {

		// Default seed (time) ////////////////////////////////////////////////

		Random rand = new Random();

		// Get a pseudorandom integer, uniformly distributed between 0 and n.
		int n = 10;
		System.out.println(rand.nextInt(n));

		// Get a pseudorandom Gaussian ("normally") distributed double value
		// with mean 0.0 and standard deviation 1.0.
		System.out.println(rand.nextGaussian());

		// Get a pseudorandom boolean, uniformly distributed boolean value.
		System.out.println(rand.nextBoolean());

		// Get a pseudorandom double, uniformly distributed double value between
		// 0.0 and 1.0.
		System.out.println(rand.nextDouble());

		// Get a pseudorandom float, uniformly distributed float value between
		// 0.0 and 1.0.
		System.out.println(rand.nextFloat());

		// Get a pseudorandom uniformly distributed integer value from this
		// random number generator's sequence.
		System.out.println(rand.nextInt());

		// Get a pseudorandom uniformly distributed long value.
		System.out.println(rand.nextLong());

		
		// Custom seed (time) /////////////////////////////////////////////////

		Random custom_rand = new Random(0); // Here 0 is used as custom seed

		System.out.println(custom_rand.nextInt());

	}

}
