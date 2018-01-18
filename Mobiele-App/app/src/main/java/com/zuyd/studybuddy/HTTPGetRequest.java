package com.zuyd.studybuddy;

import android.os.AsyncTask;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.concurrent.ExecutionException;

public class HTTPGetRequest extends AsyncTask<String, Void, String>{
    /* <Params, Progress, Result>
     * Params: the type of the parameters sent to the task upon execution.
     * Progress: the type of the progress units published during the background computation.
     * Result: the type of the result of the background computation.
     */

    public static final String REQUEST_METHOD = "GET";
    public static final int READ_TIMEOUT = 15000;
    public static final int CONNECTION_TIMEOUT = 15000;

    @Override
    protected void onPostExecute(String s) {
        // this is where you would do any post-processing on your result
        super.onPostExecute(s);
    }

    @Override
    protected String doInBackground(String... strings) {
        String stringUrl = strings[0]; // todo: for each in strings: try httpUrlConnection
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
            httpConnection.connect();

            // create inputStreamReader, buffered reader, and StringBuilder.
            InputStreamReader streamReader = new InputStreamReader(httpConnection.getInputStream());
            BufferedReader reader = new BufferedReader(streamReader);
            StringBuilder stringBuilder = new StringBuilder();

            // check if the line we are reading is not null
            String inputLine = reader.readLine();
            while (inputLine != null) {
                stringBuilder.append(inputLine);
                inputLine = reader.readLine();
            }

            // close inputStream
            reader.close();
            streamReader.close();

            // set result
            result = stringBuilder.toString();

        } catch(IOException e) {
            e.printStackTrace();
            result = null;
        }

        return result;
    }
}
