package plugins;

import java.io.IOException;

import org.apache.http.HttpResponse;
import org.apache.http.client.methods.HttpGet;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.entity.StringEntity;
import org.apache.http.impl.client.CloseableHttpClient;
import org.apache.http.impl.client.HttpClientBuilder;
import org.apache.http.util.EntityUtils;
import org.json.simple.JSONArray;
import org.json.simple.JSONObject;
import org.json.simple.parser.JSONParser;
import org.json.simple.parser.ParseException;

import com.samczsun.skype4j.events.chat.message.MessageReceivedEvent;
import com.samczsun.skype4j.exceptions.SkypeException;
import com.samczsun.skype4j.formatting.Message;
import com.samczsun.skype4j.formatting.Text;

public class StawPoll implements Plugin {
    private final String API_URL = "https://strawpoll.me/api/v2/polls";
    private final String POLL_URL = "https://strawpoll.me/";

    public String getHelp() {
        return "creates a strawpoll! (arguments: title, multiple_votes(true/false), options(comma separated))";
    }

    public String getCommand() {
        return "!poll";
    }

    public void doCommand(MessageReceivedEvent event) throws SkypeException {
        if (event.getMessage().getContent().toString().split(" ")[1].equals("results")) {
            viewPoll(event);
        } else {
            createPoll(event);
        }
    }

    private void createPoll(MessageReceivedEvent event) throws SkypeException {
        String parts[] = event.getMessage().getContent().toString().replace(getCommand(), "").split(
                ",");
        if (parts.length < 3) {
            event.getChat().sendMessage(Message.create().with(Text
                    .plain("invalid poll command: !poll title, multiple_votes(true/false), options(comma separated)")));
            return;
        }

        String title = parts[0];
        boolean multi = parts[1].equals("true");
        JSONArray options = new JSONArray();
        for (int i = 2; i < parts.length; i++) {
            options.add(parts[i]);
        }

        JSONObject r = new JSONObject();
        r.put("title", title);
        r.put("options", options);
        r.put("multi", multi);

        try (CloseableHttpClient httpClient = HttpClientBuilder.create().build()) {
            HttpPost request = new HttpPost(API_URL);
            StringEntity params = new StringEntity(r.toJSONString());
            request.addHeader("content-type", "application/json");
            request.setEntity(params);
            HttpResponse result = httpClient.execute(request);

            String json = EntityUtils.toString(result.getEntity(), "UTF-8");

            JSONParser parser = new JSONParser();
            JSONObject response = (JSONObject)parser.parse(json);

            String message = "New Poll: ";
            message += response.get("title") + " ";
            message += POLL_URL + response.get("id") + "\n";
            message += "Options:\n";

            JSONArray o = (JSONArray)response.get("options");
            for (int i = 0; i < o.size(); i++) {
                message += o.get(i) + "\n";
            }

            message += "Get results with !poll results " + response.get("id");
            event.getChat().sendMessage(Message.create().with(Text.plain(message)));
        } catch(IOException e) {
            System.out.println("Error creating poll: " + e.getMessage());
        } catch (ParseException e) {
            e.printStackTrace();
        }
    }

    private void viewPoll(MessageReceivedEvent event) throws SkypeException {
        String id = event.getMessage().getContent().toString().split(" ")[2];
        try (CloseableHttpClient httpClient = HttpClientBuilder.create().build()) {
            HttpGet request = new HttpGet(API_URL + "/" + id);
            HttpResponse result = httpClient.execute(request);

            String json = EntityUtils.toString(result.getEntity(), "UTF-8");

            JSONParser parser = new JSONParser();
            JSONObject response = (JSONObject)parser.parse(json);

            String message = response.get("title") + "\n";
            JSONArray options = (JSONArray)response.get("options");
            JSONArray votes = (JSONArray)response.get("votes");
            for (int i = 0; i<options.size(); i++) {
                message += options.get(i) + ": " + votes.get(i) + "\n";
            }

            event.getChat().sendMessage(Message.create().with(Text.plain(message)));
        } catch (IOException io) {
            System.out.println("Unable to connect to strawpoll: " + io.getMessage());
        } catch (ParseException pe) {
            System.out.println("Unable to parse poll: " + pe.getMessage());
        }
    }
}
