package com.newerth.core;

import com.newerth.core.entities.MapStats;
import com.newerth.core.entities.Player;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.autoconfigure.jdbc.EmbeddedDatabaseConnection;
import org.springframework.boot.test.autoconfigure.orm.jpa.AutoConfigureTestDatabase;
import org.springframework.boot.test.autoconfigure.orm.jpa.DataJpaTest;
import org.springframework.boot.test.autoconfigure.orm.jpa.TestEntityManager;
import org.springframework.context.annotation.ComponentScan;
import org.springframework.test.context.ContextConfiguration;
import org.springframework.test.context.junit4.SpringRunner;

import java.util.ArrayList;
import java.util.List;

import static org.assertj.core.api.Assertions.assertThat;

@RunWith(SpringRunner.class)
@ContextConfiguration
@DataJpaTest(showSql = false)
@ComponentScan("com.newerth.core")
@AutoConfigureTestDatabase(connection = EmbeddedDatabaseConnection.H2)
public class UpdaterTest {

	@Autowired
	private TestEntityManager entityManager;

	@Autowired
	private Updater updater;

	@Autowired
	private Reference ref;

	@Autowired
	private MapStats mapStats;

	private Player player;

	// Runs before every test
	@Before
	public void setup() {
		this.player = new Player(1L);
		player.setLastUsedName("Mike");
		player.setAccuracyStats(10, 5, 5);
	}

	@Test
	public void saveOrUpdatePlayer() {
		Player player = new Player();
		player.setUid(1L);
		player.setAccuracyStats(4, 1, 1);
		// First save
		assertThat(updater.saveOrUpdatePlayer(player));
		player = ref.findPlayerByUid(player.getUid());
		// 1 * 100 / 4 = 25
		assertThat(player.getAccuracyStats().getAccumulatedAccuracyPercent()).isEqualTo(25);
		// 2 * 100 / 4 = 50
		// 3 * 100 / 8 = 37.5 (Math.round() -> 38)
		player.setAccuracyStats(4 , 2, 2);
		assertThat(player.getAccuracyStats().getLastAccuracyPercent()).isEqualTo(50);
		assertThat(player.getAccuracyStats().getAccumulatedAccuracyPercent()).isEqualTo(38);
		// Second update
		assertThat(updater.saveOrUpdatePlayer(player));
		Player p2 = ref.findPlayerByUid(1L);
		assertThat(p2).isEqualTo(player);
	}

	@Test
	public void saveOrUpdatePlayers() {
		Player p1 = new Player(1L);
		Player p2 = new Player(2L);
		List<Player> players = new ArrayList<>();
		players.add(p1);
		players.add(p2);
		assertThat(updater.saveOrUpdatePlayers(players));
	}

	@Test
	public void saveMapStats() {
		mapStats = new MapStats();
		mapStats.setBlueScore(30);
		mapStats.setRedScore(22);
		mapStats.setMapName("eden2");
		mapStats.setWinner("blue");
		assertThat(updater.saveMapStats(mapStats));
		List<MapStats> ms = ref.findAllMapStats();
		System.out.println(ms);
		assertThat(ms.contains(mapStats));
	}
}
