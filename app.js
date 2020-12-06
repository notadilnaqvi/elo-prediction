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

            $predictedEloChange = model.predict(tf.tensor([[$whiteElo, $blackElo, $result]]));
            $expW = 1 / (1 + 10**(($blackElo - $whiteElo) / 400));
            $actualEloChange = 10*($result - $expW);

            if(isNaN($predictedEloChange.dataSync()[0])){
                $("#eloChange").removeClass().addClass("alert alert-danger").text("Invalid input!");
                $("#actualEloChange").removeClass().addClass("alert alert-danger").text("Invalid input!")
            } else {
                $("#eloChange").removeClass().addClass("alert alert-primary").text(`Predicted Elo: ${($predictedEloChange.dataSync()[0] + $whiteElo).toFixed(1)}`);
                $("#actualEloChange").removeClass().addClass("alert alert-success").text(`Ground truth: ${($actualEloChange + $whiteElo).toFixed(1)}`);
            }
        })
    }
    loadModel();
})


// ERROR Uncaught (in promise) ReferenceError: loadGraphModel is not defined
// Solved by changing loadGraphModel() to tf.loadGraphModel()