package com.newerth.core;

import com.newerth.core.dao.JPAPlayerDAO;
import com.newerth.core.entities.Player;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class GameService implements DataService {

	@Autowired
	private JPAPlayerDAO jpaPlayerDAO;

	@Override
	public Player findOne(Long id) {
		return jpaPlayerDAO.findOne(id);
	}

	@Override
	public List<Player> findAll() {
		return jpaPlayerDAO.findAll();
	}

	@Override
	public boolean saveOne(Player player) {
		try {
			jpaPlayerDAO.save(player);
			return true;
		} catch (RuntimeException e) {
			// ignored; all logging here
		}
		return false;
	}

	@Override
	public boolean saveAll(List<Player> players) {
		return false;
	}
}
