package com.app.tfgcrudserver.repository;

import java.util.List;

import org.springframework.data.mongodb.repository.MongoRepository;
import org.springframework.data.mongodb.repository.Query;
import org.springframework.stereotype.Repository;

import com.app.tfgcrudserver.model.ProcessTask;

@Repository
public interface ProcessTaskRepository extends MongoRepository<ProcessTask, String> {
    
	@Query("{task:'?0'}")
    List<ProcessTask> findProcessByTask(String task);
    
	@Query("{timestamp:'?0'}")
    List<ProcessTask> findProcessByTimestamp(Long timestamp);
	
    public long count();
}
