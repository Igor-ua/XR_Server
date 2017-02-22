package com.newerth.api;

import com.newerth.core.Utils;
import org.apache.tomcat.util.http.fileupload.IOUtils;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.core.env.Environment;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RestController;

import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStream;


/**
 * Public API
 */
@RestController
@RequestMapping("/world")
public class FilesApi {

	private final Logger log = LoggerFactory.getLogger(this.getClass());
	private static final String SERVICE_NAME = "API for downloading files for XR clients";
	private static final String DEFAULT_WORLD_PATH = "./spring-core/world/";

	@Autowired
	private Environment env;

	@RequestMapping("")
	public String index(HttpServletResponse response, HttpServletRequest request) {
		Utils.logRequest(request, this.getClass());
		return SERVICE_NAME;
	}


	@RequestMapping(value = "/{file_name}.{file_extension}", method = RequestMethod.GET)
	public void getFile(
			@PathVariable("file_name") String fileName,
			@PathVariable("file_extension") String fileExtension,
			HttpServletResponse response, HttpServletRequest request) {
		Utils.logRequest(request, this.getClass());
		String completeFileName = fileName + "." + fileExtension;
		InputStream is = null;
		File f;

		try {
			String worldPath = env.getProperty("world.path");
			if (worldPath == null || worldPath.isEmpty()) {
				worldPath = DEFAULT_WORLD_PATH;
			}

			String src = worldPath + completeFileName;
			f = new File(src);
			is = new FileInputStream(f);

			response.setContentType("application/force-download");
			response.addHeader("Content-Disposition","attachment;filename=\"" + completeFileName + "\"");
			response.addHeader("Content-Length", Long.toString(f.length()));

			IOUtils.copy(is, response.getOutputStream());
			response.flushBuffer();
		} catch (IOException ex) {
			log.info("File error for: " + completeFileName);
			// If map was not found: send size = 220
			response.addHeader("Content-Length", "220");
			response.setStatus(404);
		} finally {
			try {
				if (is != null) {
					is.close();
				}
			} catch (IOException ignored) {
				log.info("Error closing the file");
			}
		}

	}

}
