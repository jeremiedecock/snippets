import org.eclipse.swt.SWT;
import org.eclipse.swt.layout.GridData;
import org.eclipse.swt.layout.GridLayout;
import org.eclipse.swt.widgets.Display;
import org.eclipse.swt.widgets.Label;
import org.eclipse.swt.widgets.Shell;

public class SwtHello {

    public static void main(String [] args) {
        Display display = new Display();

        // Make the window
        Shell shell = new Shell(display);
        shell.setLayout(new GridLayout(1, false));

        shell.setText("Hello SWT");
        shell.setMinimumSize(400, 350);
        shell.setSize(640, 480);

        // Add a widget
        Label label = new Label(shell, SWT.NONE);
        label.setLayoutData(new GridData(GridData.FILL_BOTH));
        label.setText("Hello World");
        label.pack();

        // Render the window
        shell.pack();
        shell.open();

        while(!shell.isDisposed()) {
            if(!display.readAndDispatch()) {
                display.sleep();
            }
        }

        display.dispose();
    }
}
