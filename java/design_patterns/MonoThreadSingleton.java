/*
 * This snippet shows an example of "Singleton" pattern.
 * 
 * Warning: this implementation is not "thread safe". Don't use it if you write
 * a multi-thread application !
 *
 * Usage:
 * - compile: javac MonoThreadSingleton.java
 * - execute: java MonoThreadSingleton
 */

public class MonoThreadSingleton {

	private static MonoThreadSingleton uniqueInstance;

	// The constructor is PRIVATE thus only Singleton can instantiate
	// Singleton...
	private MonoThreadSingleton() {
	}

	public static MonoThreadSingleton getInstance() {
		if (uniqueInstance == null) {                   // WARNING: this is not "thread-safe"
			uniqueInstance = new MonoThreadSingleton(); // WARNING: this is not "thread-safe"
		}
		return uniqueInstance;
	}

	// ...

	public static void main(String[] args) {
		System.out.println(MonoThreadSingleton.getInstance().toString());
		System.out.println(MonoThreadSingleton.getInstance().toString());
	}
}
