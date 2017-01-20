package com.newerth.core;

import com.newerth.core.dao.JPAPlayerDAO;
import com.newerth.core.entities.Player;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class DataService {

	private JPAPlayerDAO jpaPlayerDAO;

	@Autowired
	private void setPlayer(JPAPlayerDAO jpaPlayerDAO) {
		this.jpaPlayerDAO = jpaPlayerDAO;
	}

	public Player findOne(Long id) {
		return jpaPlayerDAO.findOne(id);
	}

	public List<Player> findAll() {
		return jpaPlayerDAO.findAll();
	}

	public boolean saveOne(Player player) {
		try {
			jpaPlayerDAO.save(player);
			return true;
		} catch (RuntimeException e) {
			// ignored
		}
		return false;
	}

	public boolean saveAll(List<Player> players) {
		return false;
	}
}
