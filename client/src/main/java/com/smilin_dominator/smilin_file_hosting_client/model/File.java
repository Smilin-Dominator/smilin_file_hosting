package com.smilin_dominator.smilin_file_hosting_client.model;

import java.util.UUID;
import java.util.Date;
import java.nio.ByteBuffer;

public class File {

    // Fields
    
    private UUID file_id;
    private ByteBuffer encrypted_filename;
    private ByteBuffer iv;
    private Date date;
    
    // Getters + Setters

    public UUID getFileId() {
        return file_id;
    }

    public void setFileId(UUID file_id) {
        this.file_id = file_id;
    }

    public ByteBuffer getEncryptedFilename() {
        return encrypted_filename;
    }

    public void setEncryptedFilename(ByteBuffer encrypted_filename) {
        this.encrypted_filename = encrypted_filename;
    }

    public ByteBuffer getIv() {
        return iv;
    }

    public void setIv(ByteBuffer iv) {
        this.iv = iv;
    }

    public Date getDate() {
        return date;
    }

    public void setDate(Date date) {
        this.date = date;
    }
    
}
