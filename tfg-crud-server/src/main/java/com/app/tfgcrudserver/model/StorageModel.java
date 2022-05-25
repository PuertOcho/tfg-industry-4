package com.app.tfgcrudserver.model;


public class StorageModel {

    private String pallet;
    private String hall;
    private Integer number;

    public StorageModel(String pallet, String hall, Integer number) {
        this.pallet = pallet;
        this.hall = hall;
        this.number = number;
    }

	public String getPallet() {
		return pallet;
	}

	public void setPallet(String pallet) {
		this.pallet = pallet;
	}

	public String getHall() {
		return hall;
	}

	public void setHall(String hall) {
		this.hall = hall;
	}

	public Integer getNumber() {
		return number;
	}

	public void setNumber(Integer number) {
		this.number = number;
	}

	@Override
	public String toString() {
		return "StorageModel [pallet=" + pallet + ", hall=" + hall + ", number=" + number + "]";
	}

    
}
