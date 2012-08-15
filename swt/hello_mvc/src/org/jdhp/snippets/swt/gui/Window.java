package org.jdhp.snippets.swt.gui;

import org.eclipse.swt.SWT;
import org.eclipse.swt.layout.GridData;
import org.eclipse.swt.layout.GridLayout;
import org.eclipse.swt.widgets.Display;
import org.eclipse.swt.widgets.Label;
import org.eclipse.swt.widgets.Shell;

public class Window
{
    private Display display;
    private Shell shell;
    private Label label;

    /**
     *
     */
    public Window() {
        this.display = new Display();

        // Make the window
        this.shell = new Shell(this.display);
        this.shell.setLayout(new GridLayout(1, false));

        this.shell.setText("Hello SWT");
        this.shell.setMinimumSize(400, 350);
        this.shell.setSize(640, 480);

        // Add a widget
        this.label = new Label(this.shell, SWT.NONE);
        this.label.setLayoutData(new GridData(GridData.FILL_BOTH));
        this.label.setText("Hello World");
        this.label.pack();
    }

    /**
     * Render the window
     */
    public void run() {
        this.shell.pack();
        this.shell.open();

        while(!this.shell.isDisposed()) {
            if(!this.display.readAndDispatch()) {
                this.display.sleep();
            }
        }

        this.display.dispose();
    }
}

