package com.newerth.core.entities;

import com.fasterxml.jackson.annotation.JsonBackReference;
import com.fasterxml.jackson.annotation.JsonIgnore;
import com.fasterxml.jackson.annotation.JsonView;
import com.newerth.core.View;
import org.springframework.stereotype.Component;

import javax.persistence.*;
import javax.validation.constraints.Max;
import javax.validation.constraints.Min;
import java.io.Serializable;

@Component
@Entity
@Table(name = "awards")
public class Awards implements Serializable {

	@Id
	@GeneratedValue
	@JsonIgnore
	@Column(name = "id")
	private Long id;

	@OneToOne
	@JoinColumn(name = "player_uid", referencedColumnName = "uid", unique = true, nullable = false)
	@JsonView(View.Summary.class)
	@JsonBackReference
	private Player player;
	//----Last awards-----------------------------------------------------------------------
	@Column(name = "last_mvp")
	@JsonIgnore
	@Min(0)
	@Max(1)
	private int lastMvp;

	@Column(name = "last_sadist")
	@JsonIgnore
	@Min(0)
	@Max(1)
	private int lastSadist;

	@Column(name = "last_survivor")
	@JsonIgnore
	@Min(0)
	@Max(1)
	private int lastSurvivor;

	@Column(name = "last_ripper")
	@JsonIgnore
	@Min(0)
	@Max(1)
	private int lastRipper;

	@Column(name = "last_phoe")
	@JsonIgnore
	@Min(0)
	@Max(1)
	private int lastPhoe;

	@Column(name = "last_aimbot")
	@JsonIgnore
	@Min(0)
	@Max(1)
	private int lastAimbot;
	//----Accumulated awards----------------------------------------------------------------
	@Column(name = "accumulated_mvp")
	@JsonView(View.Summary.class)
	@Min(0)
	private int accumulatedMvp;

	@Column(name = "accumulated_sadist")
	@JsonView(View.Summary.class)
	@Min(0)
	private int accumulatedSadist;

	@Column(name = "accumulated_survivor")
	@JsonView(View.Summary.class)
	@Min(0)
	private int accumulatedSurvivor;

	@Column(name = "accumulated_ripper")
	@JsonView(View.Summary.class)
	@Min(0)
	private int accumulatedRipper;

	@Column(name = "accumulated_phoe")
	@JsonView(View.Summary.class)
	@Min(0)
	private int accumulatedPhoe;

	@Column(name = "accumulated_aimbot")
	@JsonView(View.Summary.class)
	@Min(0)
	private int accumulatedAimbot;
	//--------------------------------------------------------------------------------------
	// Flag that indicates that accumulated logic was called once
	@Transient
	private boolean isAccumulated = false;
	//--------------------------------------------------------------------------------------
	public Awards() {
	}

	public Awards(Player player) {
		this();
		this.player = player;
	}
	//----Getters---------------------------------------------------------------------------
	public Long getId() {
		return id;
	}

	public Player getPlayer() {
		return player;
	}

	public int getLastMvp() {
		return lastMvp;
	}

	public int getLastSadist() {
		return lastSadist;
	}

	public int getLastSurvivor() {
		return lastSurvivor;
	}

	public int getLastRipper() {
		return lastRipper;
	}

	public int getLastPhoe() {
		return lastPhoe;
	}

	public int getLastAimbot() {
		return lastAimbot;
	}

	public int getAccumulatedMvp() {
		return accumulatedMvp;
	}

	public int getAccumulatedSadist() {
		return accumulatedSadist;
	}

	public int getAccumulatedSurvivor() {
		return accumulatedSurvivor;
	}

	public int getAccumulatedRipper() {
		return accumulatedRipper;
	}

	public int getAccumulatedPhoe() {
		return accumulatedPhoe;
	}

	public int getAccumulatedAimbot() {
		return accumulatedAimbot;
	}

	//----Setters---------------------------------------------------------------------------
	void setAwards(int mvp, int sadist, int survivor, int ripper, int phoe, int aimbot) {
		this.lastMvp = mvp;
		this.lastSadist = sadist;
		this.lastSurvivor = survivor;
		this.lastRipper = ripper;
		this.lastPhoe = phoe;
		this.lastAimbot = aimbot;

		if (!isAccumulated) {
			this.accumulatedMvp += mvp;
			this.accumulatedSadist += sadist;
			this.accumulatedSurvivor += survivor;
			this.accumulatedRipper += ripper;
			this.accumulatedPhoe += phoe;
			this.accumulatedAimbot += aimbot;
			isAccumulated = true;
		}
	}

	public void setId(Long id) {
		this.id = id;
	}

	//--------------------------------------------------------------------------------------
	@PrePersist
	@PreUpdate
	private void accumulatedStatsUpdater() {
		isAccumulated = false;
	}
	//--------------------------------------------------------------------------------------
	@Override
	public boolean equals(Object o) {
		if (this == o) return true;
		if (o == null || getClass() != o.getClass()) return false;

		Awards awards = (Awards) o;

		return id != null ? id.equals(awards.id) : awards.id == null;
	}

	@Override
	public int hashCode() {
		return id != null ? id.hashCode() : 0;
	}
	//--------------------------------------------------------------------------------------
	@Override
	public String toString() {
		return "\tAwards: {\n" +
				"\t\tplayer_uid: " + (player != null ? player.getUid() : "null") + "\n" +
				"\t\tlast: [mvp: " + lastMvp + ", sadist: " + lastSadist +
				", survivor: " + lastSurvivor + ", ripper: " + lastRipper +
				", phoe: " + lastPhoe + ", aimbot: " + lastAimbot + "]\n" +
				"\t\taccumulated: [mvp: " + accumulatedMvp + ", sadist: " + accumulatedSadist +
				", survivor: " + accumulatedSurvivor + ", ripper: " + accumulatedRipper +
				", phoe: " + accumulatedPhoe + ", aimbot: " + accumulatedAimbot + "]\n" +
				"\t}";
	}
}