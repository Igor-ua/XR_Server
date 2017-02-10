package com.newerth.api;

import com.fasterxml.jackson.annotation.JsonView;
import com.newerth.core.Reference;
import com.newerth.core.Utils;
import com.newerth.core.View;
import com.newerth.core.entities.Player;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import javax.servlet.http.HttpServletRequest;
import java.util.List;

/**
 * Private API for clients to _GET_ any kind of information from the DB
 */
@RestController
@RequestMapping("/stats")
public class ClientApi {

	private static final String SERVICE_NAME = "Internal filtered stats API";
	private Reference ref;

	@Autowired
	private void setRef(Reference reference) {
		this.ref = reference;
	}

	@RequestMapping("")
	public String index(HttpServletRequest request) {
		Utils.logRequest(request, this.getClass());
		return SERVICE_NAME;
	}

	@RequestMapping(
			value = "/get/{uid}",
			method = RequestMethod.GET)
	@ResponseBody
	@JsonView(View.Summary.class)
	public Player findOne(@PathVariable("uid") long uid, HttpServletRequest request) {
		Utils.logRequest(request, this.getClass());
		return ref.findPlayerByUid(uid);
	}

	@RequestMapping(
			value = "/get/name/{name}",
			method = RequestMethod.GET)
	@ResponseBody
	@JsonView(View.Summary.class)
	public Player findOneByName(@PathVariable("name") String name, HttpServletRequest request) {
		Utils.logRequest(request, this.getClass());
		return ref.findPlayerByName(name);
	}

	@RequestMapping(
			value = "/get/top/aimbots",
			method = RequestMethod.GET)
	@ResponseBody
	@JsonView(View.Summary.class)
	public List<Player> findTopAimbots(HttpServletRequest request) {
		Utils.logRequest(request, this.getClass());
		return ref.findTopAimbots();
	}

	@RequestMapping(
			value = "/get/top/sadists",
			method = RequestMethod.GET)
	@ResponseBody
	@JsonView(View.Summary.class)
	public List<Player> findTopSadists(HttpServletRequest request) {
		Utils.logRequest(request, this.getClass());
		return ref.findTopSadists();
	}

	@RequestMapping(
			value = "/get/top/survivors",
			method = RequestMethod.GET)
	@ResponseBody
	@JsonView(View.Summary.class)
	public List<Player> findTopSurvivors(HttpServletRequest request) {
		Utils.logRequest(request, this.getClass());
		return ref.findTopSurvivors();
	}

	@RequestMapping(
			value = "/get/top/rippers",
			method = RequestMethod.GET)
	@ResponseBody
	@JsonView(View.Summary.class)
	public List<Player> findTopRippers(HttpServletRequest request) {
		Utils.logRequest(request, this.getClass());
		return ref.findTopRippers();
	}

	@RequestMapping(
			value = "/get/top/phoes",
			method = RequestMethod.GET)
	@ResponseBody
	@JsonView(View.Summary.class)
	public List<Player> findTopPhoes(HttpServletRequest request) {
		Utils.logRequest(request, this.getClass());
		return ref.findTopPhoes();
	}

	@RequestMapping(
			value = "/get/top/mvps",
			method = RequestMethod.GET)
	@ResponseBody
	@JsonView(View.Summary.class)
	public List<Player> findTopMvps(HttpServletRequest request) {
		Utils.logRequest(request, this.getClass());
		return ref.findTopMvps();
	}
}
