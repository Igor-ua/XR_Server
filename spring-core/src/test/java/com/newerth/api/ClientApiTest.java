package com.newerth.api;

import com.newerth.core.Reference;
import com.newerth.core.Utils;
import com.newerth.core.entities.Player;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.test.context.junit4.SpringRunner;
import org.springframework.test.web.servlet.MockMvc;

import static org.mockito.BDDMockito.*;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.*;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

@RunWith(SpringRunner.class)
@WebMvcTest(ClientApi.class)
public class ClientApiTest {

	@Autowired
	private MockMvc mvc;

	@MockBean
	private Reference ref;

	@Test
	public void clientApiMessage() {
		try {
			this.mvc.perform(get("/stats/")).andExpect(status().isOk())
					.andExpect(content().string("Internal filtered stats API"));
		} catch (Exception e) {
			e.printStackTrace();
		}
	}

	@Test
	public void findOne() {
		given(this.ref.findPlayerByUid(1L))
				.willReturn(new Player(1L));
		try {
			this.mvc.perform(get("/stats/get/1")).andExpect(status().isOk())
					.andExpect(content().json(Utils.objectToJson(new Player(1L))));
		} catch (Exception e) {
			e.printStackTrace();
		}
	}
}
