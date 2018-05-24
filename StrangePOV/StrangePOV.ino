/* StrangePOV - May 23, 2018
 *  Author: Gregory Mark
 *  
 *  The purpose of this code is to create a POV display that
 *   mimics the mystical sheild spells (and other spells) of
 *   Doctor Strange in the Marvel Cinematic Universe.
 *   
 *   With the flexibility of the POV display, this can certainly
 *   be used to display other images, however, this piece of
 *   code in particular is used for the Doctor Strange spells.
 *   
 *  Abbreviations:
 *    tr = average time per revolution (us)
 *    tw = time of delay per angle increment (us)
 *    na = number of angle shifts per rotation 
 *    nc = number of approximate clock cycles per angle shift
 *    
 *  Calculations:
 *  
 *    tw = tr/na - nc * 16MHz * 1000000 (us/s)
 *   
 *  Operational Steps:
 *    1. Turn on PCB board
 *    2. Select programmed image (spell to display)
 *    3. Turn on DC motor
 *    4. Measure tr
 *    5. Load Image (if using EEPROM, which I don't think I am)
 *    6. Set tw to loop delay.
 *    7. Update image refresh loop, and set delay.
 *    8. Repeat
 */
int na = 240;
int nc = 300;
long tr = 0;
long tw = 0;

int pushButtonPin = 1;
int latchPin = 1;
int clockPin = 1;
int dataPin = 1;
int hallEffectPin = 1;

int lengthLED = 120; //x40 RGB LEDs
boolean registers[lengthLED]; //index 0 is the closest to the center

int revInitDiscard = 50;
int revLimit = 20;
int revCount = 0;
unsigned long prevTime = 0;
unsigned long currTime = 0;
int sumTime = 0;



/*
 * Setup
 */
void setup() {
  pinMode(pushButtonPin, INPUT);

  //Shift registers
  pinMode(latchPin, OUTPUT);
  pinMode(clockPin, OUTPUT);
  pinMode(dataPin, OUTPUT);

  //Hall Effect Sensor
  Serial.begin(9600);
  attachInterrupt(hallEffectPin, calibrateRPM, RISING);
}


/*
 * Main Loop
 */
void loop() {

  //Display POV
  if (tr > 0) {


    
  }
  

}

/*
 * Functions
 */

// Discard first few rotations until steady speed.
//  Then calculate average rotation time in us, set to tr.
//  Detach Interrupt
void calibrateRPM(){
  
  if (revInitDiscard > 0){
    revInitDiscard--;
    prevTime = micros();
    
  } else if (revCount < revLimit) {
    currTime = micros();
    sumTime += currTime - prevTime;
    revCount++;
    prevTime = micros();
    
  } else {
    tr = calculateTr();
    detachInterrupt();   
  }
}

long calculateTr(){
  return sumTime/limitRev;
}

long calculateTw() {


  
}

//Approx 482 clock cycles
void writeDataToLEDS(){

  digitalWrite(latchPin, LOW);

  //Clock in all of the bits to the LED's shift registers
  for (int i = lengthLED - 1; i>=0; i--){
    digitalWrite(clockPin, LOW);
    digitalWrite(dataPin, registers[i]);
    digitalWrite(clockPin, HIGH);
  }

  //Latch all of the data to output
  digitalWrite(latchPin, HIGH);
}




