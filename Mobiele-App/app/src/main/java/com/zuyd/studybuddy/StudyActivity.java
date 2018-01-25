package com.zuyd.studybuddy;

public class StudyActivity {
    /// class attributes
    private int id;
    private int studentid;
    private String moduleid;
    private int teacherid;
    private String title;
    private String description;
    private String category;
    private String notes;
    private String activity_status;
    private String time_est;

    /// constructors
    public StudyActivity() {
        id = -1;
        studentid = -1;
        moduleid = "";
        teacherid = -1;
        title = "";
        description = "";
        category = "";
        notes = "";
        activity_status = "";
        time_est = "";
    }

    /// class methods
    // getters
    public int getId() {
        return id;
    }

    public int getStudentid() {
        return studentid;
    }

    public String getModuleid() {
        return moduleid;
    }

    public int getTeacherid() {
        return teacherid;
    }

    public String getTitle() {
        return title;
    }

    public String getDescription() {
        return description;
    }

    public String getCategory() {
        return category;
    }

    public String getNotes() {
        return notes;
    }

    public String getActivity_status() {
        return activity_status;
    }

    public String getTime_est() {
        return time_est;
    }

    // setters
    public void setStudentid(int studentid) {
        this.studentid = studentid;
    }

    public void setModuleid(String moduleid) {
        this.moduleid = moduleid;
    }

    public void setTeacherid(int teacherid) {
        this.teacherid = teacherid;
    }

    public void setTitle(String title) {
        this.title = title;
    }

    public void setDescription(String description) {
        this.description = description;
    }

    public void setCategory(String category) {
        this.category = category;
    }

    public void setNotes(String notes) {
        this.notes = notes;
    }

    public void setActivity_status(String activity_status) {
        this.activity_status = activity_status;
    }

    public void setTime_est(String time_est) {
        this.time_est = time_est;
    }
}
