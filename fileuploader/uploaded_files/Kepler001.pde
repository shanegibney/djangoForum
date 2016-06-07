PVector p, v, v0, a, f, r;
float radius = 5.0;
float C = 0.045, m;
void setup() {
  size(600, 600);
  smooth();
  r = new PVector(0.0, 0.0);
  f = new PVector(width/2, height/2);
  p = new PVector(20.0, height-40);
  v = new PVector(2.7, -4.5);
  a = new PVector(0.0, 0.0);
}
void draw() {
  background(255, 255, 255);
  PVector r = PVector.sub(f, p);
  float m = r.mag();
  PVector a = new PVector(r.x, r.y, C/(pow(m, 2)));
  v.x += a.x;
  p.x += v.x;
  v.y += a.y;
  p.y += v.y;
  fill(0);
  ellipse(p.x, p.y, radius, radius);
}
boolean bStop;
void keyPressed()
{
  bStop = !bStop;
  if (bStop)
    noLoop();
  else
    loop();
} 

