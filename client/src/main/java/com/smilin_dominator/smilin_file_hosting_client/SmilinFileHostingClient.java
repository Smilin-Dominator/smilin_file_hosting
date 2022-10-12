package com.smilin_dominator.smilin_file_hosting_client;

import com.smilin_dominator.smilin_file_hosting_client.backend.Requester;
import com.smilin_dominator.smilin_file_hosting_client.model.Config;
import com.smilin_dominator.smilin_file_hosting_client.ui.AuthenticationUI;
import com.smilin_dominator.smilin_file_hosting_client.ui.MainUI;
import java.util.function.Supplier;

public class SmilinFileHostingClient {
    
    public static void main(String[] args) {
        
        final Config config = Config.load();
        final Requester requester = new Requester();
        
        final Supplier<AuthenticationUI> authUISupplier = () -> new AuthenticationUI(config, requester);
        
        final MainUI mainUI = new MainUI(authUISupplier, config.getMaxThreads());
        mainUI.setVisible(true);
        
        if (!config.isValid()) {
            
            mainUI.setEnabled(false);
            
            final AuthenticationUI authenticationUI = authUISupplier.get();
            authenticationUI.setVisible(true);
            authenticationUI.addWindowListener(new java.awt.event.WindowAdapter() {
                @Override
                public void windowClosed(java.awt.event.WindowEvent windowEvent) {
                    mainUI.setEnabled(true);
                }
            });
            
        }
        
    }
    
}
