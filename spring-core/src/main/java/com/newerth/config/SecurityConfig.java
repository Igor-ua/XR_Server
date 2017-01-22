package com.newerth.config;

import org.springframework.context.annotation.Configuration;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configuration.EnableWebSecurity;
import org.springframework.security.config.annotation.web.configuration.WebSecurityConfigurerAdapter;


@Configuration
@EnableWebSecurity
public class SecurityConfig extends WebSecurityConfigurerAdapter {

	@Override
	protected void configure(HttpSecurity http) throws Exception {
		http
				.authorizeRequests()
				.antMatchers("/").permitAll()
				.antMatchers("/world/**").permitAll()
				.antMatchers("/stats/**")
				.access("hasIpAddress('0.0.0.0/16')" +
						" or hasIpAddress('127.0.0.1/32')" +
						" or hasIpAddress('0:0:0:0:0:0:0:1')")
				.and()
				.csrf().disable()
		;
	}
}