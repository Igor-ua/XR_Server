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
import java.text.SimpleDateFormat;
import java.util.Date;

@Component
@Entity
@Table(name = "accuracy_stats")
public class AccuracyStats implements Serializable {

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
	//----Last accuracy stats---------------------------------------------------------------
	@Column(name = "last_shots")
	@JsonView(View.Summary.class)
	private int lastShots;

	@Column(name = "last_hits")
	@JsonView(View.Summary.class)
	private int lastHits;

	@Column(name = "last_frags")
	@JsonView(View.Summary.class)
	private int lastFrags;

	@Column(name = "last_accuracy_percent")
	@JsonView(View.Summary.class)
	@Min(0)
	@Max(100)
	private int lastAccuracyPercent;
	//----Accumulated accuracy stats--------------------------------------------------------
	@Column(name = "accumulated_shots")
	@JsonView(View.Summary.class)
	private int accumulatedShots;

	@Column(name = "accumulated_hits")
	@JsonView(View.Summary.class)
	private int accumulatedHits;

	@Column(name = "accumulated_frags")
	@JsonView(View.Summary.class)
	private int accumulatedFrags;

	@Column(name = "accumulated_accuracy_percent")
	@JsonView(View.Summary.class)
	@Min(0)
	@Max(100)
	private int accumulatedAccuracyPercent;
	//--------------------------------------------------------------------------------------
	// Flag that indicates that accumulated logic was called once
	@Transient
	private boolean isAccumulated = false;

	//--------------------------------------------------------------------------------------

	public AccuracyStats() {}

	public AccuracyStats(Player player) {
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

	public int getLastShots() {
		return lastShots;
	}

	public int getLastHits() {
		return lastHits;
	}

	public int getLastAccuracyPercent() {
		return lastAccuracyPercent;
	}

	public int getLastFrags() {
		return lastFrags;
	}

	public int getAccumulatedShots() {
		return accumulatedShots;
	}

	public int getAccumulatedHits() {
		return accumulatedHits;
	}

	public int getAccumulatedFrags() {
		return accumulatedFrags;
	}

	public int getAccumulatedAccuracyPercent() {
		return accumulatedAccuracyPercent;
	}

	//----Setters---------------------------------------------------------------------------
	void setStats(int shots, int hits, int frags) {
		if (hits > shots) {
			throw new IllegalArgumentException("Shots more than hits: [shots: " + shots + ", hits: " + hits + "]");
		}

		this.lastShots = shots;
		this.lastHits = hits;
		this.lastFrags = frags;
		this.lastAccuracyPercent = calculateAccuracy(this.lastShots, this.lastHits);

		if (!isAccumulated) {
			this.accumulatedShots += shots;
			this.accumulatedHits += hits;
			this.accumulatedFrags += frags;
			this.accumulatedAccuracyPercent = calculateAccuracy(this.accumulatedShots, this.accumulatedHits);
			isAccumulated = true;
		}
	}

	public void setId(Long id) {
		this.id = id;
	}
	//--------------------------------------------------------------------------------------
	private int calculateAccuracy(int shots, int hits) {
		int result = 0;
		if (hits > 0 && shots > 0) {
			result = (int) Math.round((double) hits * 100 / shots);
		}
		return result;
	}

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

		AccuracyStats that = (AccuracyStats) o;

		return (id != null ? id.equals(that.id) : that.id == null) &&
				(player != null ? player.equals(that.player) : that.player == null);
	}

	@Override
	public int hashCode() {
		int result = id != null ? id.hashCode() : 0;
		result = 31 * result + (player != null ? player.hashCode() : 0);
		return result;
	}
	//--------------------------------------------------------------------------------------
	@Override
	public String toString() {
		return "\tAccuracyStats: {\n" +
				"\t\tplayer_uid: " + (player != null ? player.getUid() : "null") + "\n" +
				"\t\tlast:        [shots: " + lastShots + ", hits: " + lastHits + ", frags: " + lastFrags + ", accuracy: " +
				lastAccuracyPercent + "]\n" +
				"\t\taccumulated: [shots: " + accumulatedShots + ", hits: " + accumulatedHits + ", frags: " + accumulatedFrags +
				", accuracy: " + accumulatedAccuracyPercent + "]\n" +
				"\t}";
	}
}