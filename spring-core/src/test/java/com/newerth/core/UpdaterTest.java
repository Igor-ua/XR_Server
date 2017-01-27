package com.newerth.core;

import com.newerth.core.entities.Player;
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
import static com.newerth.DataPreparer.*;

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

	@Test
	public void saveOrUpdatePlayer() {
		Player p1 = getPlayerWithFields(1L);
		assertThat(updater.saveOrUpdatePlayer(p1));
		p1 = ref.findPlayerByUid(p1.getUid());

		p1.setAccuracyStats(4, 1, 1);
		assertThat(updater.saveOrUpdatePlayer(p1));
		p1 = ref.findPlayerByUid(p1.getUid());
		assertThat(p1.getAccuracyStats().getAccumulatedAccuracyPercent()).isEqualTo(43);

		p1.setAccuracyStats(4 , 2, 2);
		updater.saveOrUpdatePlayer(p1);
		p1 = ref.findPlayerByUid(p1.getUid());
		assertThat(p1.getAccuracyStats().getAccumulatedAccuracyPercent()).isEqualTo(44);
	}

	@Test
	public void saveOrUpdatePlayers() {
		Player p1 = getPlayerWithFields(1L);
		Player p2 = getPlayerWithFields(2L);
		List<Player> players = new ArrayList<>();
		players.add(p1);
		players.add(p2);
		assertThat(updater.saveOrUpdatePlayers(players));
	}
}
