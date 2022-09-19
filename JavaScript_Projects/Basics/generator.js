function* geometricSequence(){
    var member = 1;
    while(true){
        yield member *= 2;
    }
}

var generator = geometricSequence();

for(let i = 0; i <=5; i++){
    console.log(generator.next().value);
}