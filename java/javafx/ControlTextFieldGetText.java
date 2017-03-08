import javafx.application.Application;
import javafx.event.ActionEvent;
import javafx.event.EventHandler;
import javafx.scene.Scene;
import javafx.scene.control.TextField;
import javafx.scene.layout.StackPane;
import javafx.stage.Stage;

public class ControlTextFieldGetText extends Application {

    public void start(Stage stage) {
        TextField text = new TextField();
        text.setText("Hello");

        text.setOnAction(new EventHandler<ActionEvent>() {
            public void handle(ActionEvent event) {
                System.out.println(text.getText());
            }
        });

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
