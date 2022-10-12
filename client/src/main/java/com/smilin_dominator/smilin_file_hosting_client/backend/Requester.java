package com.smilin_dominator.smilin_file_hosting_client.backend;

import java.io.IOException;
import java.util.Optional;
import com.smilin_dominator.smilin_file_hosting_client.common.JSON;
import com.smilin_dominator.smilin_file_hosting_client.model.User;
import com.smilin_dominator.smilin_file_hosting_client.model.response.DeleteUserResponse;
import com.smilin_dominator.smilin_file_hosting_client.model.response.LoginRegisterResponse;
import org.apache.http.HttpEntity;
import org.apache.http.client.HttpClient;
import org.apache.http.client.methods.HttpDelete;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.client.methods.HttpRequestBase;
import org.apache.http.impl.client.HttpClients;

public class Requester {
        
    private final HttpClient http = HttpClients.createDefault();
    private String access_token;
    
    public void setAccessToken(String access_token) {
        this.access_token = access_token;
    }
    
    // Helper Methods
    
    public void addAuthorizationHeader (HttpRequestBase req) {
        final String auth = "Bearer " + this.access_token;
        req.addHeader("Authorization", auth);
    }
    
    // User Methods
    
    /**
     * This creates a user
     * @return A user object
     * @throws IOException If the program can't get the content of the response
     */
    public User register() throws IOException {
        final HttpPost request = new HttpPost(URL.REGISTER);
        final HttpEntity response = http.execute(request).getEntity();
        final LoginRegisterResponse res = JSON.parseInputStream(response.getContent(), LoginRegisterResponse.class);
        return res.getData();
    }
    
    /**
     * This logs in a user
     * @return A user object if the id exists
     * @throws IOException If the program can't get the content of the response
     */
    public Optional<User> login() throws IOException {
        final HttpPost request = new HttpPost(URL.LOGIN);
        addAuthorizationHeader(request);
        final HttpEntity response = http.execute(request).getEntity();
        final LoginRegisterResponse res = JSON.parseInputStream(response.getContent(), LoginRegisterResponse.class);
        if (res.getSuccess()) {
            return Optional.of(res.getData());
        }
        return Optional.empty();
    }
    
    /**
     * This deletes a user
     * @return True if the account was deleted
     * @throws IOException If the program can't get the content of the response
     */
    public boolean delete() throws IOException {
        final HttpDelete request = new HttpDelete(URL.DELETE);
        addAuthorizationHeader(request);
        final HttpEntity response = http.execute(request).getEntity();
        final DeleteUserResponse res = JSON.parseInputStream(response.getContent(), DeleteUserResponse.class);
        return res.getSuccess();
    }
    
}
