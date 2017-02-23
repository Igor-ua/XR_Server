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
	private static final String SERVICE_NAME = "Internal Server API";

	@Autowired
	private void setUpdater(Updater updater) {
		this.updater = updater;
	}

	@RequestMapping("")
	public String index(HttpServletRequest request) {
		Utils.logRequest(request, this.getClass());
		return SERVICE_NAME;
	}

	@RequestMapping(
			value = "/player/put",
			method = RequestMethod.PUT)
	@ResponseBody
	@JsonView(View.Summary.class)
	public boolean saveOne(
			@RequestBody String body,
			HttpServletRequest request) {
		Utils.logRequest(request, body, this.getClass());
		return updater.saveOrUpdatePlayer(Utils.getPlayerFromJson(body));
	}

	@RequestMapping(
			value = "/players/put",
			method = RequestMethod.PUT)
	@ResponseBody
	@JsonView(View.Summary.class)
	public boolean saveMany(
			@RequestBody String body,
			HttpServletRequest request) {
		Utils.logRequest(request, body, this.getClass());
		return updater.saveOrUpdatePlayers(Utils.getListOfPlayersFromJson(body));
	}

	@RequestMapping(
			value = "/map-stats/post",
			method = RequestMethod.POST)
	@ResponseBody
	@JsonView(View.Summary.class)
	public boolean saveMapStats(
			@RequestBody String body,
			HttpServletRequest request) {
		Utils.logRequest(request, body, this.getClass());
		return updater.saveMapStats(Utils.getMapStatsFromJson(body));
	}

}