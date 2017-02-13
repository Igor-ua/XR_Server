package com.newerth.core;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.ObjectWriter;
import com.newerth.core.entities.Player;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Service;

import javax.servlet.http.HttpServletRequest;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

@Service
public class Utils {

	/**
	 * Template to log http requests
	 */
	public static void logRequest(HttpServletRequest request, Class clazz) {
		Logger log = LoggerFactory.getLogger(clazz);
		log.info("Request: "
				+ "IP: [" + request.getRemoteAddr() + "] "
				+ "URL: " + request.getRequestURL() + " "
				+ "[" + request.getMethod() + "]"
				+ " " + ""
		);
	}

	/**
	 * Template to log http requests
	 */
	public static void logRequest(HttpServletRequest request, String body, Class clazz) {
		Logger log = LoggerFactory.getLogger(clazz);
		log.info("Request: "
				+ "IP: [" + request.getRemoteAddr() + "] "
				+ "URL: " + request.getRequestURL() + " "
				+ "[" + request.getMethod() + "] "
				+ "-> [" + body + "]"
		);
	}

	/**
	 * Converts object to JSON
	 */
	public static String getJsonFromObject(Object obj) {
		ObjectWriter ow = new ObjectMapper().writer().withDefaultPrettyPrinter();
		String json = "";
		try {
			json = ow.writeValueAsString(obj);
		} catch (JsonProcessingException e) {
			e.printStackTrace();
		}
		return json;
	}

	/**
	 * Converts JSON to Object
	 */
	public <T> T getObjectFromJson(String json,  Class<T> type) {
		ObjectMapper mapper = new ObjectMapper();
		Object obj = null;
		try {
			obj = mapper.readValue(json, type);
		} catch (IOException e) {
			e.printStackTrace();
		}
		return type.cast(obj);
	}

	/**
	 * Player JSON structure:
	 *
	 * {
	 *     "uid" : 1,
	 *     "lastUsedName" : "Mike",
	 *     "accuracyStats" : {
	 *         "lastShots" : 10,
	 *         "lastHits" : 5,
	 *         "lastFrags" : 5
	 *     },
	 *     "awards" : {
	 *         "id" : null (auto-generated)
	 *     }
	 * }
	 */
	public static Player getPlayerFromJson(String json) {
		Player player = new Player();
		try {
			ObjectMapper mapper = new ObjectMapper();
			JsonNode node = mapper.readTree(json);
			player = getPlayerFromNode(node);
		} catch (IOException e) {
			e.printStackTrace();
		}
		return player;
	}

	/**
	 * Gets a Player from Json Node
	 */
	public static Player getPlayerFromNode(JsonNode node) {
		Player player = new Player();
		player.setUid(node.at("/uid").longValue());
		player.setClanId(node.at("/clanId").longValue());
		player.setLastUsedName(node.at("/lastUsedName").asText());
		player.setAccuracyStats(
				node.at("/accuracyStats/lastShots").asInt(),
				node.at("/accuracyStats/lastHits").asInt(),
				node.at("/accuracyStats/lastFrags").asInt()
		);
		player.setAwards(
				node.at("/awards/mvp").asInt(),
				node.at("/awards/sadist").asInt(),
				node.at("/awards/survivor").asInt(),
				node.at("/awards/ripper").asInt(),
				node.at("/awards/phoe").asInt(),
				node.at("/awards/aimbot").asInt()
		);
		return player;
	}


	/**
	 * JSON "List<Player> players" structure:
	 *
	 * {
	 * 		"Players":
	 * 					[
	 * 						{"uid": 1, "lastUsedName": "Mike",
	 * 							"accuracyStats": {"lastShots" : 10, "lastHits": 5, "lastFrags": 5}
	 * 						},
	 * 						{"uid": 2, "lastUsedName": "John",
	 * 							"accuracyStats": {"lastShots": 4, "lastHits": 1, "lastFrags": 1}
	 * 						}
	 * 					]
	 * 	}
	 */
	public static List<Player> getListOfPlayersFromJson(String json) {
		List<Player> players = new ArrayList<>();
		try {
			ObjectMapper mapper = new ObjectMapper();
			JsonNode root = mapper.readTree(json);
			root.at("/Players").forEach(node -> {
				Player p = getPlayerFromNode(node);
				players.add(p);
			});
		} catch (IOException e) {
			e.printStackTrace();
		}
		return players;
	}

	public static String objectToJson(Object obj) {
		String result = "";
		try {
			ObjectWriter ow = new ObjectMapper().writer().withDefaultPrettyPrinter();
			result = ow.writeValueAsString(obj);
		} catch (JsonProcessingException e) {
			e.printStackTrace();
		}
		return result;
	}
}
