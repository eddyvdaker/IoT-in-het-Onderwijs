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
    // empty constructor
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

    /// class methods: getters & setters
    public int getId() {
        return id;
    }

    public int getStudentid() {
        return studentid;
    }
    public void setStudentid(int studentid) {
        this.studentid = studentid;
    }

    public String getModuleid() {
        return moduleid;
    }
    public void setModuleid(String moduleid) {
        this.moduleid = moduleid;
    }

    public int getTeacherid() {
        return teacherid;
    }
    public void setTeacherid(int teacherid) {
        this.teacherid = teacherid;
    }

    public String getTitle() {
        return title;
    }
    public void setTitle(String title) {
        this.title = title;
    }

    public String getDescription() {
        return description;
    }
    public void setDescription(String description) {
        this.description = description;
    }

    public String getCategory() {
        return category;
    }
    public void setCategory(String category) {
        this.category = category;
    }

    public String getNotes() {
        return notes;
    }
    public void setNotes(String notes) {
        this.notes = notes;
    }

    public String getActivity_status() {
        return activity_status;
    }
    public void setActivity_status(String activity_status) {
        this.activity_status = activity_status;
    }

    public String getTime_est() {
        return time_est;
    }
    public void setTime_est(String time_est) {
        this.time_est = time_est;
    }
}
