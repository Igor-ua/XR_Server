package com.newerth.core;

import com.newerth.core.entities.Player;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.orm.jpa.DataJpaTest;
import org.springframework.boot.test.autoconfigure.orm.jpa.TestEntityManager;
import org.springframework.context.annotation.ComponentScan;
import org.springframework.test.context.ContextConfiguration;
import org.springframework.test.context.junit4.SpringRunner;

import static org.assertj.core.api.Assertions.assertThat;
import static com.newerth.DataPreparer.*;

@RunWith(SpringRunner.class)
@ContextConfiguration
@DataJpaTest(showSql = false)
@ComponentScan("com.newerth.core")
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
		System.out.println("p1_before: " + p1);
		assertThat(updater.saveOrUpdatePlayer(p1));
		p1 = ref.findPlayerByUid(p1.getUid());
		System.out.println("p1_after: " + p1);

		p1.setAccuracyStats(4, 1, 1);
		assertThat(updater.saveOrUpdatePlayer(p1));
		p1 = ref.findPlayerByUid(p1.getUid());
		System.out.println(p1);
		assertThat(p1.getAccuracyStats().getAccumulatedAccuracyPercent()).isEqualTo(43);

		p1.setAccuracyStats(4 , 2, 2);
		updater.saveOrUpdatePlayer(p1);
		p1 = ref.findPlayerByUid(p1.getUid());
		System.out.println(p1);
		assertThat(p1.getAccuracyStats().getAccumulatedAccuracyPercent()).isEqualTo(44);
	}

	@Test
	public void saveOrUpdatePlayers() {

	}
}
