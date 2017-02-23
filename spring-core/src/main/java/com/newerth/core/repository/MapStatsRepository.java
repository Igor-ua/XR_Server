package com.newerth.core.repository;

import com.newerth.core.entities.MapStats;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface MapStatsRepository extends JpaRepository<MapStats, Long> {
}
