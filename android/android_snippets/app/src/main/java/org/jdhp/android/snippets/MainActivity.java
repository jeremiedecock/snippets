package org.jdhp.android.snippets;

import android.content.Context;
import android.content.Intent;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;

public class MainActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
    }

    public void startButton(View view) {
        Context context = MainActivity.this;
        Class destinationActivity = ButtonActivity.class;
        Intent startChildActivityIntent = new Intent(context, destinationActivity);
        startActivity(startChildActivityIntent);
    }

    public void startEditText(View view) {
        Context context = MainActivity.this;
        Class destinationActivity = EditTextActivity.class;
        Intent startChildActivityIntent = new Intent(context, destinationActivity);
        startActivity(startChildActivityIntent);
    }

    public void startHello(View view) {
        Context context = MainActivity.this;
        Class destinationActivity = HelloActivity.class;
        Intent startChildActivityIntent = new Intent(context, destinationActivity);
        startActivity(startChildActivityIntent);
    }

    public void startLifeCycle(View view) {
        Context context = MainActivity.this;
        Class destinationActivity = LifeCycleActivity.class;
        Intent startChildActivityIntent = new Intent(context, destinationActivity);
        startActivity(startChildActivityIntent);
    }

    public void startLifeCycleWithBundle(View view) {
        Context context = MainActivity.this;
        Class destinationActivity = LifeCycleWithBundleActivity.class;
        Intent startChildActivityIntent = new Intent(context, destinationActivity);
        startActivity(startChildActivityIntent);
    }

    public void startLog(View view) {
        Context context = MainActivity.this;
        Class destinationActivity = LogActivity.class;
        Intent startChildActivityIntent = new Intent(context, destinationActivity);
        startActivity(startChildActivityIntent);
    }

    public void startToast(View view) {
        Context context = MainActivity.this;
        Class destinationActivity = ToastActivity.class;
        Intent startChildActivityIntent = new Intent(context, destinationActivity);
        startActivity(startChildActivityIntent);
    }

    public void startWebView(View view) {
        Context context = MainActivity.this;
        Class destinationActivity = WebViewActivity.class;
        Intent startChildActivityIntent = new Intent(context, destinationActivity);
        startActivity(startChildActivityIntent);
    }

}