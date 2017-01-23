package com.newerth.core.entities;

import com.fasterxml.jackson.annotation.JsonView;
import com.newerth.core.View;
import org.springframework.stereotype.Component;

import javax.persistence.*;
import java.io.Serializable;

@Component
@Entity
@Table(name = "awards")
public class Awards implements Serializable {
	@Id
	@GeneratedValue
	@JsonView(View.Summary.class)
	@Column(name = "id")
	private Long id;

	@OneToOne
	@JoinColumn(name = "player_uid", referencedColumnName = "uid", nullable = false)
	@JsonView(View.Summary.class)
	private Player player;

	public Awards() {
	}
}