$(document).ready(function(){    
    $(window).resize(function(){
        redraw();
    });
});

function redraw(){
    var processingInstance = Processing.getInstanceById('flocking');
    var winWidth = window.innerWidth;
    var tempHeight;
    var tempWidth;

    if(winWidth > 900) {
        tempHeight = 600;
        tempWidth = 800;
    } else if(winWidth > 550) {
        tempHeight = 368;
        tempWidth = 480;
    } else {
        tempHeight = 184;
        tempWidth = 240;
    }

    if(tempWidth != processingInstance.WIDTH) {
        processingInstance.HEIGHT = tempHeight;
        processingInstance.WIDTH = tempWidth;

        var ctx = document.getElementById('flocking').getContext('2d');
        ctx.canvas.height = tempHeight;
        ctx.canvas.width = tempWidth;

        processingInstance.setup();
    }

}