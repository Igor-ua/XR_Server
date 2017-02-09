package com.newerth.core;

import com.newerth.core.entities.Awards;
import com.newerth.core.repository.AwardsRepository;
import com.newerth.core.repository.PlayerRepository;
import com.newerth.core.entities.Player;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.ArrayList;
import java.util.List;

/**
 * Service that only _gets_ information from the DB
 */
@Service
public class Reference {

	private PlayerRepository playerRepo;
	private AwardsRepository awardsRepo;

	@Autowired
	private void setPlayerRepo(PlayerRepository repository) {
		this.playerRepo = repository;
	}

	@Autowired
	private void setAwardsRepo(AwardsRepository repository) {
		this.awardsRepo = repository;
	}

	/**
	 * Gets player by his UID
	 */
	public Player findPlayerByUid(Long uid) {
		return playerRepo.findByUid(uid);
	}

	/**
	 * Gets player by his Name
	 */
	public Player findPlayerByName(String name) {
		return playerRepo.findByLastUsedName(name);
	}

	/**
	 * Find all players
	 */
	public List<Player> findAllPlayers() {
		return playerRepo.findAll();
	}

	/**
	 * Finds top Aimbots
	 */
	public List<Player> findTopAimbots() {
		return getPlayersFromAwards(awardsRepo.findTopAimbots());
	}

	/**
	 * Finds top Sadists
	 */
	public List<Player> findTopSadists() {
		return getPlayersFromAwards(awardsRepo.findTopSadists());
	}

	/**
	 * Finds top MVPs
	 */
	public List<Player> findTopMvps() {
		return getPlayersFromAwards(awardsRepo.findTopMvps());
	}

	/**
	 * Finds top Survivors
	 */
	public List<Player> findTopSurvivors() {
		return getPlayersFromAwards(awardsRepo.findTopSurvivors());
	}

	/**
	 * Finds top Rippers
	 */
	public List<Player> findTopRippers() {
		return getPlayersFromAwards(awardsRepo.findTopRippers());
	}

	/**
	 * Finds top Phoes
	 */
	public List<Player> findTopPhoes() {
		return getPlayersFromAwards(awardsRepo.findTopPhoes());
	}

	private List<Player> getPlayersFromAwards(List<Awards> awards) {
		List<Player> players = new ArrayList<>();
		awards.forEach(award -> players.add(award.getPlayer()));
		return players;
	}
}
