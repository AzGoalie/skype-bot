package plugins;

import java.util.Random;

import com.samczsun.skype4j.events.chat.message.MessageReceivedEvent;
import com.samczsun.skype4j.exceptions.SkypeException;
import com.samczsun.skype4j.formatting.Message;
import com.samczsun.skype4j.formatting.Text;

public class MagicEightBall implements Plugin {
    private Random random = new Random();
    private final String[] answers = {"It is certain",
            "It is decidedly so",
            "Without a doubt",
            "Yes, definitely",
            "You may rely on it",
            "As I see it, yes",
            "Most likely",
            "Outlook good",
            "Yes",
            "Signs point to yes",
            "Reply hazy try again",
            "Ask again later",
            "Better not tell you now",
            "Cannot predict now",
            "Concentrate and ask again",
            "Don't count on it",
            "My reply is no",
            "My sources say no",
            "Outlook not so good",
            "Very doubtful"
    };

    @Override
    public String getHelp() {
        return "answers your questions!";
    }

    @Override
    public String getCommand() {
        return "!ask";
    }

    @Override
    public void doCommand(MessageReceivedEvent event) throws SkypeException {
        int n = random.nextInt(answers.length);
        event.getChat().sendMessage(Message.create().with(Text.plain(answers[n])));
    }
}
