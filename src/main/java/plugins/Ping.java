package plugins;

import com.samczsun.skype4j.events.chat.message.MessageReceivedEvent;
import com.samczsun.skype4j.exceptions.SkypeException;
import com.samczsun.skype4j.formatting.Message;
import com.samczsun.skype4j.formatting.Text;

public class Ping implements Plugin {
    public String getHelp() {
        return "pings the bot";
    }

    public String getCommand() {
        return "!ping";
    }

    public void doCommand(MessageReceivedEvent event)  throws SkypeException {
        Message m = Message.create().with(Text.plain("pong"));
            event.getChat().sendMessage(m);
    }
}
