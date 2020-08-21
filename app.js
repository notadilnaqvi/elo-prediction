$(document).ready(function(){

    async function loadModel(){
        const MODEL_URL = 'tfjsModel/model.json';
        const model = await tf.loadGraphModel(MODEL_URL);
        console.log("Model loaded!");
        $("button").click(() => {
            $whiteElo = parseInt($("#whiteElo").val());
            $blackElo = parseInt($("#blackElo").val());
            $result = $("input[type='radio']:checked").val();
            
            if ($result == "win") { $result = 1;} 
            else if ($result == "draw") { $result = 0.5;} 
            else {$result = 0;}

            $eloChange = model.predict(tf.tensor([[$whiteElo, $blackElo, $result]]));

            if(isNaN($eloChange.dataSync()[0])){
                $("#eloChange").removeClass().addClass("alert alert-danger").text("Invalid input!")
            } else {
                $("#eloChange").removeClass().addClass("alert alert-primary").text(($eloChange.dataSync()[0] + $whiteElo).toFixed(1));
            }
        })
    }
    loadModel();
})


// ERROR Uncaught (in promise) ReferenceError: loadGraphModel is not defined
// Solved by changing loadGraphModel() to tf.loadGraphModel()