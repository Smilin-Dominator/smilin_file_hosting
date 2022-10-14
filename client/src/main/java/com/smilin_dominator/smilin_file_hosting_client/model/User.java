package com.smilin_dominator.smilin_file_hosting_client.model;

import java.util.UUID;

public class User {

    // Fields
    
    private UUID user_id;
    private String access_token;
    
    // Getters + Setters

    public UUID getUserId() {
        return user_id;
    }

    public void setUserId(UUID user_id) {
        this.user_id = user_id;
    }

    public String getAccessToken() {
        return access_token;
    }

    public void setAccessToken(String access_token) {
        this.access_token = access_token;
    }
    
}
