import org.eclipse.swt.SWT;
import org.eclipse.swt.events.SelectionAdapter;
import org.eclipse.swt.events.SelectionEvent;
import org.eclipse.swt.layout.GridData;
import org.eclipse.swt.layout.GridLayout;
import org.eclipse.swt.widgets.Button;
import org.eclipse.swt.widgets.Display;
import org.eclipse.swt.widgets.Shell;

public class WidgetsButtonWithListener {

    public static void main(String [] args) {
        Display display = new Display();

        // Make the window ////////////////////////////////

        Shell shell = new Shell(display);
        shell.setLayout(new GridLayout(1, false));

        shell.setText("Snippet SWT");
        shell.setMinimumSize(400, 350);
        shell.setSize(640, 480);

        // Add Button /////////////////////////////////////

        final Button button = new Button(shell, SWT.PUSH);
        button.setLayoutData(new GridData(GridData.FILL_HORIZONTAL));
        button.setText("Hello World");
        button.setToolTipText("This is a tooltips...");
        button.pack();

        // Listener ///////////////////////////////////////

        button.addSelectionListener(new SelectionAdapter() {
            public void widgetSelected(SelectionEvent e) {
                System.out.println("Hello");
            }
        });

        // Render the window //////////////////////////////

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

