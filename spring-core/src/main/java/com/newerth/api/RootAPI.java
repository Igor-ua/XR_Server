package com.newerth.api;

import com.newerth.core.Updater;
import com.newerth.core.Utils;
import com.newerth.core.entities.Player;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.autoconfigure.web.ErrorController;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import javax.servlet.http.HttpServletRequest;

@RestController
public class RootAPI implements ErrorController {

	private static final String PATH = "/error";

	@RequestMapping("/")
	public String index(HttpServletRequest request) {
		Utils.logRequest(request, this.getClass());

		test();

		return "XR Server instagib API";
	}

	@Autowired
	private Updater updater;

	private void test() {
		Player p = new Player();
		p.setUid(123L);
		p.setLastUsedName("Mike");
		updater.saveOrUpdatePlayer(p);
	}

	@RequestMapping(value = PATH)
	public String error(HttpServletRequest request) {
		Utils.logRequest(request, this.getClass());
		return "Error";
	}

	@Override
	public String getErrorPath() {
		return PATH;
	}
}
