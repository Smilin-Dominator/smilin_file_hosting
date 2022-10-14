package com.smilin_dominator.smilin_file_hosting_client.common;

import com.google.gson.Gson;
import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.nio.file.Files;
import java.nio.file.Path;

public abstract class JSON {

    private static final Gson GSON = new Gson();
    
    public static <T> T parseInputStream(InputStream is, Class<T> cls) {
        final InputStreamReader isReader = new InputStreamReader(is);
        return GSON.fromJson(isReader, cls);
    }
    
    public static <T> T parseFile(Path path, Class<T> cls) throws IOException {
        final BufferedReader reader = Files.newBufferedReader(path);
        return GSON.fromJson(reader, cls);
    }
    
    public static <T> void toFile(T obj, Path path) throws IOException {
        if (!Files.exists(path)) {
            Files.createFile(path);
        }
        final BufferedWriter writer = Files.newBufferedWriter(path);
        GSON.toJson(obj, writer);
        writer.close();
    }
    
}
