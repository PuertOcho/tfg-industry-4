package com.app.tfgcrudserver.service;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

import org.apache.spark.sql.Dataset;
import org.apache.spark.sql.Row;
import org.apache.spark.sql.SparkSession;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.stereotype.Service;

@Service
public class SparkService {

	private String rutaScripts = "C:\\Users\\anton\\pyCharmProject\\pyspark-getting-started-master\\";

	
	public void sparkAction(String action) {
		try {
			String aux = System.getProperty("user.dir");
			//ProcessBuilder builder = new ProcessBuilder("python", System.getProperty("user.dir") + "\\pythonScripts\\spark_submit.py save");
			//Process process = builder.start();
			
			// Process p = Runtime.getRuntime().exec("python " + System.getProperty("user.dir") + "\\pythonScripts\\spark_submit.py save");
			String command = "python " + rutaScripts + "spark_submit.py save";
			Process p = Runtime.getRuntime().exec(command);

			BufferedReader in = new BufferedReader(new InputStreamReader(p.getInputStream()));
			//int ret = new Integer(in.readLine()).intValue();
			System.out.println("value is : ");
			
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}
	
}