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
	@JoinColumn(nullable = false)
	private long uid;

	@JsonView(View.Summary.class)
	@Column(name = "last_used_name", nullable = false, length = 20)
	private String lastUsedName;

	public Player() {
		this.uid = 0;
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
	public String toString() {
		return "Player{" +
				"id=" + id +
				", uid=" + uid +
				", lastUsedName='" + lastUsedName + '\'' +
				'}';
	}
}
