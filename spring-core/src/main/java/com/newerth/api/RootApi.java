package com.newerth.api;

import com.newerth.core.Utils;
import org.springframework.boot.autoconfigure.web.ErrorController;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import javax.servlet.http.HttpServletRequest;

/**
 * Private API
 */
@RestController
public class RootApi implements ErrorController {

	private static final String SERVICE_NAME = "XR Server instagib API";
	private static final String ERROR_PATH = "/error";
	private static final String ERROR_MSG = "Error/403";

	@RequestMapping("/")
	public String index(HttpServletRequest request) {
		Utils.logRequest(request, this.getClass());
		return SERVICE_NAME;
	}

	@RequestMapping(value = ERROR_PATH)
	public String error(HttpServletRequest request) {
		Utils.logRequest(request, this.getClass());
		return ERROR_MSG;
	}

	@Override
	public String getErrorPath() {
		return ERROR_PATH;
	}
}