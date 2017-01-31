package com.newerth.api;

import com.newerth.core.Updater;
import com.newerth.core.Utils;
import com.newerth.core.entities.Player;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import javax.servlet.ServletException;
import javax.servlet.http.HttpServletRequest;
import java.io.IOException;

/**
 * API to make any changes in the DB
 */
@RestController
@RequestMapping("/stats/server")
public class ServerAPI {

	private Updater updater;

	@Autowired
	private void setUpdater(Updater updater) {
		this.updater = updater;
	}

	@RequestMapping(
			value = "/save",
			method = RequestMethod.POST)
	@ResponseBody
	public boolean savePlayer(
			@RequestBody String body,
			HttpServletRequest request) {
		Utils.logRequest(request, body, this.getClass());
		return false;
	}

}
