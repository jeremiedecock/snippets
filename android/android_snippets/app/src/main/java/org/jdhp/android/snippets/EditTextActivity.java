package org.jdhp.android.snippets;

import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.EditText;
import android.widget.Toast;

public class EditTextActivity extends AppCompatActivity {

    EditText etMessage;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_edit_text);

        etMessage = (EditText) findViewById(R.id.et_text_entry);
    }

    public void displayToastFromTextEntry(View view) {
        String message = etMessage.getText().toString();
        Toast.makeText(this, message, Toast.LENGTH_SHORT).show();
    }
}
