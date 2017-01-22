package com.newerth.api;

import com.fasterxml.jackson.annotation.JsonView;
import com.newerth.core.DataService;
import com.newerth.core.Utils;
import com.newerth.core.View;
import com.newerth.core.entities.Player;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import javax.servlet.http.HttpServletRequest;
import java.util.List;

@RestController
@RequestMapping("/stats")
public class StatsAPI {
	@Autowired
	private DataService service;

	@RequestMapping("")
	public String index(HttpServletRequest request) {
		Utils.logRequest(request, this.getClass());
		return "Internal filtered stats API";
	}

	@RequestMapping(
			value = "/save",
			method = RequestMethod.POST)
	@ResponseBody
	public boolean savePlayer(
			@RequestParam("uid") Long uid,
			@RequestParam("lastUsedName") String lastName,
			HttpServletRequest request) {
		Utils.logRequest(request, this.getClass());
		Player player = new Player();
		player.setUid(uid);
		player.setLastUsedName(lastName);
		return service.saveOrUpdate(player);
	}

	@RequestMapping(
			value = "/all",
			method = RequestMethod.GET)
	@JsonView(View.Summary.class)
	public List<Player> findAll(HttpServletRequest request) {
		Utils.logRequest(request, this.getClass());
		return service.findAll();
	}

	@RequestMapping(
			value = "/one",
			params = {"uid"},
			method = RequestMethod.GET)
	@ResponseBody
	public Player findOne(@RequestParam(value = "uid") long uid, HttpServletRequest request) {
		Utils.logRequest(request, this.getClass());
		return service.findOne(uid);
	}
}
