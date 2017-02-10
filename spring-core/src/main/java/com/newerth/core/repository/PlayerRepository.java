package com.newerth.core.repository;

import com.newerth.core.entities.Player;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.stereotype.Repository;

@Repository
public interface PlayerRepository extends JpaRepository<Player, Long> {

	Player findByUid(Long uid);

	// JPQL
	@Query(value = "SELECT * FROM PLAYER WHERE LOWER(last_used_name) like ?1% ORDER BY last_used_name ASC LIMIT 1",
			nativeQuery = true)
	Player findByLastUsedName(String name);
}
