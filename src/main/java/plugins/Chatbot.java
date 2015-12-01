package plugins;

import com.google.code.chatterbotapi.ChatterBot;
import com.google.code.chatterbotapi.ChatterBotFactory;
import com.google.code.chatterbotapi.ChatterBotSession;
import com.google.code.chatterbotapi.ChatterBotType;
import com.samczsun.skype4j.events.chat.message.MessageReceivedEvent;
import com.samczsun.skype4j.exceptions.SkypeException;
import com.samczsun.skype4j.formatting.Message;
import com.samczsun.skype4j.formatting.Text;

import bot.SkypeBot;

public class Chatbot implements Plugin {
    private SkypeBot bot;
    private boolean on = false;
    private BotHandler botHandler;

    public Chatbot(SkypeBot bot) {
        this.bot = bot;
    }

    public String getHelp() {
        return "toggles on/off the chat bot. When on, talk to the bot with '!' before your message";
    }

    public String getCommand() {
        return "!chatbot";
    }

    public void doCommand(MessageReceivedEvent event) throws SkypeException {
        on = !on;
        if (on) {
            event.getChat().sendMessage(Message.create().with(Text.plain("Chatbot started, talk to it by starting with '!'")));
            event.getChat().sendMessage(Message.create().with(Text.plain("Hi!")));
            botHandler = new BotHandler();
            bot.addPlugin(botHandler);
        } else {
            event.getChat().sendMessage(Message.create().with(Text.plain("Chatbot ended")));
            bot.removePlugin(botHandler);
        }
    }

    private class BotHandler implements Plugin {
        private ChatterBotFactory factory;
        private ChatterBot bot;
        private ChatterBotSession session;

        public BotHandler() {
            try {
                factory = new ChatterBotFactory();
                bot = factory.create(ChatterBotType.PANDORABOTS, "c0be057cfe345a6e");
                session = bot.createSession();
            } catch (Exception e) {
                System.out.println("Error creating chat bot: " + e.getMessage());
            }
        }

        public String getHelp() {
            return "talk to the chat bot!";
        }

        public String getCommand() {
            return "!";
        }

        public void doCommand(MessageReceivedEvent event) throws SkypeException {
            try {
                String str = event.getMessage().getContent().toString().replace("!", "").trim();
                str = session.think(str).replaceAll("(?s)<[^>]*>(\\s*<[^>]*>)*", " ");;
                event.getChat().sendMessage(Message.create().with(Text.plain(str)));
            } catch (Exception e) {
                System.out.println("Error in bot think: " + e.getMessage());
            }
        }
    }
}
