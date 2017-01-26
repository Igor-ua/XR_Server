package com.newerth.core;

import com.newerth.core.repository.AccuracyRepository;
import com.newerth.core.repository.LastAccuracyRepository;
import com.newerth.core.repository.PlayerRepository;
import com.newerth.core.entities.AccuracyStats;
import com.newerth.core.entities.LastAccuracyStats;
import com.newerth.core.entities.Player;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;

/**
 * Service that only _gets_ information from the DB
 */
@Service
public class Reference {

	private PlayerRepository playerDAO;
	private AccuracyRepository accuracyDAO;
	private LastAccuracyRepository lastAccuracyDAO;

	@Autowired
	private void setPlayerDAO(PlayerRepository jpaPlayerDAO) {
		this.playerDAO = jpaPlayerDAO;
	}

	@Autowired
	private void setAccuracyDAO(AccuracyRepository jpaAccuracyDAO) {
		this.accuracyDAO = jpaAccuracyDAO;
	}

	@Autowired
	private void setLastAccuracyDAO(LastAccuracyRepository jpaLastAccuracyDAO) {
		this.lastAccuracyDAO = jpaLastAccuracyDAO;
	}

	/**
	 * Gets player by his UID
	 */
	public Player findPlayerByUid(Long uid) {
		return playerDAO.findByUid(uid);
	}

	/**
	 * Get general info about the player by his UID
	 */
	public AccuracyStats findPlayerAccuracy(Long uid) {
		Player p = playerDAO.findByUid(uid);
		if (p != null) {
			return p.getAccuracyStats();
		}
		return null;
	}


	/**
	 * Get info about the last game of the player by his UID
	 */
	public LastAccuracyStats findPlayerLastAccuracy(Long uid) {
		Player p = playerDAO.findByUid(uid);
		if (p != null) {
			return lastAccuracyDAO.findByPlayer(p);
		}
		return null;
	}

	/**
	 * Find all players
	 */
	public List<Player> findAllPlayers() {
		return playerDAO.findAll();
	}
}
