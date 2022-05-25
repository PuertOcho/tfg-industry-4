package com.app.tfgcrudserver.model;


import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.mapping.Document;
import org.springframework.data.mongodb.core.mapping.Field;

import lombok.Data;

@Data
@Document(collection = "TFGCollection")
public class ProcessTask {

    @Id
    private String id;

    @Field("stage")
    private String stage;
    
    @Field("task")
    private String task;
    
    @Field("timestamp")
    private Long timestamp;
    
    @Field("worker")
    private String worker;
    
    @Field("supplier")
    private String supplier;
    
    @Field("milkTanks")
    private String[] milkTanks;

    @Field("order")
    private String order;
    
    @Field("tansport")
    private String tansport;

    @Field("temperature")
    private Double temperature;
    
    @Field("humidity")
    private Double humidity;
    
    @Field("latitude")
    private Double latitude;
    
    @Field("longitude")
    private Double longitude;

    @Field("milkTank")
    private String milkTank;
    
    @Field("preasure")
    private Double preasure;

    @Field("pallets")
    private String[] pallets;

    @Field("storage")
    private StorageModel[] storage;

    public ProcessTask(String id, String stage, String task, Long timestamp, String worker, String supplier, String[] milkTanks, String order, String tansport, Double temperature, Double humidity, Double latitude, Double longitude, String milkTank, Double preasure, String[] pallets, StorageModel[] storage) {
    	super();
    	this.id = id;
        this.stage = stage;
        this.task = task;
        this.timestamp = timestamp;
        this.worker = worker;
        this.supplier = supplier;
        this.milkTanks = milkTanks;
        this.order = order;
        this.tansport = tansport;
        this.temperature = temperature;
        this.humidity = humidity;
        this.latitude = latitude;
        this.longitude = longitude;
        this.milkTank = milkTank;
        this.preasure = preasure;
        this.pallets = pallets;
        this.storage = storage;
    }

    public String getId() {
        return id;
    }

    public void setId(String id) {
        this.id = id;
    }

    public String getStage() {
        return stage;
    }

    public void setStage(String stage) {
        this.stage = stage;
    }

    public String getTask() {
        return task;
    }

    public void setTask(String task) {
        this.task = task;
    }

    public Long getTimestamp() {
        return timestamp;
    }

    public void setTimestamp(Long timestamp) {
        this.timestamp = timestamp;
    }

    public String getWorker() {
        return worker;
    }

    public void setWorker(String worker) {
        this.worker = worker;
    }

    public String getSupplier() {
        return supplier;
    }

    public void setSupplier(String supplier) {
        this.supplier = supplier;
    }

    public String[] getMilkTanks() {
        return milkTanks;
    }

    public void setMilkTanks(String[] milkTanks) {
        this.milkTanks = milkTanks;
    }

    public String getOrder() {
        return order;
    }

    public void setOrder(String order) {
        this.order = order;
    }

    public String getTansport() {
        return tansport;
    }

    public void setTansport(String tansport) {
        this.tansport = tansport;
    }

    public Double getTemperature() {
        return temperature;
    }

    public void setTemperature(Double temperature) {
        this.temperature = temperature;
    }

    public Double getHumidity() {
        return humidity;
    }

    public void setHumidity(Double humidity) {
        this.humidity = humidity;
    }

    public Double getLatitude() {
        return latitude;
    }

    public void setLatitude(Double latitude) {
        this.latitude = latitude;
    }

    public Double getLongitude() {
        return longitude;
    }

    public void setLongitude(Double longitude) {
        this.longitude = longitude;
    }

    public String getMilkTank() {
        return milkTank;
    }

    public void setMilkTank(String milkTank) {
        this.milkTank = milkTank;
    }

    public Double getPreasure() {
        return preasure;
    }

    public void setPreasure(Double preasure) {
        this.preasure = preasure;
    }

    public String[] getPallets() {
        return pallets;
    }

    public void setPallets(String[] pallets) {
        this.pallets = pallets;
    }

    public StorageModel[] getStorage() {
        return storage;
    }

    public void setStorage(StorageModel[] storage) {
        this.storage = storage;
    }

	@Override
	public String toString() {
		return "ProcessTask [id=" + id + ", stage=" + stage + ", task=" + task + ", timestamp=" + timestamp + "]";
	}
	
}
