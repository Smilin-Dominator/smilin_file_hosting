package com.smilin_dominator.smilin_file_hosting_client.model;

import java.util.UUID;
import java.util.Date;
import java.nio.ByteBuffer;

public class File {

    // Fields
    
    private UUID file_id;
    private byte[] encrypted_filename;
    private byte[] iv;
    private Long date;
    
    // Getters + Setters

    public UUID getFileId() {
        return file_id;
    }

    public void setFileId(UUID file_id) {
        this.file_id = file_id;
    }

    public byte[] getEncryptedFilename() {
        return encrypted_filename;
    }

    public void setEncryptedFilename(byte[] encrypted_filename) {
        this.encrypted_filename = encrypted_filename;
    }

    public byte[] getIv() {
        return iv;
    }

    public void setIv(byte[] iv) {
        this.iv = iv;
    }

    public Long getDate() {
        return date;
    }

    public void setDate(Long date) {
        this.date = date;
    }
    
}
