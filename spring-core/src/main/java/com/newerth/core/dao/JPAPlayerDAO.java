package com.newerth.core.dao;

import com.newerth.core.entities.Player;
import org.springframework.data.jpa.repository.JpaRepository;

public interface JPAPlayerDAO extends JpaRepository<Player, Long> {

}
