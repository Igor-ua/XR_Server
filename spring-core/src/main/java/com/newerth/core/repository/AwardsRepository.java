package com.newerth.core.repository;

import com.newerth.core.entities.Awards;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface AwardsRepository extends JpaRepository<Awards, Long> {
	@Query(value = "SELECT * FROM awards ORDER BY accumulated_aimbot DESC LIMIT 10", nativeQuery = true)
	List<Awards> findTop10Aimbots();
}
