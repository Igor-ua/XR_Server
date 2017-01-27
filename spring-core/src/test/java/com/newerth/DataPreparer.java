package com.newerth;

import com.newerth.core.entities.Player;

public class DataPreparer {

	public static Player getPlayerWithFields() {
		return getPlayerWithFields(123L);
	}

	public static Player getPlayerWithFields(Long uid) {
		Player p = new Player(uid);
		p.setLastUsedName("Mike");
		p.setAccuracyStats(10, 5, 5);
		return p;
	}
}
