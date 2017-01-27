package com.newerth.core.repository;

import com.newerth.core.entities.AccuracyStats;
import com.newerth.core.entities.Player;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface AccuracyRepository extends JpaRepository<AccuracyStats, Long> {
	AccuracyStats findByPlayer(Player player);
}
