import javafx.application.Application;
import javafx.scene.Scene;
import javafx.scene.control.TextArea;
import javafx.scene.layout.StackPane;
import javafx.stage.Stage;

public class ControlTextArea extends Application {

    public void start(Stage stage) {
        TextArea text = new TextArea();
        text.setText("Hello");

        StackPane root = new StackPane();
        root.getChildren().add(text);

        Scene scene = new Scene(root, 300, 200);

        stage.setScene(scene);
        stage.show();
    }

    public static void main(String [] args) {
        launch(args);
    }

}
