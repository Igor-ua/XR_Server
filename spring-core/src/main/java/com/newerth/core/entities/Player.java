package com.newerth.core.entities;

import com.fasterxml.jackson.annotation.JsonView;
import com.newerth.core.View;
import org.springframework.stereotype.Component;

import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.Id;
import javax.persistence.Table;

@Component

@Entity
@Table(name = "Person_sql")
public class Player {

	@Id
	@GeneratedValue
	@JsonView(View.Summary.class)
	private long id;
	@JsonView(View.Summary.class)
	private String name;

	public Player() {
		this.name = "Mike";
	}

	public long getId() {
		return id;
	}

	public String getName() {
		return name;
	}

	@Override
	public String toString() {
		return "Player{" +
				"id=" + id +
				", name='" + name + '\'' +
				'}';
	}
}
