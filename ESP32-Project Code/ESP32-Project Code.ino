#include "DHTesp.h"
#include "DFRobot_RGBLCD1602.h"

char dtaUart[15];
char dtaLen = 0;

DFRobot_RGBLCD1602 lcd(/*lcdCols*/16,/*lcdRows*/2);  //16 characters and 2 lines of show

//Temperature chip i/o
//OneWire ds(DS18S20_Pin);  // on digital pin 2

DHTesp dht;
TempAndHumidity measurement;

// Define the pins of the Arduino where the current signal is to be read
const int SensorPin = A2;

// Define the current sensor data
const int Rshunt = 33.3;                // Transformer resistance Resistencia. 30 A Model: 33.3 ohms
double n_transf = 1000;                  // Number of turns between the primary and secondary windings

// Variables to track the passing of one milissecond
unsigned long time_now = 0, time_int = 0;
unsigned long time_ant = 0, difTime = 0, act_time = 0, reading_time = 0, dif_reading_time = 0;

// Define the variables to calculate the RMS for one cycle of the grid
double quadratic_sum_rms = 0.0;         // Variable that stores the accumulated value of the quadratic sum of the instant current
const int sampleDuration = 20;          // Sample duration of the data retrieval (20 milissenconds = 1/50 Hz)
int quadratic_sum_counter = 0;          // Counter for the number of readings retrieved
double freq = 50.0;                     // Grid frequency

// Define the variables to calculate the current mean
double corriente_acumulada = 0.0;       // Acumulador de valores RMS para hacer la media
const int sampleAverage = 250;          // Numero de samples que determina cada cuantas muestras se hace la media de los RMS
int contador_acumulado = 0;             // Contador de cuantas veces se ha acumulado valores de RMS
double calibration_V = 0;

double suma_v;                          // Acumulador de valores RMS para hacer la media
int read_voltage;                       // Auxiliary variable to store the value of each voltage read from the sensor
int voltages_read_sum = 0;              // Variable to store the sum of the voltages read from the sensor
int counter = 0;                        // Number of voltages read from the sensor
int counter_v;

char comando;
int kettle_mode;

double steam_sum = 0.0;   //steam quatratic_sum
double steam_media = 0.0;

double temp_water_sum = 0.0; // To filter water temperature sensor
double temp_water_media = 0.0;
//=================================================================================================================================
// Function SETUP: Function that only executes once, at the beginning of runtime
//=================================================================================================================================
void setup()
{
  // Inicializar el periferico del puerto serie para poder imprimir datos a una velocidad de 115200 bits por segundos
  Serial.begin(115200);

  // Initialize the relay controller OFF
  pinMode(D2, OUTPUT);
  digitalWrite(D2, LOW);
  kettle_mode = 0;

  dht.setup(D3, DHTesp::DHT22);

  time_ant = micros();

  read_voltage = 0;
  counter = 0;

  while(time_int<2000) // 2 seconds to calibrate voltage
  {
    // Read voltage from Arduino pin -> value ranges between 0 and 4095
    read_voltage = analogRead(SensorPin);

    voltages_read_sum = voltages_read_sum + read_voltage;
    counter = counter + 1;

    reading_time = micros();

    // Keep track of the 2 sec calibration time
    time_int = reading_time - time_ant;
  }

  // Calibration voltage is obtained by converting the 0 -> 4095 signal reading scale into voltage, with linear relationship and max voltage of 3.3V
  calibration_V = double((voltages_read_sum/4095.0)*3.3/counter);

  // Print calibration voltage to make sure the circuit is running properly
  //Serial.println(calibration_V);
  //act_time = micros();

  lcd.init();
  // Print a message to the LCD.
  lcd.print("Setup finished...");
  delay(1500);
  lcd.init();

}


//=================================================================================================================================
// Function LOOP: Function that runs on an infinite loop (same as a while(true) statement)
//=================================================================================================================================
void loop()
{

  if (Serial.available() > 0)
  {
    comando = Serial.read();

    if (comando == 'H')
    {
      digitalWrite(D2, HIGH);
      kettle_mode = 1;
    }
    else if (comando == 'L')
    {
      digitalWrite(D2, LOW);
      kettle_mode = 0;
    }
  }

  // STEAM SENSOR
    float sensorValue1;
    float steam_percentage;
    sensorValue1 = analogRead(A4);   //connect Steam sensors to Analog 4
    steam_percentage = sensorValue1/4095.0*100.0;

  // NEW TEMPERATURE SENSOR
    uint16_t read_water_temp;
    double temp_water;
    read_water_temp = analogRead(A1);
    temp_water = (double) ((read_water_temp * (3.3 / 4095.0)) - 0.05)*100.0;

  //Serial.println(calibration_V);
    // Leer el tiempo en microsegundos desde el arranque del arduino
    act_time = micros();
    // Calcular la diferencia de tiempo entre el tiempo actual y la ultima vez que se actualizó la corriente instantanea
    difTime = act_time - time_ant;
    dif_reading_time = act_time - reading_time;
    // CADA 1 MILISEGUNDO, LEER ADC Y CALCULAR LA CORRIENTE INSTANTANEA PARA CALCULAR EL RMS

    //Serial.println(difTime);

    if (difTime >= 1000 && counter_v > 0)
    {
        // Actualizar el registro de tiempo con el tiempo actual
        time_ant = act_time + (difTime - 1000);

        double V_media = suma_v / counter_v;


        // Calibration of the midpoint tension

        double d_V = V_media - calibration_V;

        // Calculation of the instantaneous current
        double Iinst =  n_transf*d_V/Rshunt;

        // Calculation the quadratic sum I
        quadratic_sum_rms += ((Iinst*Iinst) * 0.001);
        // Calculation the Steam average value
        steam_media = steam_sum / counter_v;
        steam_sum = 0;
        // Calculation the Steam average value
        temp_water_media = temp_water_sum / counter_v;
        temp_water_sum = 0;

        // Incrementar el contador de muestras del acumulador del RMS
        quadratic_sum_counter++;
        suma_v = 0;
        counter_v = 0;
    }
//=============================================================================================================================================================
// FILTER
// Cogemos n muestras de la medida para filtrar el ruido del adc

    if (dif_reading_time >= 100){
      reading_time = act_time;

      // Leer del ADC las tensiones del tensor (devuelve datos entre 0 y 4095, el ADC del ESP32 es de 12 bits)
      int ADC_sensor = analogRead(SensorPin);
      double t = double(ADC_sensor/4095);
      //Serial.println(ADC_sensor);

      // Translate ADC values to tension values
      double V_sens = ADC_sensor * 3.3 / 4095.0;

      suma_v += V_sens;

      steam_sum += steam_percentage;
      temp_water_sum += temp_water;

      counter_v += 1;
    }
    else;
//=============================================================================================================================================================

    // EAH CYCLE OF THE GRID (20 ACCUMULATED VALUES), CALCULATE RMS
    if (quadratic_sum_counter >= sampleDuration)
    {

      //=================================================================================================================================
      // TO DO: Compute the square root in order to calculate the RMS of the last cicle
      //double Vrms = V_sens/counter_v;
      double Irms = sqrt(freq * quadratic_sum_rms);
      //=================================================================================================================================

        // Reiniciar valores de acumulación para calcular el RMS del último ciclo de red
        quadratic_sum_counter = 0;
        quadratic_sum_rms = 0;

        // Acumular valores de corriente RMS para calcular el promedio de RMS
        corriente_acumulada += Irms;
        contador_acumulado++;
    }
    else;

    // CADA 250 CICLOS DE RED (aproximadamente 5 segundos), CALCULAR EL RMS PROMEDIO
    if (contador_acumulado >= sampleAverage)
    {
        // Calcular la media de la corriente RMS promediado
        double Irms_filt = corriente_acumulada / ((double)contador_acumulado);

        // Reiniciar valores de acumulación para calcular el RMS promediado
        corriente_acumulada = 0;
        contador_acumulado = 0;
        // Imprimir la corriente filtrada, y la potencia (P = V*I = 230 * I)
        Serial.print(kettle_mode);
        Serial.print(" ");
        Serial.print(230.0*Irms_filt);
        Serial.print(" ");
        Serial.print(Irms_filt);
        Serial.print(" ");

        // TEMPERATURE AND HUMIDITY SENSOR
        if (!isnan(dht.getTempAndHumidity().temperature) && !isnan(dht.getTempAndHumidity().humidity)){
          measurement = dht.getTempAndHumidity();
        }

        Serial.print(measurement.temperature);
        Serial.print(" ");

        Serial.print(measurement.humidity);
        Serial.print(" ");

        Serial.print(steam_media); //print the value to serial
        Serial.print(" ");

        Serial.println(temp_water_media);

        // DISPLAY

        lcd.setCursor(0,0);
        lcd.print("T:");
        lcd.print(measurement.temperature);
        lcd.print(" C");
        lcd.setCursor(0,1);
        lcd.print("H:");
        lcd.print(steam_media);
        lcd.print(" %");

    }
    else;
}