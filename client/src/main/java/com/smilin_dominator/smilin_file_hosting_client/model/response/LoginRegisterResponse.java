package com.smilin_dominator.smilin_file_hosting_client.model.response;

import com.smilin_dominator.smilin_file_hosting_client.model.User;

public class LoginRegisterResponse {

    // Fields
    
    private Boolean success;
    private String error;
    private User data;
    
    // Getters + Setters

    public Boolean getSuccess() {
        return success;
    }

    public String getError() {
        return error;
    }

    public User getData() {
        return data;
    }
    
}
