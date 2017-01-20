package com.newerth.core.entities;


import org.springframework.stereotype.Component;

import javax.persistence.Entity;
import javax.persistence.Table;

@Component
@Entity
@Table(name = "accuracy_stats_last")
public class LastAccuracyStats extends AccuracyStats {
}