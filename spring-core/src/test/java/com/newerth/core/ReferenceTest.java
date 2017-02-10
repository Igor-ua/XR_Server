package com.newerth.core;

import com.newerth.core.entities.Awards;
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

import java.util.List;

import static org.assertj.core.api.Assertions.assertThat;

@RunWith(SpringRunner.class)
@ContextConfiguration
@DataJpaTest(showSql = false)
@ComponentScan("com.newerth.core")
@AutoConfigureTestDatabase(connection = EmbeddedDatabaseConnection.H2)
public class ReferenceTest {

	@Autowired
	private TestEntityManager entityManager;

	@Autowired
	private Reference ref;

	private Player player;

	// Runs before every test
	@Before
	public void setup() {
		this.player = new Player(1L);
		player.setLastUsedName("Mike");
		player.setAccuracyStats(10, 5, 5);
	}

	@Test
	public void findPlayerByUid() {
		Player p = player;
		this.entityManager.persist(p);
		assertThat(ref.findPlayerByUid(p.getUid()).getUid()).isEqualTo(p.getUid());
	}

	@Test
	public void findPlayerByName() {
		Player p = player;
		this.entityManager.persist(p);
		assertThat(ref.findPlayerByName(p.getLastUsedName()).getLastUsedName())
				.isEqualTo(p.getLastUsedName());
	}

	@Test
	public void findAllPlayers() {
		Player p1 = new Player(1L);
		Player p2 = new Player(2L);
		this.entityManager.persist(p1);
		this.entityManager.persist(p2);
		assertThat(ref.findAllPlayers().size()).isEqualTo(2);
	}

	@Test
	public void findTopAimbots() {
		Player p1 = new Player(1L);
		Player p2 = new Player(2L);
		p1.setAwards(1,1,1,1,1,1);
		this.entityManager.persist(p1);
		p1.setAwards(1,1,1,1,1,1);
		p2.setAwards(1,1,1,1,1,1);
		this.entityManager.persist(p1);
		this.entityManager.persist(p2);
		assertThat(ref.findTopAimbots());
		assertThat(ref.findTopSadists());
		assertThat(ref.findTopSurvivors());
		assertThat(ref.findTopRippers());
		assertThat(ref.findTopMvps());
		assertThat(ref.findTopPhoes());
	}
}
