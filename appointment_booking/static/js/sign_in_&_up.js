

var sliding= (function slidingWrapper(){
    let left = true;
   
    function slidingFunc(){
        if(left){

            slideToRight();
            left= false;
        }else{
        
            slideToLeft();
            left= true;
        }
    }
    return slidingFunc;
})()

function hideAndShowElements(hideId, showId){
    $(hideId).css("opacity", 0);
    $(showId).css("opacity", 1);
}
function changeElementsLayer(...elements){
    for(element of elements){
        $(element.id).css("z-index", element.layer);
    }
}
function translateElementsToRight(...elementIds){
    for(id of elementIds){
        $(id).css("transform", "translateX(100%)");
    }
}
function translateElementsToLeft(...elementIds){
    for(id of elementIds){
        $(id).css("transform", "translateX(0%)");
    }
}
function slideToRight(){
    
    translateElementsToRight("#slider-box");
    translateElementsToLeft("#sign-in-box", "#sign-up-box");
    changeElementsLayer({id: "#sign-in-box", layer: 1}, 
                        {id: "#sign-up-box", layer: 0},
                        {id: "#sign-up-text-box", layer: 3},
                        {id: "#sign-in-text-box", layer: -1})
    hideAndShowElements("#sign-in-text-box", "#sign-up-text-box");
    $("#switch-btn").text("Sign up"); 
}

function slideToLeft(){
    
    translateElementsToLeft("#slider-box");
    translateElementsToRight("#sign-in-box", "#sign-up-box");
    changeElementsLayer({id: "#sign-in-box", layer: 0}, 
                        {id: "#sign-up-box", layer: 1},
                        {id: "#sign-in-text-box", layer: 3},
                        {id: "#sign-up-text-box", layer: -1})
    hideAndShowElements("#sign-up-text-box", "#sign-in-text-box"); 
    $("#switch-btn").text("Sign in"); 
}