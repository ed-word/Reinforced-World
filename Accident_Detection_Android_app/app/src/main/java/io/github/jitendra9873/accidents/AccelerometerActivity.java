package io.github.jitendra9873.accidents;


import android.content.Context;
import android.graphics.Color;
import android.hardware.Sensor;
import android.hardware.SensorEvent;
import android.hardware.SensorEventListener;
import android.hardware.SensorManager;
import android.os.Bundle;
import android.os.CountDownTimer;
import android.support.v7.app.AppCompatActivity;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;
import android.widget.Toast;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.util.Date;

public class AccelerometerActivity extends AppCompatActivity implements SensorEventListener {

    SoundRecording r=null;
    private SensorManager sm;
    private String TAG="AccelerometerActivity";
    Context mContext;
    GPSTracker g;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_accelerometer);
        mContext=getApplicationContext();
        sm = (SensorManager) getSystemService(SENSOR_SERVICE);
        g=new GPSTracker(mContext);
        initActionButtons();
    }


    @Override
    public void onBackPressed() {
        super.onBackPressed();
        stopSensor();
        finish();
    }

    @Override
    public void onSensorChanged(SensorEvent event) {
        Acceleration capturedAcceleration = getAccelerationFromSensor(event);
        updateTextView(capturedAcceleration);
    }

    @Override
    public void onAccuracyChanged(Sensor sensor, int accuracy) {
        //Do nothing
    }

    /**
     * Init start and stop buttons actions.
     */
    private void initActionButtons() {
        final Button myStartButton = (Button) findViewById(R.id.button_start);
        final Button myStopButton = (Button) findViewById(R.id.button_stop);

        myStartButton.setVisibility(View.VISIBLE);
        myStopButton.setVisibility(View.GONE);

        //Start button action on click
        myStartButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                startSensor();
                myStartButton.setVisibility(View.GONE);
                myStopButton.setVisibility(View.VISIBLE);
            }
        });
        //Stop button action on click
        myStopButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                stopSensor();
                myStartButton.setVisibility(View.VISIBLE);
                myStopButton.setVisibility(View.GONE);
            }
        });


    }

    private void startSensor() {
        Sensor accelerometer = sm.getDefaultSensor(Sensor.TYPE_ACCELEROMETER);
        sm.registerListener(this, accelerometer, SensorManager.SENSOR_DELAY_NORMAL);
    }

    private void stopSensor() {
        sm.unregisterListener(this);
    }

    public float getCpuTemp() {
        Process p;
        try {
            p = Runtime.getRuntime().exec("cat sys/class/thermal/thermal_zone0/temp");
            p.waitFor();
            BufferedReader reader = new BufferedReader(new InputStreamReader(p.getInputStream()));

            String line = reader.readLine();
            float temp = Float.parseFloat(line) / 1000.0f;

            return temp;

        } catch (Exception e) {
            e.printStackTrace();
            return 0.0f;
        }
    }

    /**
     * Update acceleration text view with new values.
     *
     * @param capturedAcceleration
     */
    double m1=-1;
    long t1;
    boolean done=false;
    private void updateTextView(Acceleration capturedAcceleration) {
        TextView acceleration = (TextView) findViewById(R.id.acceleration);
        double x=capturedAcceleration.getX(),y=capturedAcceleration.getY(),z=capturedAcceleration.getZ();
        long ti=capturedAcceleration.getTimestamp();
        acceleration.setText("X : " + x +
                " m/s^2\nY : " + y +
                " m/s^2\nZ : " + z +
                " m/s^2\nTimestamp : " + ti);
        if(Math.sqrt(x*x+y*y+z*z)>30){
            Button t=(Button) findViewById(R.id.output);
            double p= Math.sqrt(x*x+y*y+z*z);
            if(p>m1) {
                //t.setText(Double.toString(p));
                t.setVisibility(View.VISIBLE);
                t.setClickable(false);
                m1=p;
            }
            if(r==null){
                r=new SoundRecording(mContext);
                r.start();
                new CountDownTimer(11000,1000){
                    public void onTick(long m){
                        Log.d(TAG, "onTick: ticking...");
                    }
                    public void onFinish(){
                        if(g.isGPSEnabled()){
                            Log.d(TAG, "latitude=: "+g.getLatitude()+",Longitude="+g.getLongitude());
                            Toast.makeText(mContext, "lat: "+g.getLatitude()+" lon :"+g.getLongitude(),
                                    Toast.LENGTH_LONG).show();
                        }
                        Log.d(TAG, "onFinish: Success");
                        r.stop();

                    }
                }.start();

            }
            Log.d(TAG, "updateTextView: "+getCpuTemp());
        }
    }

    /**
     * Get accelerometer sensor values and map it into an acceleration model.
     *
     * @param event
     * @return an acceleration model.
     */
    private Acceleration getAccelerationFromSensor(SensorEvent event) {
        long timestamp = (new Date()).getTime() + (event.timestamp - System.nanoTime()) / 1000000L;
        return new Acceleration(event.values[0], event.values[1], event.values[2], timestamp);
    }
}


