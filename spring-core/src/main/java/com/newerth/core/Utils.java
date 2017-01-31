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
			JsonNode root = mapper.readTree(json);
			player.setUid(root.at("/uid").longValue());
			player.setLastUsedName(root.at("/lastUsedName").asText());
			player.setAccuracyStats(
					root.at("/accuracyStats/lastShots").asInt(),
					root.at("/accuracyStats/lastHits").asInt(),
					root.at("/accuracyStats/lastFrags").asInt()
			);
		} catch (IOException e) {
			e.printStackTrace();
		}
		return player;
	}
}
