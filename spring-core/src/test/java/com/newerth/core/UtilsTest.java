package com.newerth.core;

import org.junit.Test;
import org.junit.runner.RunWith;
import org.springframework.context.annotation.ComponentScan;
import org.springframework.test.context.ContextConfiguration;
import org.springframework.test.context.junit4.SpringRunner;

import static org.assertj.core.api.Assertions.assertThat;

@RunWith(SpringRunner.class)
@ContextConfiguration
@ComponentScan("com.newerth.core")
public class UtilsTest {

	private static final String json = "{\"accuracyStats\": {\"lastShots\": 10, \"lastFrags\": 5, \"lastHits\": 5}, " +
			"\"uid\": 2, \"lastUsedName\": \"Mike\"}";

	@Test
	public void getPlayerFromJson() {
		assertThat(Utils.getPlayerFromJson(json));
		System.err.println(Utils.getPlayerFromJson(json));
	}
}
