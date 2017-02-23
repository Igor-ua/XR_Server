package com.newerth.core.entities;


import com.fasterxml.jackson.annotation.JsonView;
import com.newerth.core.View;
import org.springframework.stereotype.Component;

import javax.persistence.*;

@Component
@Entity
@Table(name = "map_stats")
public class MapStats {

	@Id
	@GeneratedValue
	@JsonView(View.Summary.class)
	@Column(name = "id")
	private Long id;

	@Column(name = "map_name")
	@JsonView(View.Summary.class)
	private String mapName;

	@Column(name = "red_score")
	@JsonView(View.Summary.class)
	private int redScore;

	@Column(name = "blue_score")
	@JsonView(View.Summary.class)
	private int blueScore;

	@Column(name = "winner")
	@JsonView(View.Summary.class)
	private String winner;

	public Long getId() {
		return id;
	}

	public void setId(Long id) {
		this.id = id;
	}

	public String getMapName() {
		return mapName;
	}

	public void setMapName(String mapName) {
		this.mapName = mapName;
	}

	public int getRedScore() {
		return redScore;
	}

	public void setRedScore(int redScore) {
		this.redScore = redScore;
	}

	public int getBlueScore() {
		return blueScore;
	}

	public void setBlueScore(int blueScore) {
		this.blueScore = blueScore;
	}

	public String getWinner() {
		return winner;
	}

	public void setWinner(String winner) {
		this.winner = winner;
	}

	@Override
	public boolean equals(Object o) {
		if (this == o) return true;
		if (o == null || getClass() != o.getClass()) return false;

		MapStats mapStats = (MapStats) o;

		return (id != null ? id.equals(mapStats.id) : mapStats.id == null) &&
				(mapName != null ? mapName.equals(mapStats.mapName) : mapStats.mapName == null);
	}

	@Override
	public int hashCode() {
		int result = id != null ? id.hashCode() : 0;
		result = 31 * result + (mapName != null ? mapName.hashCode() : 0);
		return result;
	}

	@Override
	public String toString() {
		return "MapStats: {\n" +
				"\tid: " + id + ",\n" +
				"\tmap name: '" + mapName +  ",\n" +
				"\tred score: " + redScore + ",\n" +
				"\tblue score: " + blueScore + ",\n" +
				"\twinner: " + winner + ",\n" +
				'}';
	}
}