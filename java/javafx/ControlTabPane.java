import javafx.application.Application;
import javafx.scene.Scene;
import javafx.scene.control.Label;
import javafx.scene.control.Tab;
import javafx.scene.control.TabPane;
import javafx.stage.Stage;

public class ControlTabPane extends Application {

    public void start(Stage stage) {
        TabPane tabPane = new TabPane();

        // See http://stackoverflow.com/questions/31531059/how-to-remove-close-button-from-tabs-in-javafx
        tabPane.setTabClosingPolicy(TabPane.TabClosingPolicy.UNAVAILABLE);

        // Tab 1 ////////////////////////////////
        
        Label label1 = new Label("Hello 1");

        Tab tab1 = new Tab();
        tab1.setText("Tab 1");
        tab1.setContent(label1);

        tabPane.getTabs().add(tab1);

        // Tab 2 ////////////////////////////////

        Label label2 = new Label("Hello 2");

        Tab tab2 = new Tab();
        tab2.setText("Tab 2");
        tab2.setContent(label2);

        tabPane.getTabs().add(tab2);

        // Tab 3 ////////////////////////////////

        Label label3 = new Label("Hello 3");

        Tab tab3 = new Tab();
        tab3.setText("Tab 3");
        tab3.setContent(label3);

        tabPane.getTabs().add(tab3);
        
        /////////////////////////////////////////

        Scene scene = new Scene(tabPane, 400, 300);

        stage.setScene(scene);
        stage.show();
    }

    public static void main(String [] args) {
        launch(args);
    }

}
