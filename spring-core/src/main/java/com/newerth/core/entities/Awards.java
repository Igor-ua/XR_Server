package com.newerth.core.entities;

import com.fasterxml.jackson.annotation.JsonView;
import com.newerth.core.View;
import org.springframework.stereotype.Component;

import javax.persistence.*;
import java.io.Serializable;

@Component
@Entity
@Table(name = "awards")
public class Awards implements Serializable {
	@Id
	@GeneratedValue
	@JsonView(View.Summary.class)
	@Column(name = "id")
	private Long id;

	@OneToOne
	@JoinColumn(name = "player_uid", referencedColumnName = "uid", nullable = false)
	@JsonView(View.Summary.class)
	private Player player;

	public Awards() {
	}

	public Awards(Player player) {
		this.player = player;
	}

	void updateAwards(Awards awards) {
		// update awards here
	}

	public Long getId() {
		return id;
	}

	public void setId(Long id) {
		this.id = id;
	}

	public Player getPlayer() {
		return player;
	}

	public void setPlayer(Player player) {
		this.player = player;
	}

	@Override
	public String toString() {
		return "Awards{" +
				"id=" + id +
				", player_uid=" + player.getUid() +
				'}';
	}
}