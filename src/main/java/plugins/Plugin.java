package plugins;

import com.samczsun.skype4j.events.chat.message.MessageReceivedEvent;
import com.samczsun.skype4j.exceptions.SkypeException;

public interface Plugin {
    String getHelp();

    String getCommand();

    void doCommand(MessageReceivedEvent event) throws SkypeException;
}
