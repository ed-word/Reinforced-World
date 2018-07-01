package io.github.jitendra9873.accidents;

import android.content.Intent;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;


public class MainActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        final Button myStartButton = (Button) findViewById(R.id.button_start);
        myStartButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                // do something when the corky is clicked
                Intent intent = new Intent();
                intent.setClass(MainActivity.this, AccelerometerActivity.class);
                startActivity(intent);
            }
        });
    }
}
