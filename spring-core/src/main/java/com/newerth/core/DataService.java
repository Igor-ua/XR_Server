package com.newerth.core;

import com.newerth.core.entities.Player;

import java.util.List;

public interface DataService {
	Player findOne(Long id);

	List<Player> findAll();

	boolean saveOne(Player player);

	boolean saveAll(List<Player> players);
}
