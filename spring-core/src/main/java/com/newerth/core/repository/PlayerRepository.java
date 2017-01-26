package com.newerth.core.repository;

import com.newerth.core.entities.Player;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface PlayerRepository extends JpaRepository<Player, Long> {

	Player findByUid(Long uid);

	Player findByLastUsedName(String name);
}
