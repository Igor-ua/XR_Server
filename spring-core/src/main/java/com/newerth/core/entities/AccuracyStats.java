package com.newerth.core.entities;

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
	@GeneratedValue(strategy = GenerationType.TABLE)
	@JsonView(View.Summary.class)
	@Column(name = "id")
	private Long id;

	@OneToOne
	@JoinColumn(name = "player_uid", referencedColumnName = "uid", unique = true)
	@JsonView(View.Summary.class)
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
	@Column(name = "last_shots")
	@JsonView(View.Summary.class)
	private int accumulatedShots;

	@Column(name = "last_hits")
	@JsonView(View.Summary.class)
	private int accumulatedHits;

	@Column(name = "last_frags")
	@JsonView(View.Summary.class)
	private int accumulatedFrags;

	@Column(name = "accuracy_percent")
	@JsonView(View.Summary.class)
	@Min(0)
	@Max(100)
	private int accumulatedAccuracyPercent;
	//--------------------------------------------------------------------------------------
	@Column(name = "game_ts")
	@JsonView(View.Summary.class)
	private Date gameTimeStamp;

	@Transient
	private SimpleDateFormat sdf = new SimpleDateFormat("dd.MM.yyyy");
	//--------------------------------------------------------------------------------------

	public AccuracyStats() {
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

	public int getLastFrags() {
		return lastFrags;
	}

	public int getLastHits() {
		return lastHits;
	}
	//----Setters---------------------------------------------------------------------------





	protected void updateAccuracyPercent() {
		if (this.lastHits > 0 && this.lastShots > 0) {
			this.lastAccuracyPercent = lastHits * 100 / lastShots;
		}
	}

	void updateAccuracyStats(AccuracyStats as) {
		this.lastShots += as.getLastShots();
		this.lastHits += as.getLastHits();
		this.lastFrags += as.getLastFrags();
		updateAccuracyPercent();
	}




	public void setLastShots(int lastShots) {
		this.lastShots = lastShots;
	}

	public void setLastFrags(int lastFrags) {
		this.lastFrags = lastFrags;
	}

	public void setLastHits(int lastHits) {
		this.lastHits = lastHits;
	}

	public void setPlayer(Player player) {
		this.player = player;
	}



	@PrePersist
	@PreUpdate
	private void updateGameTimeStamp() {
		this.gameTimeStamp = new Date();
	}

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

	@Override
	public String toString() {
		return "AccuracyStats{" +
				"player_uid=" + player.getUid() +
				", lastShots=" + lastShots +
				", lastHits=" + lastHits +
				", lastAccuracyPercent=" + lastAccuracyPercent +
				", gameTimeStamp=" + sdf.format(gameTimeStamp) +
				'}';
	}
}