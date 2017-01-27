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

import static org.assertj.core.api.Assertions.assertThat;
import static com.newerth.DataPreparer.*;

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

	@Test
	public void findPlayerByUid() {
		Player p = getPlayerWithFields();
		this.entityManager.persist(p);
		assertThat(ref.findPlayerByUid(p.getUid()).getUid()).isEqualTo(p.getUid());
	}

	@Test
	public void findPlayerByName() {
		Player p = getPlayerWithFields();
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
}
