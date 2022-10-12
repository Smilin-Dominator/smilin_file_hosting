package com.smilin_dominator.smilin_file_hosting_client.backend;

import java.net.URI;

public abstract class URL {

    public static final String BASE = "http://localhost:2356/rest/v1";
    
    // User
    public static final URI REGISTER = URI.create(BASE + "/user/register");
    public static final URI LOGIN = URI.create(BASE + "/user/login");
    public static final URI DELETE = URI.create(BASE + "/user/delete");
    
}
