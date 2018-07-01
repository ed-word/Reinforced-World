package io.github.jitendra9873.accidents;

/**
 * Created by jitendra on 1/7/18.
 */


import android.app.Service;
        import android.content.Context;
        import android.content.DialogInterface;
        import android.content.Intent;
        import android.location.Location;
        import android.location.LocationListener;
        import android.location.LocationManager;
        import android.os.Bundle;
        import android.os.IBinder;
        import android.provider.Settings;
        import android.support.annotation.Nullable;
        import android.support.v7.app.AlertDialog;
        import android.view.View;


public class GPSTracker extends Service implements LocationListener {

    private LocationManager manager;
    private Location location;
    private double latitude;
    private double longitude;

    private boolean isGPSEnabled = false;
    private boolean isNetworkEnabled = false;

    private static final long MIN_DISTANCE_CHANGE_FOR_UPDATES = 10;
    private static final long MIN_TIME_BW_UPDATES = 1000 * 60;

    private Context context;
    private View baseView;


    public GPSTracker(Context context) {
        this.context = context;
        getLocation();
    }


    @Nullable
    @Override
    public IBinder onBind(Intent intent) {
        return null;
    }

    @SuppressWarnings("MissingPermission")
    public Location getLocation() {
        location = null;

        manager = (LocationManager) context.getSystemService(LOCATION_SERVICE);
        isGPSEnabled = manager.isProviderEnabled(LocationManager.GPS_PROVIDER);
        isNetworkEnabled = manager.isProviderEnabled(LocationManager.NETWORK_PROVIDER);


        if ((isGPSEnabled || isNetworkEnabled)) {
            if (isNetworkEnabled) {
                manager.requestLocationUpdates(
                        LocationManager.NETWORK_PROVIDER,
                        MIN_TIME_BW_UPDATES,
                        MIN_DISTANCE_CHANGE_FOR_UPDATES, this);
                if (manager != null) {
                    location = manager.getLastKnownLocation(LocationManager.NETWORK_PROVIDER);
                    if (location != null) {
                        latitude = location.getLatitude();
                        longitude = location.getLongitude();
                    }
                }
            }
            if (isGPSEnabled) {
                if (location == null) {
                    manager.requestLocationUpdates(
                            LocationManager.GPS_PROVIDER,
                            MIN_TIME_BW_UPDATES,
                            MIN_DISTANCE_CHANGE_FOR_UPDATES, this);
                    if (manager != null) {
                        location = manager.getLastKnownLocation(LocationManager.GPS_PROVIDER);
                        if (location != null) {
                            latitude = location.getLatitude();
                            longitude = location.getLongitude();
                        }
                    }
                }
            }
        }

        return location;
    }



    public boolean isGPSEnabled() {
        return isGPSEnabled || isNetworkEnabled;
    }

    public double getLatitude() {
        if (location != null) {
            latitude = location.getLatitude();
        }

        return latitude;
    }

    public double getLongitude() {
        if (location != null) {
            longitude = location.getLongitude();
        }

        return longitude;
    }


    @Override
    public void onLocationChanged(Location location) {

    }

    @Override
    public void onStatusChanged(String s, int i, Bundle bundle) {

    }

    @Override
    public void onProviderEnabled(String s) {

    }

    @Override
    public void onProviderDisabled(String s) {

    }
}