void setup() {
    size(400, 400);
    background(125);
    fill(255);

    noLoop();
    PFont fontA = loadFont("courier");
    textFont(fontA, 14);  
}

void draw() {  
    text("Hello, World!", 20, 20);
}
