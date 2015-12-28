/*
 * This snippet shows how to get an environment variable
 * (e.g. the PATH environment variable here).
 *
 * For more information, read "Le guide de survie Java" (chap. 2)
 * (by Timothy Fisher, ed. CampusPress).
 *
 * Usage:
 * - compile: javac EnvironmentVariables.java
 * - execute: java EnvironmentVariables
 */

public class EnvironmentVariables {
    public static void main(String [] args) {

        // Get the PATH environment variable
        String envPath = System.getenv("PATH");

        System.out.println(envPath);
    }
}
