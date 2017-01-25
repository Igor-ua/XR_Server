package com.newerth.core.dao;

import com.newerth.core.entities.AccuracyStats;
import com.newerth.core.entities.Player;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface JPAAccuracyDAO extends JpaRepository<AccuracyStats, Long> {
	AccuracyStats findByPlayer(Player player);
}
