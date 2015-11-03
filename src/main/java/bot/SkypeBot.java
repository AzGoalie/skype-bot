package bot;

import java.io.IOException;
import java.util.ArrayList;

import com.samczsun.skype4j.Skype;
import com.samczsun.skype4j.events.EventHandler;
import com.samczsun.skype4j.events.Listener;
import com.samczsun.skype4j.events.chat.message.MessageReceivedEvent;
import com.samczsun.skype4j.exceptions.SkypeException;
import com.samczsun.skype4j.formatting.Message;
import com.samczsun.skype4j.formatting.Text;

import plugins.Plugin;

public class SkypeBot {
    private Skype skype;
    private ArrayList<Plugin> plugins;
    private boolean quit = false;

    public SkypeBot(String username, String password) {
        try {
            plugins = new ArrayList<Plugin>();
            addPlugin(new Help());

            System.out.println("Logging into Skype");
            skype = Skype.login(username, password);
            skype.getEventDispatcher().registerListener(new ChatListener());
            System.out.println("Logged in and registered Chat Listener");
            skype.subscribe();
        } catch (SkypeException skypeException) {
            System.out.println("Skype failed to login: " + skypeException.getMessage());
        } catch (IOException ioException) {
            System.out.println("Failed to subscribe to events: " + ioException.getMessage());
        }
    }

    public void addPlugin(Plugin plugin) {
        plugins.add(plugin);
    }

    public void removePlugin(Plugin plugin) {
        plugins.remove(plugin);
    }

    public void logout() {
        try {
            System.out.println("Logging out of Skype");
            skype.logout();
        } catch (IOException e) {
            System.out.println("Failed to logout of Skype: " + e.getMessage());
        }
    }

    public boolean shouldQuit() {
        return quit;
    }

    private class ChatListener implements Listener {
        @EventHandler
        public void onMessage(MessageReceivedEvent e) {
            if (e.getMessage().getSender().getUsername() != skype.getUsername()) {
                String message = e.getMessage().getMessage().toString();
                System.out.println(e.getMessage().getSender().getUsername() + " : " + message);

                if (message.equals("!quit")) {
                    quit = true;
                    return;
                }

                for (Plugin plugin : plugins) {
                    if (message.startsWith(plugin.getCommand())) {
                        try {
                            plugin.doCommand(e);
                            break;
                        } catch (SkypeException skypeException) {
                            System.out.println("Failed to do command '" + plugin.getCommand() + "' : " + skypeException.getMessage());
                        }
                    }
                }
            }
        }
    }

    private class Help implements Plugin {

        public String getHelp() {
            return "returns this message that shows all commands";
        }

        public String getCommand() {
            return "!help";
        }

        public void doCommand(MessageReceivedEvent event) throws SkypeException {
            String helpMessage = "List of commands:\n";
            for (Plugin plugin : plugins) {
                helpMessage += plugin.getCommand() + " - " + plugin.getHelp() + "\n";
            }

            Message m = Message.create().with(Text.plain(helpMessage));
            event.getChat().sendMessage(m);
        }
    }
}
