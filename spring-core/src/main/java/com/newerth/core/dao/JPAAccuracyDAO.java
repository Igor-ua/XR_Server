package com.newerth.core.dao;

import com.newerth.core.entities.AccuracyStats;
import org.springframework.data.jpa.repository.JpaRepository;

public interface JPAAccuracyDAO extends JpaRepository<AccuracyStats, Long> {
//	AccuracyStats findByPlayerUid(Long playerUid);
}
