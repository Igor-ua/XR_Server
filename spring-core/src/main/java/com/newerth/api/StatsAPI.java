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
			value = "/add",
			method = RequestMethod.GET)
	@ResponseBody
	public boolean savePlayer(HttpServletRequest request) {
		Utils.logRequest(request, this.getClass());
		Player player = new Player();
		return service.saveOne(player);
	}

	@RequestMapping(
			value = "/all",
			method = RequestMethod.GET)
	@JsonView(View.Summary.class)
	public List<Player> getPlayers(HttpServletRequest request) {
		Utils.logRequest(request, this.getClass());
		return service.findAll();
	}

	@RequestMapping(
			value = "/one",
			params = {"id"},
			method = RequestMethod.GET)
	@ResponseBody
	public Player findOne(@RequestParam(value = "id") long id, HttpServletRequest request) {
		Utils.logRequest(request, this.getClass());
		return service.findOne(id);
	}
}
