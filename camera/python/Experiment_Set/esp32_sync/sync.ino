#define syncPin 4 // Trigger Pin

int val = 0;
int sync = 0;

void setup() {
  Serial.begin( 9600 );
  pinMode( syncPin, INPUT );
  
}

void loop() {
  
  while (sync == 0){
    val = digitalRead(syncPin);
    if (val == HIGH) {
      const char* val_str = "HIGH";
    }
    else {
      const char* val_str = "LOW";
      Serial.println(1);
      sync = 1;
    }
//    Serial.println("val");
//    Serial.println(val);
  }
}
