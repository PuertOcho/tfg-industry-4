#include <Arduino.h>
#include <Time.h>
#include <SoftwareSerial.h>
#include <TinyGPS.h>
#include <dhtnew.h>

TaskHandle_t Task2;
int gobla_val = 0;
unsigned long myTime =0;
TinyGPS gps;
DHTNEW mySensor(4);

SoftwareSerial ss(16, 17); //SoftwareSerial for SIM800L
SoftwareSerial ss2(3, 1); //SoftwareSerial for GPS . 3,1
int step = 0;
float latitude = 0.0, longitude = 0.0;
String strLatitude = "";
String strLongitude = "";
String strTemperature = "";
String strHumidity = "";


void comandoAT_CIPSHUT(){
    ss.println("AT+CIPSHUT");//Consultar el estado actual de la conexión
    delay(1000);
    String debug1 = "";
      while(ss.available()!=0){
        debug1 = ss.readStringUntil('\n');
        debug1.trim();
        Serial.println("debug:" +debug1);

        if(debug1.equals("SHUT OK")){  step = 0; Serial.print("CIPSHUT aceptado");}
          
        else{          Serial.print("debug1:"+debug1);        }
        Serial.print("\n");
    } 
}

void comandoAT(){
    ss.println("AT");//Chequear si recibe comandos
    delay(1000);
    String debug1 = "";
      while(ss.available()!=0){
        debug1 = ss.readStringUntil('\n');
        debug1.trim();
        Serial.println("debug:" +debug1);

        if(debug1.equals("OK")){  step = 1; Serial.print("AT aceptado");}
        if(debug1.equals("SMS Ready")){  step = 0; delay(15000); Serial.print("No hay conexion");}
        
        Serial.print("\n");
    } 
}

void comandoAT_CIPSTATUS(){
    ss.println("AT+CIPSTATUS");//Consultar el estado actual de la conexión
    delay(1000);
    String debug1 = "";
      while(ss.available()!=0){
        debug1 = ss.readStringUntil('\n');
        debug1.trim();
        Serial.println("debug:" +debug1);

        if(debug1.equals("OK")){  step = 2; Serial.print("CIPSTATUS aceptado");}
        if(debug1.equals("ERROR")){  step = 0; Serial.print("CIPSTATUS error");}
        if(debug1.equals("STATE: TCP CLOSED")){  
          step = 0; 
          ss.println("AT+CIPSHUT");
          Serial.print("Cierre de la conexion");}
        if(debug1.equals("SMS Ready")){  step = 0; delay(15000); Serial.print("No hay conexion");}
        else{          Serial.print("debug1:"+debug1);        }
        Serial.print("\n");
    } 
}

void comandoAT_CIPMUX(){
    ss.println("AT+CIPMUX=0");//Consultar el estado actual de la conexión
    delay(1000);
    String debug1 = "";
      while(ss.available()!=0){
        debug1 = ss.readStringUntil('\n');
        debug1.trim();
        Serial.println("debug:" +debug1);

        if(debug1.equals("ERROR")){  
          step = 0; 
          Serial.print("CIPMUX error");
          comandoAT_CIPSHUT();}

        if(debug1.equals("OK")){  step = 3; Serial.print("CIPMUX aceptado");}
        if(debug1.equals("SMS Ready")){  step = 0; delay(15000); Serial.print("No hay conexion");} 
        else{          Serial.print("debug1:"+debug1);        }
        Serial.print("\n");
        
    } 
}

void comandoAT_CSTT(){
    ss.println("AT+CSTT=\"orangeworld\",\"\",\"\"");//comando configura el APN, nombre de usuario y contraseña."gprs.movistar.com.ar","wap","wap"->Movistar Arg.
    delay(2000);
    String debug1 = "";
      while(ss.available()!=0){
        debug1 = ss.readStringUntil('\n');
        debug1.trim();
        Serial.println("debug:" +debug1);

        if(debug1.equals("OK")){  step = 4; Serial.print("CSTT aceptado");}
        if(debug1.equals("ERROR")){  step = 0; Serial.print("CSTT error");}
        if(debug1.equals("SMS Ready")){  step = 0; delay(15000); Serial.print("No hay conexion");}
        else{          Serial.print("debug1:"+debug1);        }
        Serial.print("\n");
        
    } 
}

void comandoAT_CIICR(){
    ss.println("AT+CIICR");//Consultar el estado actual de la conexión
    delay(2000);
    String debug1 = "";
      while(ss.available()!=0){
        debug1 = ss.readStringUntil('\n');
        debug1.trim();
        Serial.println("debug:" +debug1);

        if(debug1.equals("OK")){  step = 5; Serial.print("CIICR aceptado");}
        if(debug1.equals("ERROR")){  step = 0; Serial.print("CIICR error");}
        else{          Serial.print("debug1:"+debug1);        }
        Serial.print("\n");
    } 
}

void comandoAT_CIFSR(){
    ss.println("AT+CIFSR");//Consultar el estado actual de la conexión
    delay(2000);
    String debug1 = "";
      while(ss.available()!=0){
        debug1 = ss.readStringUntil('\n');
        debug1.trim();
        Serial.println("debug:" +debug1);

        //if(debug1.equals("OK")){  step = 6; }
        step = 6; Serial.print("CIFSR aceptado");
       
        Serial.print("debug1:"+debug1);
        Serial.print("\n");
    } 
}

void comandoAT_CIPSPRT(){
    ss.println("AT+CIPSPRT=0");//Consultar el estado actual de la conexión
    delay(1000);
    String debug1 = "";
      while(ss.available()!=0){
        debug1 = ss.readStringUntil('\n');
        debug1.trim();
        Serial.println("debug:" +debug1);

        if(debug1.equals("OK")){  step = 7; Serial.print("CIPSPRT aceptado");}
        if(debug1.equals("ERROR")){  step = 0; Serial.print("CIPSPRT error");}  
        else{          Serial.print("debug1:"+debug1);        }
        Serial.print("\n");
    } 
}

void comandoAT_CIPSTART(){
    ss.println("AT+CIPSTART=\"TCP\",\"api.thingspeak.com\",\"80\"");//Consultar el estado actual de la conexión
    delay(2000);
    String debug1 = "";
      while(ss.available()!=0){
        debug1 = ss.readStringUntil('\n');
        debug1.trim();
        Serial.println("debug:" +debug1);

        if(debug1.equals("OK")){  step = 8; Serial.print("CIPSTART aceptado");}
        if(debug1.equals("ERROR")){  step = 0; Serial.print("CIPSTART error");}  
        else{          Serial.print("debug1:"+debug1);        }
        Serial.print("\n");
    } 
}

void comandoAT_CIPSEND(){

    String datos="GET https://api.thingspeak.com/update?api_key=3IN7GNVRE2JGQG53&field2="+strLatitude+"&field3="+strLongitude+"&field1="+strTemperature+"&field4="+strHumidity; //funciona con 100
    
    Serial.println("datos.length():" + String(datos.length()+5));
    ss.println("AT+CIPSEND="+ String(datos.length()+5));//Consultar el estado actual de la conexión
    delay(1000);
    
    Serial.println("datos:" + datos);
    ss.println(datos);//Envía datos al servidor remoto
    delay(5000);

    String debug1 = "";
      while(ss.available()!=0){
        debug1 = ss.readStringUntil('\n');
        debug1.trim();
        Serial.println("debug:" +debug1);

        if(debug1.equals("SEND OK")){  step = 9; Serial.print("CIPSEND aceptado");}
        if(debug1.equals("ERROR")){  step = 0; Serial.print("CIPSEND error");} 
        else{          Serial.print("debug1:"+debug1);        }
        Serial.print("\n");
    }

}

void loop()
{

    bool newData = false;

    // For one second we parse GPS data and report some key values
    for (unsigned long start = millis(); millis() - start < 1000;)
    {
      while (ss2.available())
      {
        char c = ss2.read();
        // Serial.write(c); // uncomment this line if you want to see the GPS data flowing
        if (gps.encode(c)) // Did a new valid sentence come in?
          newData = true;
      }
    }

    if (newData)    {

      float flat, flon;
      unsigned long age;

      gps.f_get_position(&flat, &flon, &age);

      
      strLongitude = String((flon == TinyGPS::GPS_INVALID_F_ANGLE ? 0.0 : flon ), 6);
      //Serial.print(" longitude="+strLongitude);

      
      strLatitude = String((flat == TinyGPS::GPS_INVALID_F_ANGLE ? 0.0 : flat ), 6);
      //Serial.print(" latitude="+strLatitude);



    }
    
    // Temperature
    mySensor.read();
    strHumidity =  String(mySensor.getHumidity(), 1);
    strTemperature =  String(mySensor.getTemperature(), 1);

  
 


}



void loop2(void *parameter){
  for(;;) {
    printf(" Hilo 1 \n");
    delay(100);
    if(step == 0){comandoAT();}
    if(step == 1){comandoAT_CIPSTATUS();}
    if(step == 2){comandoAT_CIPMUX();}
    if(step == 3){comandoAT_CSTT();}
    if(step == 4){comandoAT_CIICR();}
    if(step == 5){comandoAT_CIFSR();}
    if(step == 6){comandoAT_CIPSPRT();}
    if(step == 7){comandoAT_CIPSTART();}
    if(step == 8){comandoAT_CIPSEND();}
    if(step == 9){comandoAT_CIPSHUT();}
  }
}

void setup()
{
  xTaskCreatePinnedToCore(    loop2,    "Task2",    8192,    NULL,    1,    &Task2,    0);
  
  mySensor.setHumOffset(10);
  mySensor.setTempOffset(-3.5);

  Serial.print("Simple TinyGPS library v. "); Serial.println(TinyGPS::library_version());
  Serial.println("by Mikal Hart");
  Serial.println();

  ss.begin(19200);//Arduino se comunica con el SIM900 a una velocidad de 19200bps   
  Serial.begin(115200);//Velocidad del puerto serial de arduino

  Serial.println("Empezando");
  delay(10000);//Tiempo prudencial para el escudo inicie sesión de red con tu operador
  Serial.println("Ya");

  ss2.begin(9600);
  Serial.print("Simple TinyGPS library v. "); 
  Serial.println(TinyGPS::library_version());
  Serial.println("by Mikal Hart");
  Serial.println();

}