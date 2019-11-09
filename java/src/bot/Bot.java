package bot;

import java.io.IOException;
import java.io.StringWriter;
import java.net.HttpURLConnection;
import java.net.URL;
import java.text.DateFormat;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Calendar;
import java.util.Date;
import java.util.List;

import org.apache.commons.io.IOUtils;
import org.json.JSONArray;
import org.json.JSONObject;
import org.telegram.telegrambots.bots.TelegramLongPollingBot;
import org.telegram.telegrambots.meta.api.methods.send.SendMessage;
import org.telegram.telegrambots.meta.api.objects.Update;
import org.telegram.telegrambots.meta.exceptions.TelegramApiException;

public class Bot extends TelegramLongPollingBot{

	@Override
	public String getBotUsername() {
		return "JavaBot";
	}

	@Override
	public void onUpdateReceived(Update update) {
		if (update.hasMessage() && update.getMessage().hasText()) {
			if (update.getMessage().getText().toLowerCase().startsWith("/t")) {
				
				String message = update.getMessage().getText().toLowerCase().replace("/t ", "");
				
				String[] requests = message.split(" - ");
				
				String sens = requests[0].toUpperCase().replace(" ", "+");
				String arret = requests[1].toUpperCase().replace(" ", "+");

				String sensMessage = requests[0];
				String arretMessage = requests[1];
				
				StringBuilder builder = new StringBuilder();
				
				builder.append("https://data.angers.fr/api/records/1.0/search/?dataset=bus-tram-circulation-passages&rows=300&sort=-arrivee&facet=mnemoligne&facet=nomligne&facet=dest&facet=mnemoarret&facet=nomarret&facet=numarret");
				builder.append("&refine.mnemoligne=A");
				builder.append("&refine.dest=" + sens);
				builder.append("&refine.nomarret=" + arret);
				

				try {
					URL url = new URL(builder.toString());
					
					HttpURLConnection connection = (HttpURLConnection)url.openConnection();
					connection.setRequestMethod("GET");
					connection.connect();
					
					StringWriter writer = new StringWriter();
					IOUtils.copy(connection.getInputStream(), writer, "UTF-8");
					String stringResponse = writer.toString();
					
					JSONObject jsonResponse = new JSONObject(stringResponse);
					
					JSONArray trams = (JSONArray) jsonResponse.get("records");
					
					List<Date> nextTrams = new ArrayList<>();
					
					for (Object tram : trams) {
						JSONObject thisTram = (JSONObject) tram;
						JSONObject thisField = (JSONObject) thisTram.get("fields");
						
						Calendar thisTramTime = Calendar.getInstance();
						Calendar currentTime = Calendar.getInstance();
						
						String thisDate = (String) thisField.get("arrivee");
						
						String date = thisDate.split("T")[0];
						String time = thisDate.split("T")[1].split("\\+")[0];
						
						thisTramTime.set(
								Integer.parseInt(date.split("-")[0]), 
								Integer.parseInt(date.split("-")[1]) - 1, 
								Integer.parseInt(date.split("-")[2]), 
								Integer.parseInt(time.split(":")[0]), 
								Integer.parseInt(time.split(":")[1]), 
								Integer.parseInt(time.split(":")[2]));
						
						if (thisTramTime.getTime().after(currentTime.getTime())) {
							nextTrams.add(thisTramTime.getTime());
						}
					}
						
					DateFormat formatter = new SimpleDateFormat("HH:mm:ss");
	
			        String message_text = "Prochain tram vers " + sensMessage + " depuis " + arretMessage + " : " + formatter.format(nextTrams.get(0));
			        long chat_id = update.getMessage().getChatId();
	
			        SendMessage messageSend = new SendMessage().setChatId(chat_id).setText(message_text);
		        
		        
		            execute(messageSend);
		        } catch (TelegramApiException | IOException e) {
		            e.printStackTrace();
		        }
			} else {
				try {
					String message_text = "Le message doit être écrit au format suivant : /t sens - arret";
			        long chat_id = update.getMessage().getChatId();
			    	
			        SendMessage messageSend = new SendMessage().setChatId(chat_id).setText(message_text);
		        
		        
		            execute(messageSend);
		        } catch (TelegramApiException e) {
		            e.printStackTrace();
		        }
			}
	        
	    }
	}

	@Override
	public String getBotToken() {
		return "930301457:AAGm_8NQBCI2eRdSj3n8WpBzJ8ZWFj56YmA";
	}

}
