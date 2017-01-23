package com.newerth.core.dao;

import com.newerth.core.entities.LastAccuracyStats;
import com.newerth.core.entities.Player;
import org.springframework.data.jpa.repository.JpaRepository;

public interface JPALastAccuracyDAO extends JpaRepository<LastAccuracyStats, Long> {
	LastAccuracyStats findByPlayer(Player player);
}
