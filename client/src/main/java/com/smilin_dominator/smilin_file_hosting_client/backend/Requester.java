package com.smilin_dominator.smilin_file_hosting_client.backend;

import java.io.IOException;
import java.util.Optional;
import com.smilin_dominator.smilin_file_hosting_client.common.JSON;
import com.smilin_dominator.smilin_file_hosting_client.model.User;
import com.smilin_dominator.smilin_file_hosting_client.model.File;
import com.smilin_dominator.smilin_file_hosting_client.model.response.DeleteUserResponse;
import com.smilin_dominator.smilin_file_hosting_client.model.response.FileUploadUpdateResponse;
import com.smilin_dominator.smilin_file_hosting_client.model.response.LoginRegisterResponse;
import java.nio.file.Path;
import org.apache.http.HttpEntity;
import org.apache.http.client.HttpClient;
import org.apache.http.entity.mime.MultipartEntityBuilder;
import org.apache.http.client.methods.HttpDelete;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.client.methods.HttpRequestBase;
import org.apache.http.entity.ContentType;
import org.apache.http.entity.mime.HttpMultipartMode;
import org.apache.http.entity.mime.MultipartEntity;
import org.apache.http.entity.mime.content.ByteArrayBody;
import org.apache.http.entity.mime.content.FileBody;
import org.apache.http.entity.mime.content.StringBody;
import org.apache.http.impl.client.HttpClients;

public class Requester {
        
    private final HttpClient http = HttpClients.createDefault();
    private final String access_token;
    private final Crypto crypto;

    // Constructor
    
    public Requester(String access_token, Crypto crypto) {
        this.access_token = access_token;
        this.crypto = crypto;
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
        final HttpDelete request = new HttpDelete(URL.DELETE_USER);
        addAuthorizationHeader(request);
        final HttpEntity response = http.execute(request).getEntity();
        final DeleteUserResponse res = JSON.parseInputStream(response.getContent(), DeleteUserResponse.class);
        return res.getSuccess();
    }
    
    // Files
    
    public boolean uploadFile (Path path) throws IOException {
        
        final byte[] iv = this.crypto.generateIV();
        final String filename = path.getFileName().toString();
        final byte[] encrypted_filename = this.crypto.encryptFilename(filename, iv);
        final Path encrypted_file = crypto.createTempFile();
        this.crypto.encryptFile(path, encrypted_file, iv);
        
        // Request
        final HttpPost request = new HttpPost(URL.UPLOAD);
        final MultipartEntityBuilder bodyBuilder = MultipartEntityBuilder.create();
        bodyBuilder.setMode(HttpMultipartMode.BROWSER_COMPATIBLE);
        bodyBuilder.addBinaryBody("iv", iv);
        bodyBuilder.addBinaryBody("encrypted_filename", encrypted_filename);
        bodyBuilder.addBinaryBody("file", encrypted_file.toFile());
        request.setEntity(bodyBuilder.build());
        addAuthorizationHeader(request);
        
        // Response
        final HttpEntity response = http.execute(request).getEntity();
        final FileUploadUpdateResponse res = JSON.parseInputStream(response.getContent(), FileUploadUpdateResponse.class);
        return res.isSuccess();
        
    }
    
}
