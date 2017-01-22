package com.newerth.core;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Service;

import javax.servlet.http.HttpServletRequest;

@Service
public class Utils {

	public static void logRequest(HttpServletRequest request, Class clazz) {
		Logger log = LoggerFactory.getLogger(clazz);
		log.info("Request: "
				+ "IP: [" + request.getRemoteAddr() + "] "
				+ "URL: " + request.getRequestURL()
		);
	}
}
