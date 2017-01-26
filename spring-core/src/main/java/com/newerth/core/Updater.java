package com.newerth.core;

import com.newerth.core.repository.AccuracyRepository;
import com.newerth.core.repository.PlayerRepository;
import com.newerth.core.entities.AccuracyStats;
import com.newerth.core.entities.Player;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;

/**
 * Service for changing information in the DB
 */
@Service
public class Updater {

	private PlayerRepository playerDAO;
	private AccuracyRepository accuracyDAO;
	private Reference reference;

	@Autowired
	private void setPlayerDAO(PlayerRepository jpaPlayerDAO) {
		this.playerDAO = jpaPlayerDAO;
	}

	@Autowired
	private void setAccuracyDAO(AccuracyRepository jpaAccuracyDAO) {
		this.accuracyDAO = jpaAccuracyDAO;
	}

	@Autowired
	private void setReference(Reference reference){
		this.reference = reference;
	}

	/**
	 * Saves new player or updates old player if he exists
	 */
	public boolean saveOrUpdatePlayer(Player player) {
		Player p = reference.findPlayerByUid(player.getUid());
		if (p != null) {
			player.setUid(p.getUid());
		}
		try {
			playerDAO.save(player);
			return true;
		} catch (RuntimeException e) {
//			e.printStackTrace();
//			ignored; fix it
		}
		return false;
	}

	/**
	 * Saves or updates the list of the players
	 */
	public boolean saveOrUpdatePlayers(List<Player> players) {
		players.forEach(player -> {
			Player p = reference.findPlayerByUid(player.getUid());
			if (p != null) {
				player.setUid(p.getUid());
			}
		});
		try {
			playerDAO.save(players);
			return true;
		} catch (RuntimeException e) {
			// ignored; fix it
		}
		return false;
	}

	/**
	 * Saves or updates accuracy for the player
	 */
	public boolean saveOrUpdateAccuracy(AccuracyStats accuracy) {
		saveOrUpdatePlayer(accuracy.getPlayer());
		AccuracyStats as = reference.findPlayerAccuracy(accuracy.getPlayer().getUid());
		if (as != null) {
			accuracy.setPlayer(reference.findPlayerByUid(as.getPlayer().getUid()));
		}
		try {
			accuracyDAO.save(accuracy);
			return true;
		} catch (RuntimeException e) {
			// ignored; fix it
		}
		return false;
	}
}
