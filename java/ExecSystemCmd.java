import java.io.IOException;

/*
 * This snippet shows how to execute a system command.
 * 
 * Usage:
 * - compile: javac ExecSystemCmd.java
 * - execute:    java ExecSystemCmd
 */

public class ExecSystemCmd {

	/**
	 * @param args
	 */
	public static void main(String[] args) {
		try {
			// Runtime.getRuntime().exec("commande param1 param2 ...");
			Process proc = Runtime.getRuntime().exec("zenity --info --title Hello --text hello_world");
		} catch(IOException e) {
			System.out.println(e.getMessage());
		}
	}

}
