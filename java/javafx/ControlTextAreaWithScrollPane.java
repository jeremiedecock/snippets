import javafx.application.Application;
import javafx.scene.Scene;
import javafx.scene.control.ScrollPane;
import javafx.scene.control.TextArea;
import javafx.scene.layout.StackPane;
import javafx.stage.Stage;

public class ControlTextAreaWithScrollPane extends Application {

    public void start(Stage stage) {
        TextArea text = new TextArea();
        text.setText("Hello");

        ScrollPane scrollPane = new ScrollPane();
        scrollPane.getStyleClass().add("noborder-scroll-pane");
        scrollPane.setStyle("-fx-background-color: white");
        scrollPane.setContent(text);
        scrollPane.setFitToWidth(true);
        scrollPane.setPrefHeight(180);

        Scene scene = new Scene(scrollPane);

        stage.setScene(scene);
        stage.show();
    }

    public static void main(String [] args) {
        launch(args);
    }

}
