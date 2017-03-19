package org.jdhp.android.snippets;

import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.Toast;

public class ToastActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_toast);
    }

    public void displayToast(View view) {
        String message = "Button clicked!";
        Toast.makeText(this, message, Toast.LENGTH_SHORT).show();
    }

}
