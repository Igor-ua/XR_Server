package com.newerth.core.entities;

import com.newerth.core.repository.PlayerRepository;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.autoconfigure.jdbc.EmbeddedDatabaseConnection;
import org.springframework.boot.test.autoconfigure.orm.jpa.AutoConfigureTestDatabase;
import org.springframework.boot.test.autoconfigure.orm.jpa.DataJpaTest;
import org.springframework.boot.test.autoconfigure.orm.jpa.TestEntityManager;
import org.springframework.dao.DataIntegrityViolationException;
import org.springframework.test.context.ContextConfiguration;
import org.springframework.test.context.junit4.SpringRunner;

import static org.assertj.core.api.Assertions.assertThat;

@RunWith(SpringRunner.class)
@ContextConfiguration
@DataJpaTest(showSql = false)
@AutoConfigureTestDatabase(connection = EmbeddedDatabaseConnection.H2)
public class PlayerTest {

	@Autowired
	private TestEntityManager entityManager;

	@Autowired
	private PlayerRepository repo;

	private Player player;

	// Runs before every test
	@Before
	public void setup() {
		this.player = new Player(1L);
		player.setLastUsedName("Mike");
		player.setAccuracyStats(10, 5, 5);
	}

	@Test
	public void createOne() {
		Player p = new Player();
		assertThat(p.getUid()).isEqualTo(0L);
	}

	@Test
	public void saveOne() {
		Player p = new Player(12345L);
		assertThat(repo.save(p));
	}

	@Test
	public void findOne() {
		Long uid = 123L;
		this.entityManager.persist(new Player(uid));
		assertThat(repo.findByUid(uid).getUid()).isEqualTo(uid);
		assertThat(repo.findByUid(uid).getUid()).isNotEqualTo(12345L);
	}

	@Test
	public void saveWithFields() {
		assertThat(repo.save(player));
	}

	@Test
	public void saveWithFieldsAndFind() {
		Player p1 = player;
		assertThat(repo.save(p1));
		Player p2 = repo.findByUid(p1.getUid());
		System.out.println(p2);
		assertThat(p2).isEqualTo(p1);
	}

	@Test
	public void findAndUpdate() {
		Player p1 = player;
		this.entityManager.persist(p1);
		Player p2 = repo.findByUid(p1.getUid());
		assertThat(p1.getAccuracyStats()).isEqualTo(p2.getAccuracyStats());
	}

	@Test
	public void updateMultipleTimes() {
		Player p1 = player;
		this.entityManager.persist(p1);
		Player p2 = repo.findByUid(p1.getUid());
		p2.getAccuracyStats().setStats(2, 1, 1);
		repo.save(p2);
		p2 = repo.findByUid(p1.getUid());
		p2.getAccuracyStats().setStats(3, 1, 1);
		repo.save(p2);
		p2 = repo.findByUid(p1.getUid());
		assertThat(p2.getAccuracyStats().getAccumulatedShots()).isEqualTo(15);
		assertThat(p2.getAccuracyStats().getAccumulatedHits()).isEqualTo(7);
		assertThat(p2.getAccuracyStats().getAccumulatedFrags()).isEqualTo(7);
		assertThat(p2.getAccuracyStats().getAccumulatedAccuracyPercent()).isEqualTo(47);
		assertThat(p2.getAccuracyStats().getAccumulatedAccuracyPercent()).isNotEqualTo(46);
	}

	@Test(expected = IllegalArgumentException.class)
	public void wrongAccuracyParams() {
		Player p = player;
		p.getAccuracyStats().setStats(10, 20, 5);
	}

	@Test(expected = DataIntegrityViolationException.class)
	public void saveOneTwice() {
		Player p = player;
		System.out.println(p);
		repo.save(p);
		repo.save(p);
	}

	@Test
	public void accuracyGetters() {
		Player p = player;
		AccuracyStats as = p.getAccuracyStats();
		assertThat(as.getLastShots()).isEqualTo(10);
		assertThat(as.getLastHits()).isEqualTo(5);
		assertThat(as.getLastFrags()).isEqualTo(5);
		assertThat(p.getUid()).isEqualTo(1);
	}
}