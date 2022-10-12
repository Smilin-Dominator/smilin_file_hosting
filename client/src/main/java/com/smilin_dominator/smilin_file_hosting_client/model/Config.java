package com.smilin_dominator.smilin_file_hosting_client.model;

import com.smilin_dominator.smilin_file_hosting_client.common.JSON;
import java.io.IOException;
import java.nio.file.Path;
import java.util.UUID;

public class Config {
    
    // Fields
    
    private String key;
    private UUID user_id;
    private String access_token;
    private Integer max_threads;
    private static final Path PATH = Path.of(System.getProperty("user.home"), ".config", "smilin_file_hosting", "config.json");
    
    // Static Methods
    
    /**
     * This parses the configuration file if it exists, and returns a Config
     * object with its values, or creates an empty config file and returns an
     * empty Config object
     * @return An instance of the Config class
     */
    public static Config load() {
        Config config;
        try {
            config = JSON.parseFile(PATH, Config.class);
            if (config == null) {
                config = new Config();
                config.save();
            }
        } catch (IOException e) {
            config = new Config();
            config.save();
        }
        return config;
    }

    // Methods
    
    /**
     * This saves the current configuration to the configuration file
     */
    public void save() {
        try {
            JSON.toFile(this, PATH);
        } catch (IOException e) {
            e.printStackTrace();
            System.exit(1);
        }
    }

    /**
     * This checks if all the fields are valid
     *
     * @return True if it's valid
     */
    public boolean isValid() {
        if (this.key == null) {
            return false;
        }
        if (this.user_id == null) {
            return false;
        }
        if (this.access_token == null) {
            return false;
        }
        return true;
    }

    // Getters + Setters
    
    public String getKey() {
        return key;
    }

    public void setKey(String key) {
        this.key = key;
    }

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

    public Integer getMaxThreads() {
        return max_threads;
    }

    public void setMaxThreads(Integer max_threads) {
        this.max_threads = max_threads;
    }
    
}
