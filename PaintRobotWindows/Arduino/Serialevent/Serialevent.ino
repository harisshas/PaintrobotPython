
void setup() 
{
  Serial.begin(9600);
  Serial.println("stat*commstart");
  
  delay(1000);
  Serial.println("stat*noresettpos");

  
}

void loop() 
{

}

void serialEvent() 
{
  String inputstring;
  String instructString="";
  int instructval=0;
  String Xval="";
  String Yval="";
  int xval=0;
  int yval=0;
  int countlimiter=0;
  while(Serial.available())
  {
          inputstring=Serial.readString();
          //Serial.println(inputstring);
  }
  for(int i=0;i<inputstring.length();i++)
  {
          char inChar = inputstring[i];
          if(inChar=='*')
          {
             countlimiter++;
             continue;
          }
          switch(countlimiter)
          {
            case 0:
              instructString+=inChar;
              break;
            case 1:
              Xval+=inChar;
              break;
            case 2:  
              Yval+=inChar;
              break;
          }
  }
  instructval=instructString.toInt();
  if(instructval==2)
  {
   //reset command recieved
   Serial.println("stat*resetting");
   delay(3000);
   Serial.println("stat*resetpos");
  }
  if(instructval==3)
  {
   //reset command recieved
   Serial.println("stat*inching up");
   delay(3000);
   Serial.println("stat*inchcomp");
   checkresetposition();
  }
  if(instructval==4)
  {
   //reset command recieved
   Serial.println("stat*inching down");
   delay(3000);
   Serial.println("stat*inchcomp");
   checkresetposition();
  }
  if(instructval==5)
  {
   //reset command recieved
   Serial.println("stat*inching left");
   delay(3000);
   Serial.println("stat*inchcomp");
   checkresetposition();
  }
  if(instructval==6)
  {
   //reset command recieved
   Serial.println("stat*inching right");
   delay(3000);
   Serial.println("stat*inchcomp");
   checkresetposition();
  }
  if(instructval==7)
  {
   //reset command recieved
   Serial.println("stat*sprayinch");
   delay(3000);
   Serial.println("stat*inchspraycomp");
   checkresetposition();
  }
}
void checkresetposition()
{
  delay(1000);
  Serial.println("stat*noresettpos");
}

