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
 * Service for changing information in the DB
 */
@Service
public class Updater {

	private JPAPlayerDAO playerDAO;
	private JPAAccuracyDAO accuracyDAO;
	private JPALastAccuracyDAO lastAccuracyDAO;
	private Informer informer;

	@Autowired
	private void setPlayerDAO(JPAPlayerDAO jpaPlayerDAO) {
		this.playerDAO = jpaPlayerDAO;
	}

	@Autowired
	private void setLastAccuracyDAO(JPALastAccuracyDAO jpaLastAccuracyDAO) {
		this.lastAccuracyDAO = jpaLastAccuracyDAO;
	}

	@Autowired
	private void setAccuracyDAO(JPAAccuracyDAO jpaAccuracyDAO) {
		this.accuracyDAO = jpaAccuracyDAO;
	}

	@Autowired
	private void setInformer(Informer informer){
		this.informer = informer;
	}

	/**
	 * Saves new player or updates old player if he exists
	 */
	public boolean saveOrUpdatePlayer(Player player) {
		Player p = informer.findPlayer(player.getUid());
		if (p != null) {
			player.setId(p.getId());
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
			Player p = informer.findPlayer(player.getUid());
			if (p != null) {
				player.setId(p.getId());
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
		AccuracyStats as = informer.findPlayerAccuracy(accuracy.getPlayer().getUid());
		if (as != null) {
			accuracy.setPlayer(informer.findPlayer(as.getPlayer().getUid()));
		}
		try {
			accuracyDAO.save(accuracy);
			return true;
		} catch (RuntimeException e) {
			// ignored; fix it
		}
		return false;
	}

	/**
	 * Saves or updates last accuracy for the player
	 */
	public boolean saveOrUpdateLastAccuracy(LastAccuracyStats lastAccuracy) {
		saveOrUpdatePlayer(lastAccuracy.getPlayer());
		LastAccuracyStats las = informer.findPlayerLastAccuracy(lastAccuracy.getPlayer().getUid());
		if (las != null) {
			lastAccuracy.setPlayer(informer.findPlayer(las.getPlayer().getUid()));
		}
		try {
			lastAccuracyDAO.save(lastAccuracy);
			return true;
		} catch (RuntimeException e) {
			// ignored; fix it
		}
		return false;
	}
}
