package com.newerth.core.entities;

import com.fasterxml.jackson.annotation.JsonView;
import com.newerth.core.View;
import org.springframework.stereotype.Component;

import javax.persistence.*;

@Component
@Entity
@Table(name = "player")
public class Player {

	@Id
	@GeneratedValue
	@JsonView(View.Summary.class)
	@Column(name = "id")
	private long id;

	@Column(name = "uid", unique=true, nullable = false)
	@JsonView(View.Summary.class)
	private long uid;

	@JsonView(View.Summary.class)
	@Column(name = "last_used_name", nullable = false, length = 50)
	private String lastUsedName;


	@OneToOne(cascade = CascadeType.ALL)
	@JsonView(View.Summary.class)
	private AccuracyStats accuracyStats;

	public Player() {
		this.uid = 0;
	}

	public AccuracyStats getAccuracyStats() {
		return accuracyStats;
	}

	public void setAccuracyStats(AccuracyStats accuracyStats) {
		this.accuracyStats = accuracyStats;
	}

	public long getId() {
		return id;
	}

	public void setId(long id) {
		this.id = id;
	}

	public long getUid() {
		return uid;
	}

	public void setUid(long uid) {
		this.uid = uid;
	}

	public String getLastUsedName() {
		return lastUsedName;
	}

	public void setLastUsedName(String lastUsedName) {
		this.lastUsedName = lastUsedName;
	}

	@Override
	public boolean equals(Object o) {
		if (this == o) return true;
		if (o == null || getClass() != o.getClass()) return false;

		Player player = (Player) o;

		return id == player.id && uid == player.uid;
	}

	@Override
	public int hashCode() {
		int result = (int) (id ^ (id >>> 32));
		result = 31 * result + (int) (uid ^ (uid >>> 32));
		return result;
	}

	@Override
	public String toString() {
		return "Player{" +
				"id=" + id +
				", uid=" + uid +
				", lastUsedName='" + lastUsedName + '\'' +
				", accuracyStats=" + accuracyStats +
				'}';
	}
}
