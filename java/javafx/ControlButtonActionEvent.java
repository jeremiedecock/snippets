import javafx.application.Application;
import javafx.event.ActionEvent;
import javafx.event.EventHandler;
import javafx.scene.Scene;
import javafx.scene.control.Button;
import javafx.stage.Stage;

public class ControlButtonActionEvent extends Application {

    public void start(Stage stage) {
        Button btn = new Button("Hello");

        //// or:
        //Button btn = new Button();
        //btn.setText("Hello");

        btn.setOnAction(new EventHandler<ActionEvent>() {
            public void handle(ActionEvent event) {
                System.out.println("Hello");
            }
        });

        Scene scene = new Scene(btn, 100, 50);

        stage.setScene(scene);
        stage.show();
    }

    public static void main(String [] args) {
        launch(args);
    }

}
