package com.newerth.api;

import com.fasterxml.jackson.annotation.JsonView;
import com.newerth.core.Updater;
import com.newerth.core.Utils;
import com.newerth.core.View;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;
import javax.servlet.http.HttpServletRequest;

/**
 * Private API to make any changes in the DB
 */
@RestController
@RequestMapping("/stats/server")
public class ServerApi {

	private Updater updater;

	@Autowired
	private void setUpdater(Updater updater) {
		this.updater = updater;
	}

	@RequestMapping(
			value = "/put/one",
			method = RequestMethod.PUT)
	@ResponseBody
	@JsonView(View.Summary.class)
	public boolean savePlayer(
			@RequestBody String body,
			HttpServletRequest request) {
		Utils.logRequest(request, body, this.getClass());
		return updater.saveOrUpdatePlayer(Utils.getPlayerFromJson(body));
	}

	@RequestMapping(
			value = "/put/many",
			method = RequestMethod.PUT)
	@ResponseBody
	@JsonView(View.Summary.class)
	public boolean savePlayers(
			@RequestBody String body,
			HttpServletRequest request) {
		Utils.logRequest(request, body, this.getClass());
		return updater.saveOrUpdatePlayers(Utils.getListOfPlayersFromJson(body));
	}

}
