package plugins;

import java.util.Random;

import com.samczsun.skype4j.events.chat.message.MessageReceivedEvent;
import com.samczsun.skype4j.exceptions.SkypeException;
import com.samczsun.skype4j.formatting.Message;
import com.samczsun.skype4j.formatting.Text;

public class Roll implements Plugin {
    private Random random = new Random();

    public String getHelp() {
        return "rolls a dice of x sides (default is 20)";
    }

    public String getCommand() {
        return "!roll";
    }

    public void doCommand(MessageReceivedEvent event) throws SkypeException {
        String sides = event.getMessage().getContent().toString().replace(getCommand(), "").trim();
        int n = 20;
        if (!sides.isEmpty()) {
            n = Integer.parseInt(sides);
        }

        int roll = random.nextInt(n+1) + 1;
        Message m = Message.create().with(Text.plain(event.getMessage().getSender().getUsername() + " rolled a " + roll));
        event.getChat().sendMessage(m);
    }
}
