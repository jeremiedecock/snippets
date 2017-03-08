import javafx.application.Application;
import javafx.scene.Scene;
import javafx.scene.control.Label;
import javafx.stage.Stage;

public class ControlLabel extends Application {

    public void start(Stage stage) {
        Label label = new Label("Hello");

        //// or:
        //Label label = new Label();
        //label.setText("Hello");

        Scene scene = new Scene(label, 100, 50);

        stage.setScene(scene);
        stage.show();
    }

    public static void main(String [] args) {
        launch(args);
    }

}
