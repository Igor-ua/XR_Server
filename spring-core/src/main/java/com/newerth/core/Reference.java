package com.newerth.core;

import com.newerth.core.repository.PlayerRepository;
import com.newerth.core.entities.Player;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;

/**
 * Service that only _gets_ information from the DB
 */
@Service
public class Reference {

	private PlayerRepository playerRepo;

	@Autowired
	private void setPlayerRepo(PlayerRepository repository) {
		this.playerRepo = repository;
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
}
