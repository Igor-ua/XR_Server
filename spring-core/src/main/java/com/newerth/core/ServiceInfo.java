package com.newerth.core;

import com.newerth.core.dao.JPAAccuracyDAO;
import com.newerth.core.dao.JPALastAccuracyDAO;
import com.newerth.core.dao.JPAPlayerDAO;
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
public class ServiceInfo {

	private JPAPlayerDAO playerDAO;
	private JPAAccuracyDAO accuracyDAO;
	private JPALastAccuracyDAO lastAccuracyDAO;

	@Autowired
	private void setPlayerDAO(JPAPlayerDAO jpaPlayerDAO) {
		this.playerDAO = jpaPlayerDAO;
	}

	@Autowired
	private void setAccuracyDAO(JPAAccuracyDAO jpaAccuracyDAO) {
		this.accuracyDAO = jpaAccuracyDAO;
	}

	@Autowired
	private void setLastAccuracyDAO(JPALastAccuracyDAO jpaLastAccuracyDAO) {
		this.lastAccuracyDAO = jpaLastAccuracyDAO;
	}

	/**
	 * Get player by his UID
	 */
	public Player findPlayer(Long uid) {
		return playerDAO.findByUid(uid);
	}


	/**
	 * Get general info about the player by his UID
	 */
	public AccuracyStats findPlayerAccuracy(Long uid) {
		Player p = findPlayer(uid);
		if (p != null) {
			return accuracyDAO.findByPlayer(p);
		}
		return null;
	}


	/**
	 * Get info about the last game of the player by his UID
	 */
	public LastAccuracyStats findPlayerLastAccuracy(Long uid) {
		Player p = findPlayer(uid);
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
