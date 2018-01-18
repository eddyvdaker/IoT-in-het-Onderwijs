package com.zuyd.studybuddy;


import android.os.AsyncTask;

import org.json.JSONObject;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.net.HttpURLConnection;
import java.net.URL;

public class HTTPPostRequest extends AsyncTask<String, Void, String> {

    public static final String REQUEST_METHOD = "SET";
    public static final int READ_TIMEOUT = 15000;
    public static final int CONNECTION_TIMEOUT = 15000;

    @Override
    protected void onPostExecute(String s) {
        super.onPostExecute(s);
    }

    @Override
    protected String doInBackground(String... strings) {
        String stringUrl = strings[0];
        String jsonLearningActivity = strings[1];
        String result;

        try {
            // create a URL object holding our url
            URL url = new URL(stringUrl);

            // create connection
            HttpURLConnection httpConnection = (HttpURLConnection) url.openConnection();

            // set methods and timeouts
            httpConnection.setRequestMethod(REQUEST_METHOD);
            httpConnection.setReadTimeout(READ_TIMEOUT);
            httpConnection.setConnectTimeout(CONNECTION_TIMEOUT);

            // connect to url
//            httpConnection.connect();

            // close output stream
            httpConnection.setDoOutput(true);
            OutputStream os = httpConnection.getOutputStream();
            os.write(jsonLearningActivity.toString().getBytes("UTF-8"));
            os.flush();
            os.close();

            // todo: get response

        } catch(IOException e) {
            e.printStackTrace();
            result = null;
        }
    }
}
