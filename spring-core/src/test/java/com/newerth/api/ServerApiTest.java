package com.newerth.api;

import com.newerth.core.Reference;
import com.newerth.core.Updater;
import com.newerth.core.Utils;
import com.newerth.core.entities.Player;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.http.MediaType;
import org.springframework.test.context.junit4.SpringRunner;
import org.springframework.test.web.servlet.MockMvc;

import java.util.ArrayList;
import java.util.List;

import static org.mockito.BDDMockito.given;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.put;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.content;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

@RunWith(SpringRunner.class)
@WebMvcTest(ServerApi.class)
public class ServerApiTest {

	@Autowired
	private MockMvc mvc;

	@MockBean
	private Reference ref;

	@MockBean
	private Updater updater;

	private static final String json = "{\"accuracyStats\": {\"lastShots\": 10, \"lastFrags\": 5, \"lastHits\": 5}, " +
			"\"uid\": 1, \"lastUsedName\": \"Mike\"}";

	// {"Players": [{"uid" : 1, "lastUsedName" : "Mike","accuracyStats" : {"lastShots" : 10,"lastHits" : 5,"lastFrags" : 5}},
	// 			    {"uid" : 2, "lastUsedName" : "John","accuracyStats" : {"lastShots" : 4,"lastHits" : 1,"lastFrags" : 1}}]}
	private static final String jsonArray = "{\"Players\": [{\"uid\" : 1, \"lastUsedName\" : \"Mike\",\"accuracyStats\":" +
			" {\"lastShots\" : 10,\"lastHits\" : 5,\"lastFrags\" : 5}}, {\"uid\" : 2, \"lastUsedName\" : \"John\"," +
			"\"accuracyStats\" : {\"lastShots\" : 4,\"lastHits\" : 1,\"lastFrags\" : 1}}]}";

	@Test
	public void serverApiMessage() {
		try {
			this.mvc.perform(get("/stats/server")).andExpect(status().isOk())
					.andExpect(content().string("Internal Server API"));
		} catch (Exception e) {
			e.printStackTrace();
		}
	}

	@Test
	public void saveOne() {
		given(this.updater.saveOrUpdatePlayer(new Player(1L)))
				.willReturn(true);
		try {
			this.mvc.perform(
					put("/stats/server/player/put")
							.contentType(MediaType.APPLICATION_JSON)
							.content(json))
					.andExpect(status().isOk())
					.andExpect(content().string("true"));
		} catch (Exception e) {
			e.printStackTrace();
		}
	}

	@Test
	public void saveMany() {
		List<Player> players = new ArrayList<>();
		players.add(new Player(1L));
		players.add(new Player(2L));
		given(this.updater.saveOrUpdatePlayers(players))
				.willReturn(true);
		try {
			this.mvc.perform(
					put("/stats/server/players/put")
							.contentType(MediaType.APPLICATION_JSON)
							.content(jsonArray))
					.andExpect(status().isOk())
					.andExpect(content().string("true"));
		} catch (Exception e) {
			e.printStackTrace();
		}
	}
}
