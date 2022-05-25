package com.app.tfgcrudserver.controller;

import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import com.app.tfgcrudserver.model.ProcessTask;
import com.app.tfgcrudserver.repository.ProcessTaskRepository;
import com.app.tfgcrudserver.service.TFGService;
import com.app.tfgcrudserver.service.SparkService;

@RestController
@RequestMapping("/api")
public class TFGController {

	@Autowired
	private ProcessTaskRepository processTaskRepository;
	
	@Autowired
	private SparkService sparkService;
	
	@Autowired
	protected TFGService tfgService; 
	
	@GetMapping("/count")
	public long countCollection() {
	  return processTaskRepository.count();
	}
	
	@GetMapping("/find")
	public void findCollection(@RequestParam(value = "task", required = false) String task) {
		List<ProcessTask> res = processTaskRepository.findProcessByTask(task);
		System.out.println("" + res.toString());
	}
	
	@GetMapping("/sparkAction")
	public void sparkTest(@RequestParam(value = "action", required = false) String action) {
	  sparkService.sparkAction(action);
	}
	
}