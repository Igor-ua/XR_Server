package com.newerth;

import com.newerth.core.Informer;
import com.newerth.core.Updater;
import com.newerth.core.entities.AccuracyStats;
import com.newerth.core.entities.Player;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.CommandLineRunner;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.builder.SpringApplicationBuilder;
import org.springframework.boot.web.support.SpringBootServletInitializer;

import java.util.Date;

@SpringBootApplication
public class Main extends SpringBootServletInitializer implements CommandLineRunner {

	@Override
	protected SpringApplicationBuilder configure(SpringApplicationBuilder application) {
		return application.sources(Main.class);
	}

	public static void main(String[] args) {
		SpringApplication.run(Main.class, args);
	}

	@Override
	public void run(String... strings) throws Exception {
		test();
	}

	@Autowired
	private Informer informer;
	@Autowired
	private Updater updater;

	private void test() {
		System.out.println("TEST_______________________");

		Player p = new Player();
		p.setUid(123L);
		p.setLastUsedName("Mike");
//		updater.saveOrUpdatePlayer(p);

		AccuracyStats as = new AccuracyStats();

		as.setPlayer(p);
		as.setShots(10);
		as.setHits(4);
		as.setFrags(4);
		as.setGameTimeStamp(new Date());

		p.updateAccuracyStats(as);

		updater.saveOrUpdatePlayer(p);


//		p = informer.findPlayer(123L);
		p = informer.findOne("Mike");
		System.out.println("found: " + p);
//		as = new AccuracyStats();
//		as.setPlayer(p);
//		as.setShots(20);
//		as.setHits(4);
//		as.setFrags(2);
//		as.setGameTimeStamp(new Date());
//		p.updateAccuracyStats(as);
//		updater.saveOrUpdatePlayer(p);
	}
}
