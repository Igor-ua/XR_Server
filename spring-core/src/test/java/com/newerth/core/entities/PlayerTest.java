package com.newerth.core.entities;

import com.newerth.core.Reference;
import com.newerth.core.Updater;
import com.newerth.core.Utils;
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

import static org.assertj.core.api.Assertions.assertThat;

@RunWith(SpringRunner.class)
@ContextConfiguration
@DataJpaTest(showSql = false)
@ComponentScan("com.newerth.core")
@AutoConfigureTestDatabase(connection = EmbeddedDatabaseConnection.H2)
public class PlayerTest {

	@Autowired
	private TestEntityManager entityManager;

	@Autowired
	private Updater updater;

	@Autowired
	private Reference ref;

	private Player player;

	// Runs before every test
	@Before
	public void setup() {
		this.player = new Player(1L);
		this.player.setClanId(333L);
		player.setLastUsedName("Mike");
		player.setAccuracyStats(10, 5, 5);
		player.setAwards(1, 1, 1, 1,1,1);
	}

	@Test
	public void createOne() {
		Player p = new Player();
		assertThat(p.getUid()).isEqualTo(0L);
	}

	@Test
	public void saveOne() {
		Player p = new Player(12345L);
		assertThat(updater.saveOrUpdatePlayer(p));
	}

	@Test
	public void findOne() {
		Long uid = 1L;
		this.entityManager.persist(player);
		assertThat(ref.findPlayerByUid(uid).getUid()).isEqualTo(uid);
		assertThat(ref.findPlayerByUid(uid).getClanId()).isEqualTo(333L);
		assertThat(ref.findPlayerByUid(uid).getUid()).isNotEqualTo(12345L);
	}

	@Test
	public void saveWithFields() {
		assertThat(updater.saveOrUpdatePlayer(player));
	}

	@Test
	public void saveWithFieldsAndFind() {
		Player p1 = player;
		assertThat(updater.saveOrUpdatePlayer(p1));
		Player p2 = ref.findPlayerByUid(p1.getUid());
		System.out.println(p2);
		assertThat(p2).isEqualTo(p1);
	}

	@Test
	public void findAndUpdate() {
		Player p1 = player;
		this.entityManager.persist(p1);
		Player p2 = ref.findPlayerByUid(p1.getUid());
		assertThat(p1.getAccuracyStats()).isEqualTo(p2.getAccuracyStats());
	}

	@Test
	public void updateMultipleTimes() {
		Player p = player;
		System.out.println(p);
		updater.saveOrUpdatePlayer(p);

		p.setAccuracyStats(4, 1, 1);
		p.setAwards(1,1,1,1,1,1);
		System.out.println(p);
		updater.saveOrUpdatePlayer(p);

		p.setAccuracyStats(4, 2, 2);
		p.setAwards(1,1,1,1,1,1);
		System.out.println(p);
		updater.saveOrUpdatePlayer(p);

		p = ref.findPlayerByUid(player.getUid());
		assertThat(p.getAccuracyStats().getAccumulatedShots()).isEqualTo(18);
		assertThat(p.getAccuracyStats().getAccumulatedHits()).isEqualTo(8);
		assertThat(p.getAccuracyStats().getAccumulatedFrags()).isEqualTo(8);
		assertThat(p.getAccuracyStats().getAccumulatedAccuracyPercent()).isEqualTo(44);
		assertThat(p.getAccuracyStats().getAccumulatedAccuracyPercent()).isNotEqualTo(43);
		assertThat(p.getAwards().getAccumulatedAimbot()).isEqualTo(3);
		assertThat(p.getAwards().getAccumulatedMvp()).isEqualTo(3);
		assertThat(p.getAwards().getAccumulatedPhoe()).isEqualTo(3);
		assertThat(p.getAwards().getAccumulatedRipper()).isEqualTo(3);
		assertThat(p.getAwards().getAccumulatedSadist()).isEqualTo(3);
		assertThat(p.getAwards().getAccumulatedSurvivor()).isEqualTo(3);
	}

	@Test(expected = IllegalArgumentException.class)
	public void wrongAccuracyParams() {
		Player p = player;
		p.getAccuracyStats().setStats(10, 20, 5);
	}

	@Test
	public void saveOneTwice() {
		Player p = player;
		System.out.println(p);
		assertThat(updater.saveOrUpdatePlayer(p));
		assertThat(updater.saveOrUpdatePlayer(p));
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

	@Test
	public void objectToJson() {
		String json = Utils.getJsonFromObject(player);
		System.out.println(json);
	}

	@Test
	public void saveNameValidation() {
		Player p = player;
		p.setLastUsedName("asdASD123890_- ()");
		assertThat(updater.saveOrUpdatePlayer(p));
		p.setLastUsedName("asdASD-_{}()23423  sdf;#$%");
		assertThat(updater.saveOrUpdatePlayer(p));
	}
}