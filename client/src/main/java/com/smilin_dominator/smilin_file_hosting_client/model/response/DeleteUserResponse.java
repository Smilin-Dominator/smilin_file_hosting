package com.smilin_dominator.smilin_file_hosting_client.model.response;

/**
 * This is the response from /user/delete
 * @author Devisha Padmaperuma
 */
public class DeleteUserResponse {

    // Fields
    
    private Boolean success;
    private String message;
    
    // Getters

    public Boolean getSuccess() {
        return success;
    }

    public String getMessage() {
        return message;
    }
    
}
