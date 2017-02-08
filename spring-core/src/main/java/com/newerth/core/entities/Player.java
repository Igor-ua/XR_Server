package com.newerth.core.entities;

import com.fasterxml.jackson.annotation.JsonView;
import com.newerth.core.View;
import org.springframework.stereotype.Component;

import javax.persistence.*;
import javax.validation.constraints.Min;

@Component
@Entity
@Table(name = "player")
public class Player {

	@Id
	@Min(0)
	@JsonView(View.Summary.class)
	@Column(name = "uid")
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
		this.uid = 0L;
		this.lastUsedName = "";
		this.accuracyStats = new AccuracyStats(this);
		this.awards = new Awards(this);
	}

	public Player(Long uid) {
		this();
		this.uid = uid;
	}

	public Player(Long uid, String name) {
		this(uid);
		this.setLastUsedName(name);
	}

	public void setUid(Long uid) {
		this.uid = uid;
	}

	public Long getUid() {
		return uid;
	}

	public AccuracyStats getAccuracyStats() {
		return accuracyStats;
	}

	public void setAccuracyStats(int shots, int hits, int frags) {
		accuracyStats.setStats(shots, hits, frags);
	}

	public void setAwards(int mvp, int sadist, int survivor, int ripper, int phoe, int aimbot) {
		awards.setAwards(mvp, sadist, survivor, ripper, phoe, aimbot);
	}

	public Awards getAwards() {
		return awards;
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

		return uid != null ? uid.equals(player.uid) : player.uid == null;
	}

	@Override
	public int hashCode() {
		return uid != null ? uid.hashCode() : 0;
	}

	@Override
	public String toString() {
		return "Player: {\n" +
				"\tuid: " + uid + ",\n" +
				"\tname: " + lastUsedName + ",\n" +
				"" + accuracyStats + "\n" +
				"" + awards +
				"\n}";
	}
}
