import bot.SkypeBot;
import plugins.Catfacts;
import plugins.Chatbot;
import plugins.MagicEightBall;
import plugins.Ping;
import plugins.Roll;
import plugins.StawPoll;

public class Application {
    public static void main(String args[]) {
        SkypeBot skypeBot = new SkypeBot("", "");

        skypeBot.addPlugin(new Ping());
        skypeBot.addPlugin(new Roll());
        skypeBot.addPlugin(new Catfacts());
        skypeBot.addPlugin(new Chatbot(skypeBot));
        skypeBot.addPlugin(new StawPoll());
        skypeBot.addPlugin(new MagicEightBall());

        while (!skypeBot.shouldQuit()) {
        }
        skypeBot.logout();
    }
}
