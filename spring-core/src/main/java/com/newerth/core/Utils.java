package com.newerth.core;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.ObjectWriter;
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
				+ "METHOD: " + request.getMethod()
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
}
