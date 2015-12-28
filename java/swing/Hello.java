import javax.swing.JFrame;
import javax.swing.JLabel;

/*
 * This snippet shows how to make a very basic Swing window.
 *
 * Usage:
 * - compile: javac Hello.java
 * - execute: java Hello
 */

public class Hello {
    public static void main(String args[]) {
        // Create a frame and set the title
        JFrame frame = new JFrame("Hello World!");

        // Set the default close operation
        frame.setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE);

        // Add a label
        frame.getContentPane().add(new JLabel("Hello, World!"));

        // Set the frame size
        frame.pack();

        // Center the frame
        frame.setLocationRelativeTo(null);

        // Show the frame
        frame.setVisible(true);
    }
}
