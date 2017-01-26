import com.newerth.core.entities.Player;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.springframework.boot.test.context.SpringBootContextLoader;
import org.springframework.test.context.ContextConfiguration;
import org.springframework.test.context.junit4.SpringJUnit4ClassRunner;

import static org.assertj.core.api.Assertions.assertThat;

@RunWith(SpringJUnit4ClassRunner.class)
@ContextConfiguration(classes=Player.class, loader=SpringBootContextLoader.class)
public class PlayerTest {
	@Test
	public void createPlayer() {
		Player p = new Player();
		assertThat(p.getUid() == 0L);
	}
}
