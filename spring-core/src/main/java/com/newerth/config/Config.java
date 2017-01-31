package com.newerth.config;

import org.apache.catalina.filters.RequestDumperFilter;
import org.springframework.boot.web.servlet.FilterRegistrationBean;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

import javax.servlet.Filter;

@Configuration
public class Config {

//	@Bean
	public FilterRegistrationBean requestDumperFilter() {
		Filter requestDumperFilter = new RequestDumperFilter();
		FilterRegistrationBean registration = new FilterRegistrationBean();
		registration.setFilter(requestDumperFilter);
		registration.addUrlPatterns("/*");
		return registration;
	}
}
