package com.newerth.core.dao;

import com.newerth.core.entities.Player;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface JPAPlayerDAO extends JpaRepository<Player, Long> {

	Player findByUid(Long uid);

	Player findByLastUsedName(String name);
}
