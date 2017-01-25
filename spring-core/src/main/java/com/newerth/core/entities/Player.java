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
	private Long id;

	@Column(name = "uid", unique = true, nullable = false)
	@JsonView(View.Summary.class)
	private Long uid;

	@JsonView(View.Summary.class)
	@Column(name = "last_used_name", nullable = false, length = 50)
	private String lastUsedName;

	@OneToOne(mappedBy = "player", cascade = CascadeType.ALL)
	@JsonView(View.Summary.class)
	private AccuracyStats accuracyStats;

	@OneToOne(mappedBy = "player", cascade = CascadeType.ALL)
	@JsonView(View.Summary.class)
	private Awards awards;

	public Player() {
	}

	public AccuracyStats getAccuracyStats() {
		return accuracyStats;
	}

	public void updateAccuracyStats(AccuracyStats as) {
		if (this.accuracyStats == null) {
			this.accuracyStats = as;
		} else {
			this.accuracyStats.setShots(this.accuracyStats.getShots() + as.getShots());
			this.accuracyStats.setFrags(this.accuracyStats.getFrags() + as.getFrags());
			this.accuracyStats.setHits(this.accuracyStats.getHits() + as.getHits());
			this.accuracyStats.setGameTimeStamp(as.getGameTimeStamp());
		}
	}

	public Long getId() {
		return id;
	}

	public void setId(Long id) {
		this.id = id;
	}

	public Long getUid() {
		return uid;
	}

	public void setUid(Long uid) {
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

		return (id != null ? id.equals(player.id) : player.id == null) &&
				(uid != null ? uid.equals(player.uid) : player.uid == null);
	}

	@Override
	public int hashCode() {
		int result = id != null ? id.hashCode() : 0;
		result = 31 * result + (uid != null ? uid.hashCode() : 0);
		return result;
	}

	@Override
	public String toString() {
		return "Player{" +
				"id=" + id +
				", uid=" + uid +
				", lastUsedName='" + lastUsedName + "'}";
	}
}
