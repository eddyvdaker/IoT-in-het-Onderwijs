package com.zuyd.studybuddy;


// todo: is this class necesarry?

public class Studysession {
    private int id;
    private int activityid;
    private String start_time;
    private String stop_time;
    private String session_date;
    private int eventid;

    public Studysession() {
        this.id = -1;
        this.activityid = -1;
        this.start_time = "";
        this.stop_time = "";
        this.session_date = "";
        this.eventid = -1;
    }
}
