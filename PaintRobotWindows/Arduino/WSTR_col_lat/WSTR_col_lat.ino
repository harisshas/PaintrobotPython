const int maxrowcount=3;
const int maxcolcount=3;

int rowcount=maxrowcount;
int colcount=maxcolcount;

boolean stackoccarray[maxrowcount][maxcolcount];
int stacklocarray[maxrowcount][maxcolcount];

int stacklocountstart=22;

int senspinarray[maxrowcount][maxcolcount];
int senspincountstart=36;

int rowmotorfwdpin=2;
int rowmotorrevpin=3;

int colmotorfwdpin=4;
int colmotorrevpin=5;

int traymotorfwdpin=6;
int traymotorrevpin=7;

int originpin=35;
int bottompin=53;

void initsenspinarray()
{
  int pincount=senspincountstart;
  for(int i=0;i<rowcount;i++)
  {
    for(int j=0;j<colcount;j++)
    {
      senspinarray[i][j]=pincount;
      pinMode(pincount,INPUT);
      //Serial.println("pin-"+String(pincount)+" input");
      pincount++;
    }
  }
}
int scanallsensors()
{
  for(int i=0;i<rowcount;i++)
  {
    for(int j=0;j<colcount;j++)
    {
      if(digitalRead(senspinarray[i][j])==LOW)
      {
        return senspinarray[i][j];
      }
    }
  }
  return 0;
}
void initialize(int xval, int yval)
{
  rowcount=xval;
  colcount=yval;
  initstacklocarray();
  initsenspinarray();
  Serial.println("msg*init complete");
}
void setup() 
{
  //assign digital pins that are connected to the load cells of the stack as inputs
  Serial.begin(9600);
  //Serial.println("Program started");
  //initstacklocarray();
  //initsenspinarray();
  //scanlcs();
  //printscanlcs();
}
void loop() 
{
  
}

void initstacklocarray()
{
  int pincount=stacklocountstart;
  pinMode(originpin,INPUT);
  pinMode(bottompin,INPUT);
  for(int i=0;i<rowcount;i++)
  {
    for(int j=0;j<colcount;j++)
    {
      stacklocarray[i][j]=pincount;
      pinMode(pincount,INPUT);
      //Serial.println("pin-"+String(pincount)+" input");
      pincount++;
    }
  }
}

void scanlcs()
{
  for(int i=0;i<rowcount;i++)
  {
    for(int j=0;j<colcount;j++)
    {
      stackoccarray[i][j]=!digitalRead(stacklocarray[i][j]);
      //Serial.println("row:"+String(i)+" column:"+String(j)+" value:"+String(digitalRead(stacklocarray[i][j])));
      /*if(digitalRead(stacklocarray[i][j])==true)
      {
        Serial.println("row:"+String(i)+" column:"+String(j)+" occupied.");
      }
      else
      {
        Serial.println("row:"+String(i)+" column:"+String(j)+" not-occupied.");
      }*/
    }
  }
}
void printscanlcs()
{
  String sendscanlcsstring="scan*";
  for(int i=0;i<rowcount;i++)
  {
    for(int j=0;j<colcount;j++)
    {
      if(stackoccarray[i][j]==true)
      {
        //Serial.println("row:"+String(i)+" column:"+String(j)+" occupied.");
        sendscanlcsstring.concat("1");
      }
      else
      {
        //Serial.println("row:"+String(i)+" column:"+String(j)+" not-occupied.");
        sendscanlcsstring.concat("0");
      }
    }
  }
  Serial.println(sendscanlcsstring);
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
    //Serial.println("recived scan instruction");
    scanlcs();
    printscanlcs();
   }
   else if(instructval==0)
   {
    xval=Xval.toInt();
    yval=Yval.toInt();
    //Serial.println("recived place instruction X:"+String(xval)+" Y:"+String(yval));
    place(xval, yval);
   }
   else if(instructval==1)
   {
    xval=Xval.toInt();
    yval=Yval.toInt();
    //Serial.println("recived retrieve instruction X:"+String(xval)+" Y:"+String(yval));
    retrieve(xval, yval);
   }
   else if(instructval==3)
   {
    xval=Xval.toInt();
    yval=Yval.toInt();
    //Serial.println("recived retrieve instruction X:"+String(xval)+" Y:"+String(yval));
    initialize(xval, yval);
   }
   else if(instructval==4)
   {
    rowmotorinchforward();
   }
   else if(instructval==5)
   {
    rowmotorinchreverse();
   }
   else if(instructval==6)
   {
    colmotorinchforward();
   }
   else if(instructval==7)
   {
    colmotorinchreverse();
   }
   else if(instructval==8)
   {
    traymotorinchforward();
   }
   else if(instructval==9)
   {
    traymotorinchreverse();
   }
   else if(instructval==10)
   {
    resetcarraige();
   }
}
void resetcarraige()
{
  Serial.println("stat*resetting");
  if(movetobottom())
  {
      if(movetoorigin())
      {
        Serial.println("stat*reset done");
      }
  }
}
void place(int xval, int yval)
{
  if(checkvalidcell(xval, yval))
  {
    if(checkinstructvalid(xval, yval, 0))
    {
      Serial.println("msg*recived retrieve instruction X:"+String(xval)+" Y:"+String(yval)+" all OK");
      if(!digitalRead(originpin))
      {
        if(movetocol(xval,yval))
        {
          if(movetorow(xval,yval))
          {
            if(incline())
            {
              travelback(xval, yval);
            }
          }
        }
      }
      else
      {
        Serial.println("err*carraige not in origin");
      }
    }
  }
}
void travelback(int xval, int yval)
{
  Serial.println("stat*travelling back");
  if(movebackrow(xval,yval))
  {
    if(movebackcol(xval,yval))
    {
      if(movetoorigin())
      {
        Serial.println("stat*complete");
      }
    }
  }
}
boolean movetoorigin()
{
  while(digitalRead(originpin))
  {
    colmotormovereverse();
    Serial.println("stat*move back to origin");
    delay(1000);
  }
  return true;
}
boolean movetobottom()
{
  while(digitalRead(bottompin))
  {
    rowmotormovereverse();
    Serial.println("stat*move back to bottom");
    delay(1000);
  }
  return true;
}

boolean movebackcol(int xval,int yval)
{
  boolean sequencecorrect=true;
  boolean operationcomplete=false;
  int destcell=senspinarray[0][0];
  int nextexpectedcell=senspinarray[0][yval];
  int prevcell=senspinarray[0][yval];
  int loopcount=0;
  while(sequencecorrect)
  {
    while(scanallsensors()==0)
    {
    colmotormovereverse();
    //Serial.println("movecolfwd");
    delay(1000);
    }
    
    if((scanallsensors()!=nextexpectedcell && scanallsensors()!=prevcell) || !digitalRead(originpin))
    {
      sequencecorrect=false;
      operationcomplete=false;
    }
    if(scanallsensors()!=nextexpectedcell && scanallsensors()==prevcell && digitalRead(originpin))
    {
      Serial.println("msg*back col seq correct passing through");
      delay(1000);
    }
    if((scanallsensors()==nextexpectedcell) && (destcell!=nextexpectedcell) && digitalRead(originpin))
    {
      Serial.println("msg*back col seq correct: "+String(loopcount));
      sequencecorrect=true;
      operationcomplete=false;
      prevcell=nextexpectedcell;
      loopcount++;
      nextexpectedcell=senspinarray[0][yval-loopcount];
    }
    if((scanallsensors()==nextexpectedcell) && (destcell==nextexpectedcell) && digitalRead(originpin))
    {
      sequencecorrect=false;
      operationcomplete=true;
    }
  }
  if(sequencecorrect==false && operationcomplete==false)
  {
    Serial.println("err*Wrong sequence back ");
    colmotorstop();
    return false;
  }
  else if(sequencecorrect==false && operationcomplete==true)
  {
    Serial.println("msg*Moved back to dest Y");
    colmotorstop();
    return true;
  }
}
boolean movebackrow(int xval,int yval)
{
  boolean sequencecorrect=true;
  boolean operationcomplete=false;
  int destcell=senspinarray[0][yval];
  int nextexpectedcell=senspinarray[xval][yval];
  int prevcell=senspinarray[xval][yval];
  int loopcount=0;
  while(sequencecorrect)
  {
    while(scanallsensors()==0)
    {
      rowmotormovereverse();
      //Serial.println("moverowfwd");
      delay(1000);
    }
    if((scanallsensors()!=nextexpectedcell && scanallsensors()!=prevcell)|| !digitalRead(originpin))
    {
      sequencecorrect=false;
      operationcomplete=false;
    }
    if(scanallsensors()!=nextexpectedcell && scanallsensors()==prevcell && digitalRead(originpin))
    {
      Serial.println("msg*row seq correct passing through back");
      delay(1000);
    }
    if((scanallsensors()==nextexpectedcell) && (destcell!=nextexpectedcell) && digitalRead(originpin))
    {
      Serial.println("msg*back row seq correct: "+String(loopcount));
      sequencecorrect=true;
      operationcomplete=false;
      loopcount++;
      prevcell=nextexpectedcell;
      nextexpectedcell=senspinarray[xval-loopcount][yval];
    }
    if((scanallsensors()==nextexpectedcell) && (destcell==nextexpectedcell) && digitalRead(originpin))
    {
      sequencecorrect=false;
      operationcomplete=true;
    }
  }
  if(sequencecorrect==false && operationcomplete==false)
  {
    Serial.println("err*Wrong sequence back ");
    rowmotorstop();
    return false;
  }
  else if(sequencecorrect==false && operationcomplete==true)
  {
    Serial.println("msg*Moved back to dest X");
    rowmotorstop();
    return true;
  }
}
void retrieve(int xval, int yval)
{
  if(checkvalidcell(xval, yval))
  {
    if(checkinstructvalid(xval, yval, 1))
    {
      Serial.println("msg*recived retrieve instruction X:"+String(xval)+" Y:"+String(yval)+" all OK");
      if(!digitalRead(originpin))
      {
        if(movetocol(xval,yval))
        {
          if(movetorow(xval,yval))
          {
            if(incline())
            {
              travelback(xval, yval);
            }
          }
        }
      }
      else
      {
        Serial.println("err*carraige not in origin");
      }
    }
  }
}
boolean incline()
{
            Serial.println("stat*tray movement");
            traymotormoveforward();
            delay(2000);
            traymotorstop();
            delay(2000);
            traymotormovereverse();
            delay(2000);
            traymotorstop();

            Serial.println("stat*incline movement");
            rowmotormoveforward();
            delay(500);
            rowmotorstop();
            delay(500);
            rowmotormovereverse();
            delay(500);
            rowmotorstop();
            return true;
}
boolean checkvalidcell(int xval, int yval)
{
  if(xval<0 || xval>=rowcount)
  {
    Serial.println("err*recived invalid co-ordinate");
    return false;
  }
  else if(yval<0 || yval>=colcount)
  {
    Serial.println("err*recived invalid co-ordinate");
    return false;
  }
  return true;
}
boolean checkinstructvalid(int xval, int yval, int instruction)
{
  if(String(instruction)==String(stackoccarray[xval][yval]))
  {
    return true;
  }
  else
  {
    Serial.println("err*recived invalid instruc");
    return false;
  }
}
void rowmotorinchforward()
{
  Serial.println("stat*row motor inch fwd");
  digitalWrite(rowmotorfwdpin,HIGH);
  digitalWrite(rowmotorrevpin,LOW);
  delay(2000);
  Serial.println("stat*row motor inch stop");
  digitalWrite(rowmotorfwdpin,LOW);
  digitalWrite(rowmotorrevpin,LOW);
}
void rowmotorinchreverse()
{
  Serial.println("stat*row motor inch rev");
  digitalWrite(rowmotorfwdpin,LOW);
  digitalWrite(rowmotorrevpin,HIGH);
  delay(2000);
  Serial.println("stat*row motor inch stop");
  digitalWrite(rowmotorfwdpin,LOW);
  digitalWrite(rowmotorrevpin,LOW);
}
void colmotorinchforward()
{
  Serial.println("stat*column motor inch fwd");
  digitalWrite(colmotorfwdpin,HIGH);
  digitalWrite(colmotorrevpin,LOW);
  delay(2000);
  Serial.println("stat*column motor inch stop");
  digitalWrite(colmotorfwdpin,LOW);
  digitalWrite(colmotorrevpin,LOW);
}
void colmotorinchreverse()
{
  Serial.println("stat*column motor inch rev");
  digitalWrite(colmotorfwdpin,LOW);
  digitalWrite(colmotorrevpin,HIGH);
  delay(2000);
  Serial.println("stat*column motor inch stop");
  digitalWrite(colmotorfwdpin,LOW);
  digitalWrite(colmotorrevpin,LOW);
}
void traymotorinchforward()
{
  Serial.println("stat*tray motor inch fwd");
  digitalWrite(traymotorfwdpin,HIGH);
  digitalWrite(traymotorrevpin,LOW);
  delay(1000);
  Serial.println("stat*tray motor inch stop");
  digitalWrite(traymotorfwdpin,LOW);
  digitalWrite(traymotorrevpin,LOW);
}
void traymotorinchreverse()
{
  Serial.println("stat*tray motor inch rev");
  digitalWrite(traymotorfwdpin,LOW);
  digitalWrite(traymotorrevpin,HIGH);
  delay(1000);
  Serial.println("stat*tray motor inch stop");
  digitalWrite(traymotorfwdpin,LOW);
  digitalWrite(traymotorrevpin,LOW);
}
void rowmotormoveforward()
{
  Serial.println("stat*row motor mov fwd");
  digitalWrite(rowmotorfwdpin,HIGH);
  digitalWrite(rowmotorrevpin,LOW);
}
void rowmotorstop()
{
  Serial.println("stat*row motor stop");
  digitalWrite(rowmotorfwdpin,LOW);
  digitalWrite(rowmotorrevpin,LOW);
}
void rowmotormovereverse()
{
  Serial.println("stat*row motor mov rev");
  digitalWrite(rowmotorfwdpin,LOW);
  digitalWrite(rowmotorrevpin,HIGH);
}
void colmotormoveforward()
{
  Serial.println("stat*column motor mov fwd");
  digitalWrite(colmotorfwdpin,HIGH);
  digitalWrite(colmotorrevpin,LOW);
}
void colmotorstop()
{
  Serial.println("stat*column motor stop");
  digitalWrite(colmotorfwdpin,LOW);
  digitalWrite(colmotorrevpin,LOW);
}
void colmotormovereverse()
{
  Serial.println("stat*column motor mov rev");
  digitalWrite(colmotorfwdpin,LOW);
  digitalWrite(colmotorrevpin,HIGH);
}
void traymotormoveforward()
{
  Serial.println("stat*tray motor mov fwd");
  digitalWrite(traymotorfwdpin,HIGH);
  digitalWrite(traymotorrevpin,LOW);
}
void traymotorstop()
{
  Serial.println("stat*tray motor mov stop");
  digitalWrite(traymotorfwdpin,LOW);
  digitalWrite(traymotorrevpin,LOW);
}
void traymotormovereverse()
{
  Serial.println("stat*tray motor mov rev");
  digitalWrite(traymotorfwdpin,LOW);
  digitalWrite(traymotorrevpin,HIGH);
}
boolean movetorow(int xval,int yval)
{
  boolean sequencecorrect=true;
  boolean operationcomplete=false;
  int destcell=senspinarray[xval][yval];
  int nextexpectedcell=senspinarray[0][yval];
  int prevcell=senspinarray[0][yval];
  int loopcount=0;
  while(sequencecorrect)
  {
    while(scanallsensors()==0)
    {
      rowmotormoveforward();
      //Serial.println("moverowfwd");
      delay(1000);
    }
    if((scanallsensors()!=nextexpectedcell && scanallsensors()!=prevcell)|| !digitalRead(originpin))
    {
      sequencecorrect=false;
      operationcomplete=false;
    }
    if(scanallsensors()!=nextexpectedcell && scanallsensors()==prevcell && digitalRead(originpin))
    {
      Serial.println("msg*row seq correct passing through");
      delay(1000);
    }
    if((scanallsensors()==nextexpectedcell) && (destcell!=nextexpectedcell) && digitalRead(originpin))
    {
      Serial.println("msg*row seq correct: "+String(loopcount));
      sequencecorrect=true;
      operationcomplete=false;
      loopcount++;
      prevcell=nextexpectedcell;
      nextexpectedcell=senspinarray[loopcount][yval];
    }
    if((scanallsensors()==nextexpectedcell) && (destcell==nextexpectedcell) && digitalRead(originpin))
    {
      sequencecorrect=false;
      operationcomplete=true;
    }
  }
  if(sequencecorrect==false && operationcomplete==false)
  {
    Serial.println("err*Wrong sequence");
    rowmotorstop();
    return false;
  }
  else if(sequencecorrect==false && operationcomplete==true)
  {
    Serial.println("msg*Moved to dest X");
    rowmotorstop();
    return true;
  }
}
boolean movetocol(int xval,int yval)
{
  boolean sequencecorrect=true;
  boolean operationcomplete=false;
  int destcell=senspinarray[0][yval];
  int nextexpectedcell=senspinarray[0][0];
  int prevcell=senspinarray[0][0];
  int loopcount=0;
  while(sequencecorrect)
  {
    while(scanallsensors()==0)
    {
    colmotormoveforward();
      if(!digitalRead(originpin))
      {
        Serial.println("msg*passing through origin");
      }
    //Serial.println("movecolfwd");
    delay(1000);
    }
    
    if((scanallsensors()!=nextexpectedcell && scanallsensors()!=prevcell) || !digitalRead(originpin))
    {
      sequencecorrect=false;
      operationcomplete=false;
    }
    if(scanallsensors()!=nextexpectedcell && scanallsensors()==prevcell && digitalRead(originpin))
    {
      Serial.println("msg*col seq correct passing through");
      delay(1000);
    }
    if((scanallsensors()==nextexpectedcell) && (destcell!=nextexpectedcell) && digitalRead(originpin))
    {
      Serial.println("msg*col seq correct: "+String(loopcount));
      sequencecorrect=true;
      operationcomplete=false;
      prevcell=nextexpectedcell;
      loopcount++;
      nextexpectedcell=senspinarray[0][loopcount];
    }
    if((scanallsensors()==nextexpectedcell) && (destcell==nextexpectedcell) && digitalRead(originpin))
    {
      sequencecorrect=false;
      operationcomplete=true;
    }
  }
  if(sequencecorrect==false && operationcomplete==false)
  {
    Serial.println("err*Wrong sequence");
    colmotorstop();
    return false;
  }
  else if(sequencecorrect==false && operationcomplete==true)
  {
    Serial.println("msg*Moved to dest Y");
    colmotorstop();
    return true;
  }
}
