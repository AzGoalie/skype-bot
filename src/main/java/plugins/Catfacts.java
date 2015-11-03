package plugins;

import java.io.IOException;
import java.net.URL;

import org.apache.commons.io.IOUtils;
import org.json.simple.JSONArray;
import org.json.simple.JSONObject;
import org.json.simple.JSONValue;
import org.json.simple.parser.ParseException;

import com.samczsun.skype4j.events.chat.message.MessageReceivedEvent;
import com.samczsun.skype4j.exceptions.SkypeException;
import com.samczsun.skype4j.formatting.Message;
import com.samczsun.skype4j.formatting.Text;

public class Catfacts implements Plugin {
    private static final String CATFACT_URL = "http://catfacts-api.appspot.com/api/facts";

    public String getHelp() {
        return "gives a random catfact!";
    }

    public String getCommand() {
        return "!catfact";
    }

    public void doCommand(MessageReceivedEvent event) throws SkypeException {
        try {
            String genreJson = IOUtils.toString(new URL(CATFACT_URL));
            JSONObject genreJsonObject = (JSONObject) JSONValue.parseWithException(genreJson);

            JSONArray facts = (JSONArray) genreJsonObject.get("facts");
            String catfact = (String) facts.get(0);

            Message m = Message.create().with(Text.plain(catfact));
            event.getChat().sendMessage(m);
        } catch (IOException io) {
                System.out.println("Unable to connect to catfact server: " + io.getMessage());
        } catch (ParseException pe) {
            System.out.println("Unable to parse catfacts: " + pe.getMessage());
        }
    }
}
