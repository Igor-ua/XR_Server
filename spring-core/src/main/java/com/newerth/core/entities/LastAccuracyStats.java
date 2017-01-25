package com.newerth.core.entities;


import org.springframework.stereotype.Component;

import javax.persistence.Entity;
import javax.persistence.PrePersist;
import javax.persistence.PreUpdate;
import javax.persistence.Table;

@Component
@Entity
@Table(name = "accuracy_stats_last")
public class LastAccuracyStats extends AccuracyStats {

	public LastAccuracyStats() {
	}

	public LastAccuracyStats(Player player) {
		super(player);
	}

	@Override
	@PrePersist
	@PreUpdate
	protected void updateAccuracyPercent() {
		super.updateAccuracyPercent();
	}
}