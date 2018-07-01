package io.github.jitendra9873.accidents;

import android.content.Context;
import android.media.MediaPlayer;
import android.media.MediaRecorder;
import android.os.Environment;
import android.widget.Button;
import android.widget.Toast;

import java.io.IOException;

/**
 * Created by jitendra on 30/6/18.
 */



public class Recorder  {
    private Button play, stop, record;
    private MediaRecorder myAudioRecorder;
    private String outputFile;
    Context mContext;
    Recorder(Context c){
        mContext=c;
    }

    void start(){
        outputFile = Environment.getExternalStorageDirectory().getAbsolutePath() + "/recording.3gp";
        myAudioRecorder = new MediaRecorder();
        myAudioRecorder.setAudioSource(MediaRecorder.AudioSource.MIC);
        myAudioRecorder.setOutputFormat(MediaRecorder.OutputFormat.THREE_GPP);
        myAudioRecorder.setAudioEncoder(MediaRecorder.OutputFormat.AMR_NB);
        myAudioRecorder.setOutputFile(outputFile);

        try {
            myAudioRecorder.prepare();
            myAudioRecorder.start();
        } catch (IllegalStateException ise) {
            // make something ...
        } catch (IOException ioe) {
            // make something
        }
        Toast.makeText(mContext, "Recording started", Toast.LENGTH_LONG).show();
    }
    void stop(){
        myAudioRecorder.stop();
        myAudioRecorder.release();
        myAudioRecorder = null;
        Toast.makeText(mContext, "Audio Recorder successfully", Toast.LENGTH_LONG).show();
    }


    void play(){
        MediaPlayer mediaPlayer = new MediaPlayer();
        try {
            mediaPlayer.setDataSource(outputFile);
            mediaPlayer.prepare();
            mediaPlayer.start();
            Toast.makeText(mContext, "Playing Audio", Toast.LENGTH_LONG).show();
        } catch (Exception e) {
            // make something
        }
    }
}