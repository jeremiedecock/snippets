package org.jdhp.android.snippets;

import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.webkit.WebView;

public class WebViewActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_web_view);

        WebView wv = (WebView) findViewById(R.id.wv_webview);

        String html = "<html><body><b>Hello</b>,<i>world</i>!</body></html>";
        wv.loadData(html, "text/html", null);
    }
}