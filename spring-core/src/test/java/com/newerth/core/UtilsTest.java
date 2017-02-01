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

	// {"Players": [{"uid" : 1, "lastUsedName" : "Mike","accuracyStats" : {"lastShots" : 10,"lastHits" : 5,"lastFrags" : 5}},
	// 			    {"uid" : 2, "lastUsedName" : "John","accuracyStats" : {"lastShots" : 4,"lastHits" : 1,"lastFrags" : 1}}]}
	private static final String jsonArray = "{\"Players\": [{\"uid\" : 1, \"lastUsedName\" : \"Mike\",\"accuracyStats\":" +
			" {\"lastShots\" : 10,\"lastHits\" : 5,\"lastFrags\" : 5}}, {\"uid\" : 2, \"lastUsedName\" : \"John\"," +
			"\"accuracyStats\" : {\"lastShots\" : 4,\"lastHits\" : 1,\"lastFrags\" : 1}}]}";

	@Test
	public void getPlayerFromJson() {
		assertThat(Utils.getPlayerFromJson(json));
		System.err.println(Utils.getPlayerFromJson(json));
	}

	@Test
	public void getListOfPlayersFromJson() {
		assertThat(Utils.getListOfPlayersFromJson(jsonArray));
		System.err.println(Utils.getListOfPlayersFromJson(jsonArray));
	}
}
