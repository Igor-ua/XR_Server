package com.newerth.api;

import org.junit.Test;
import org.junit.runner.RunWith;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.http.MediaType;
import org.springframework.test.context.junit4.SpringRunner;
import org.springframework.test.web.servlet.MockMvc;

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.*;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

@RunWith(SpringRunner.class)
@WebMvcTest(RootApi.class)
public class RootApiTest {

	@Autowired
	private MockMvc mvc;

	@Test
	public void rootApiMessage() {
		try {
			this.mvc.perform(get("/").accept(MediaType.TEXT_PLAIN)).andExpect(status().isOk())
					.andExpect(content().string("XR Server instagib API"));
		} catch (Exception e) {
			e.printStackTrace();
		}
	}
}