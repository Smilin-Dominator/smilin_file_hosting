package com.smilin_dominator.smilin_file_hosting_client.model.response;

import com.smilin_dominator.smilin_file_hosting_client.model.File;
import java.util.Date;
import java.util.UUID;

public class FileUploadUpdateResponse {

    private static class Data {
        
        private UUID id;
        private String encrypted_filename;
        private String iv;
        private Long date_added;

        public UUID getId() {
            return id;
        }

        public void setId(UUID id) {
            this.id = id;
        }

        public String getEncrypted_filename() {
            return encrypted_filename;
        }

        public void setEncrypted_filename(String encrypted_filename) {
            this.encrypted_filename = encrypted_filename;
        }

        public String getIv() {
            return iv;
        }

        public void setIv(String iv) {
            this.iv = iv;
        }

        public Date getDate_added() {
            return date_added;
        }

        public void setDate_added(Date date_added) {
            this.date_added = date_added;
        }
        
    }
    
    private boolean success;
    private Data data;

    public boolean isSuccess() {
        return success;
    }

    public File getData() {
        return data;
    }
    
}
