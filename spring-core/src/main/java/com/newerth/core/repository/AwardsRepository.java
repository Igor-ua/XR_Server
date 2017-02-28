package com.newerth.core.repository;

import com.newerth.core.entities.Awards;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface AwardsRepository extends JpaRepository<Awards, Long> {
	@Query(value = "SELECT * FROM awards WHERE accumulated_aimbot > 0 ORDER BY accumulated_aimbot DESC LIMIT 5",
			nativeQuery = true)
	List<Awards> findTopAimbots();

	@Query(value = "SELECT * FROM awards WHERE accumulated_mvp > 0 ORDER BY accumulated_mvp DESC LIMIT 5",
			nativeQuery = true)
	List<Awards> findTopMvps();

	@Query(value = "SELECT * FROM awards WHERE accumulated_sadist > 0 ORDER BY accumulated_sadist DESC LIMIT 5",
			nativeQuery = true)
	List<Awards> findTopSadists();

	@Query(value = "SELECT * FROM awards WHERE accumulated_ripper > 0 ORDER BY accumulated_ripper DESC LIMIT 5",
			nativeQuery = true)
	List<Awards> findTopRippers();

	@Query(value = "SELECT * FROM awards WHERE accumulated_phoe > 0 ORDER BY accumulated_phoe DESC LIMIT 5",
			nativeQuery = true)
	List<Awards> findTopPhoes();

	@Query(value = "SELECT * FROM awards WHERE accumulated_survivor > 0 ORDER BY accumulated_survivor DESC LIMIT 5",
			nativeQuery = true)
	List<Awards> findTopSurvivors();
}
