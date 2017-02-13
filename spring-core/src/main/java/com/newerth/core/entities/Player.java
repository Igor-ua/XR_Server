package com.newerth.core.entities;

import com.fasterxml.jackson.annotation.JsonIgnore;
import com.fasterxml.jackson.annotation.JsonView;
import com.newerth.core.View;
import org.springframework.stereotype.Component;

import javax.persistence.*;
import javax.validation.constraints.Min;
import javax.validation.constraints.Pattern;
import java.text.SimpleDateFormat;
import java.util.Date;

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
	@Column(name = "clan_id")
	private Long clanId;

	@JsonView(View.Summary.class)
	@Column(name = "last_used_name", nullable = false, length = 50)
	@Pattern(regexp = "[A-Za-z-_()0-9 ]{0,50}")
	private String lastUsedName;

	@OneToOne(mappedBy = "player", cascade = CascadeType.ALL)
	@JsonView(View.Summary.class)
	private AccuracyStats accuracyStats;

	@OneToOne(mappedBy = "player", cascade = CascadeType.ALL)
	@JsonView(View.Summary.class)
	private Awards awards;

	@Column(name = "game_ts")
	@JsonIgnore
	private Date gameTimeStamp;

	@Transient
	private SimpleDateFormat sdf = new SimpleDateFormat("dd.MM.yyyy");

	@Transient
	private static final String NAME_FILTER = "[^-\\w\\s^(^)]";

	public Player() {
		this.gameTimeStamp = new Date();
		this.uid = 0L;
		this.clanId = 86846L;
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

	public Long getClanId() {
		return clanId;
	}

	public void setClanId(Long clanId) {
		if (clanId == 0) {
			this.clanId = 86846L;
		} else {
			this.clanId = clanId;
		}
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
		this.lastUsedName = lastUsedName.replaceAll(NAME_FILTER, "");
	}

	@PrePersist
	@PreUpdate
	private void prePersistUpdate() {
		this.gameTimeStamp = new Date();
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
				"\tclan_id: " + clanId + ",\n" +
				"\tname: " + lastUsedName + ",\n" +
				"\ttime: " + sdf.format(gameTimeStamp) + "\n" +
				"" + accuracyStats + "\n" +
				"" + awards +
				"\n}";
	}
}
