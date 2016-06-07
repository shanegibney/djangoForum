float freq, y1;
float dt, dx = 1.0;
float lTime = 0.0, cTime = 0.0;
int radius = 1, A = 50;
float x, y;
int w = 50, h = 30;
boolean bStop;
void setup() {
  size(750, 400);
  frameRate = 60;
  x = width - 100;
  y = height - 100;
  fill(0);
  stroke(0);
  smooth();
}
void draw() {
  background(#F79D57);
  fill(#DDDDDD);
  rect(width - 100 + w/2 - 2, 100, 4, height - 200);
  line(50, height/2, width - 50, height/2);
  fill(0);
  cTime = millis();
  dt = (cTime - lTime)/1000;//dt = 1/60;
  lTime = cTime;
  for (int i = 0; i < 500; i++) {
    stroke(255, 0, 0);
    fill(255, 0, 0);
    y1 = A*sin(TWO_PI*freq*cTime/1000 + i*TWO_PI*freq*dt);
    ellipse(i*dx + 50, y1 + height/2, radius, radius);
  }
  if ((mouseX > x) && (mouseX < x + w) && (mouseY > y) && (mouseY < y + h)) {
    if (mousePressed) {
      ellipse(100, 100, 5, 5);
      y = mouseY - h/2;
      freq = map(mouseY, 100, height - 100, 0.0000, 0.0610);
    }
  }
  fill(#BBBBBB);
  rect(x, y, w, h);
  println("freq = ", freq);
  /*fill(0);
   textSize(20);
   text("frequency = ", 50, 50);
   text(freq, 170, 50);
   println("cTime = ", cTime/1000);
   println("freq = ", freq);
   println("dx = ", dx);
   println("dt = ", dt);
   println("velx = ", dx/dt);
   println("wavelength = ", dx/(dt*freq));//lambda=velx/freq
   */
}
void keyPressed()
{
  bStop = !bStop;
  if (bStop)
    noLoop();
  else
    loop();
} 

