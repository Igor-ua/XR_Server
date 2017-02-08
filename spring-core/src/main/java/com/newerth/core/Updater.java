package com.newerth.core;

import com.newerth.core.repository.PlayerRepository;
import com.newerth.core.entities.Player;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.ArrayList;
import java.util.List;

/**
 * Service for changing information in the DB
 */
@Service
public class Updater {

	private PlayerRepository playerRepo;
	private Reference ref;
	private static Logger log = LoggerFactory.getLogger(Updater.class);

	@Autowired
	private void setPlayerRepo(PlayerRepository repository) {
		this.playerRepo = repository;
	}

	@Autowired
	private void setReference(Reference reference){
		this.ref = reference;
	}

	/**
	 * Saves new player or updates old player if he exists
	 */
	public boolean saveOrUpdatePlayer(Player player) {
		Player found = ref.findPlayerByUid(player.getUid());
		if (found != null) {
			found.setAccuracyStats(
					player.getAccuracyStats().getLastShots(),
					player.getAccuracyStats().getLastHits(),
					player.getAccuracyStats().getLastFrags());
			found.setAwards(
					player.getAwards().getLastMvp(),
					player.getAwards().getLastSadist(),
					player.getAwards().getLastSurvivor(),
					player.getAwards().getLastRipper(),
					player.getAwards().getLastPhoe(),
					player.getAwards().getLastAimbot()
					);
			player = found;
		}
		try {
			playerRepo.save(player);
			return true;
		} catch (RuntimeException e) {
			log.info("Error during saving a player: " + player);
		}
		return false;
	}

	/**
	 * Saves or updates the list of the players
	 */
	public boolean saveOrUpdatePlayers(List<Player> players) {
		List<Player> playersToSave = new ArrayList<>();
		players.forEach(player -> {
			Player found = ref.findPlayerByUid(player.getUid());
			if (found != null) {
				found.setAccuracyStats(
						player.getAccuracyStats().getLastShots(),
						player.getAccuracyStats().getLastHits(),
						player.getAccuracyStats().getLastFrags());
				found.setAwards(
						player.getAwards().getLastMvp(),
						player.getAwards().getLastSadist(),
						player.getAwards().getLastSurvivor(),
						player.getAwards().getLastRipper(),
						player.getAwards().getLastPhoe(),
						player.getAwards().getLastAimbot()
				);
				player = found;
			}
			playersToSave.add(player);
		});
		try {
			playerRepo.save(playersToSave);
			return true;
		} catch (RuntimeException e) {
			StringBuilder sb = new StringBuilder();
			players.forEach(p -> sb.append(" ").append(p.getUid()));
			log.info("Error during saving a list of the players with UIDs:" + sb.toString());
		}
		return false;
	}
}
