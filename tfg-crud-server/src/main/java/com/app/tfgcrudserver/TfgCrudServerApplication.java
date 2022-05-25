package com.app.tfgcrudserver;

import java.util.List;

import org.apache.catalina.security.SecurityConfig;
import org.apache.spark.SparkConf;
import org.apache.spark.api.java.JavaSparkContext;
import org.apache.spark.sql.Dataset;
import org.apache.spark.sql.Row;
import org.apache.spark.sql.SparkSession;
import org.bson.Document;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.boot.CommandLineRunner;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.data.mongodb.repository.config.EnableMongoRepositories;

import com.app.tfgcrudserver.repository.ProcessTaskRepository;
import com.mongodb.spark.MongoSpark;
import com.mongodb.spark.rdd.api.java.JavaMongoRDD;


@SpringBootApplication
@EnableMongoRepositories
public class TfgCrudServerApplication implements CommandLineRunner{

	@Autowired
	ProcessTaskRepository processTaskRepository; 
	
	public static void main(String[] args) {
		SpringApplication.run(TfgCrudServerApplication.class, args);
	}
	
	@Override
	public void run(String... args) throws Exception {
		// TODO Auto-generated method stub
		
		Long res = processTaskRepository.count();
		System.out.println("res: " + res);
		//List<ProcessTask> aa = processTaskRepository.findProcessByTask("AA");
		//System.out.println("aa: " + aa);
		
		//ProcessTask pT = new ProcessTask("aaa", "aaa", "", 123456L, "", "", new String[]{}, "", "", 15.65, 15.65, 15.65, 15.65, "", 15.65, new String[]{}, new StorageModel[]{});
		//processTaskRepository.save(pT);
		//System.out.println("res: " + res);
		
	}

}
