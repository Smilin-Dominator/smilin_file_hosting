package com.smilin_dominator.smilin_file_hosting_client.backend;

import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.nio.file.Files;
import java.nio.file.Path;
import java.security.InvalidAlgorithmParameterException;
import java.security.InvalidKeyException;
import java.security.NoSuchAlgorithmException;
import java.util.Random;
import javax.crypto.BadPaddingException;
import javax.crypto.Cipher;
import javax.crypto.CipherInputStream;
import javax.crypto.CipherOutputStream;
import javax.crypto.IllegalBlockSizeException;
import javax.crypto.NoSuchPaddingException;
import javax.crypto.SecretKey;
import javax.crypto.spec.IvParameterSpec;
import javax.crypto.spec.SecretKeySpec;

public class Crypto {

    // Fields
    
    private static final String SALTCHARS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ";
    private final SecretKey key;
    
    // Constructor
    
    /**
     * This creates the crypto object with the user's key
     * @param key The user's key
     */
    public Crypto(String key) {
        this.key = new SecretKeySpec(key.getBytes(), "AES");
    }
    
    // Helper methods
    
    /**
     * This generates a random string
     * @param length The length of the string
     * @return The random string
     */
    private String generateRandomString(int length) {
        final Random rng = new Random();
        final StringBuilder sb = new StringBuilder();
        for (int i = 0; i < length; i++) {
            int index = (int) (rng.nextFloat() * SALTCHARS.length());
            sb.append(SALTCHARS.charAt(index));
        }
        return sb.toString();
    }
    
    /**
     * This creates a temporary file and returns its path
     * @return The path to the temporary file
     */
    public Path createTempFile() {
        Path path = null;
        try {
            path = Files.createTempFile(this.generateRandomString(32), ".sfh");
        } catch (IOException ignored) {
            System.err.println("Error while creating a temp file");
            System.exit(10);
        }
        return path;
    }
        
    /**
     * This configures a cipher for encryption and returns it
     * @return The cipher object
     */
    private Cipher getEncryptionCipher(byte[] iv) {
        Cipher cipher = null;
        try {
            cipher = Cipher.getInstance("AES/CBC/PKCS5Padding");
            cipher.init(Cipher.ENCRYPT_MODE, this.key, new IvParameterSpec(iv));
        } catch (InvalidKeyException | NoSuchAlgorithmException | NoSuchPaddingException | InvalidAlgorithmParameterException e) {
            System.err.println("Error when getting cipher!");
            System.exit(10);
        }
        return cipher;
    }
    
    /**
     * This configures a cipher for decryption and returns it
     * @param iv The initialization vector used to encrypt the object
     * @return The cipher object
     */
    private Cipher getDecryptionCipher(byte[] iv) {
        Cipher cipher = null;
        try {
            cipher = Cipher.getInstance("AES/CBC/PKCS5Padding");
            cipher.init(Cipher.DECRYPT_MODE, this.key, new IvParameterSpec(iv));
        } catch (InvalidKeyException | NoSuchAlgorithmException | NoSuchPaddingException | InvalidAlgorithmParameterException e) {
            System.err.println("Error when getting cipher!");
            System.exit(10);
        }
        return cipher;
    }
    
    /**
     * This reads an input stream chunk by chunk and writes to the output
     * stream
     * @param inStream The input stream
     * @param outStream The output stream
     */
    private void readStreamAndWriteToStream(InputStream inStream, OutputStream outStream) {
        byte[] buff = new byte[16];
        try {
            int bytesRead = inStream.read(buff);
            while (bytesRead != -1) {
                outStream.write(buff);
                bytesRead = inStream.read(buff);
            }
            inStream.close();
            outStream.close();
        } catch (IOException ignored) {
            System.err.println("Error occured while encrypting file!");
            System.exit(10);
        }
    }
        
    /**
     * This generates an initialization vector
     * @return A new iv
     */
    public byte[] generateIV() {
        byte[] bytes = new byte[16];
        new Random().nextBytes(bytes);
        return bytes;
    }
    
    // Encrypting Methods
    
    /**
     * This encrypts a filename and returns it
     * @param filename The filename to encrypt
     * @param iv The initialization vector used to encrypt the object
     * @return The encrypted filename
     */
    public byte[] encryptFilename(String filename, byte[] iv) {
        final Cipher cipher = this.getEncryptionCipher(iv);
        byte[] enc = null;
        try {
            enc = cipher.doFinal(filename.getBytes());
        } catch (IllegalBlockSizeException | BadPaddingException e) {
            System.err.println("Error when encrypting filename!");
            System.exit(10);
        }
        return enc;
    }
    
    /**
     * This creates a temp file and encrypts the specified file to the temp
     * file and returns its path
     * @param file The path of the file to encrypt
     * @param enc The path to output the encrypted contents to
     * @param iv The initialization vector used to encrypt the object
     */
    public void encryptFile(Path file, Path enc, byte[] iv) {
        final Cipher cipher = this.getEncryptionCipher(iv);
        try (
                FileInputStream fileIn = new FileInputStream(file.toFile()); // the normal file
                FileOutputStream fileOut = new FileOutputStream(enc.toFile()); // the encrypted file
                CipherOutputStream cipherOut = new CipherOutputStream(fileOut, cipher); // the cipher to the encrypted file
        ) {
            this.readStreamAndWriteToStream(fileIn, cipherOut);
        } catch (IOException e) {
            System.err.println("Error occured when encrypting a file");
            System.exit(10);
        }
    }
    
    // Decrypting Methods
    
    /**
     * This decrypts a filename
     * @param enc The encrypted filename
     * @param iv The initialization vector used to encrypt the object
     * @return The normal filename
     */
    public String decryptFilename(byte[] enc, byte[] iv) {
        final Cipher cipher = this.getDecryptionCipher(iv);
        String filename = null;
        try {
            filename = cipher.doFinal(enc).toString();
        } catch (IllegalBlockSizeException | BadPaddingException e) {
            System.err.println("Error when decrypting filename!");
            System.exit(10);
        }
        return filename;
    }
    
    /**
     * This decrypts a file to the specified path
     * @param enc The path to the encrypted file
     * @param dec The path of the file to decrypt to
     * @param iv The initialization vector used to encrypt the object
     */
    public void decryptFile(Path enc, Path dec, byte[] iv) {
        final Cipher cipher = this.getDecryptionCipher(iv);
        try (
                FileInputStream fileIn = new FileInputStream(enc.toFile()); // the encrypted file
                CipherInputStream cipherIn = new CipherInputStream(fileIn, cipher); // the cipher of the encrypted file
                FileOutputStream fileOut = new FileOutputStream(dec.toFile()); // the decrypted file to write to
        ) {
            this.readStreamAndWriteToStream(cipherIn, fileOut);
        } catch (IOException e) {
            System.err.println("Error when decrypting file!");
            System.exit(10);
        }
    }
    
}
