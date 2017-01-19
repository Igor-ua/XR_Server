package com.newerth.api;

import com.fasterxml.jackson.annotation.JsonView;
import com.newerth.core.GameService;
import com.newerth.core.View;
import com.newerth.core.entities.Player;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/stats")
public class StatsAPI {
	@Autowired
	private GameService gameService;

	@RequestMapping(
			value = "/add",
			method = RequestMethod.GET)
	@ResponseBody
	public boolean savePlayer() {
		Player player = new Player();
		return gameService.saveOne(player);
	}

	@RequestMapping(
			value = "/all",
			method = RequestMethod.GET)
	@JsonView(View.Summary.class)
	public List<Player> getPlayers() {
		return gameService.findAll();
	}

	@RequestMapping(
			value = "/one",
			params = {"id"},
			method = RequestMethod.GET)
	@ResponseBody
	public Player findOne(@RequestParam(value = "id") long id) {
		return gameService.findOne(id);
	}
}
