package com.newerth.core.repository;

import com.newerth.core.entities.LastAccuracyStats;
import com.newerth.core.entities.Player;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface LastAccuracyRepository extends JpaRepository<LastAccuracyStats, Long> {
	LastAccuracyStats findByPlayer(Player player);
}
