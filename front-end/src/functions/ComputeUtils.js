export default {
    someFunc,
    computeElapsedMinimal,
    computeNodeCounts,
}


function someFunc(){
    console.log("some func")
}

function computeElapsedMinimal(elapsedData){
    let dataLength = elapsedData.length;
    let elapsedMinimal = {}
    for (let i=0;i<dataLength;i++){
        let key = elapsedData[i].eval_node_id;
        if (!(key in elapsedMinimal)){
            elapsedMinimal[key] = elapsedData[i].y2;
        }
        else{
            if (elapsedMinimal[key] > elapsedData[i].y2){
                elapsedMinimal[key] = elapsedData[i].y2
            }
        }
    }
    return elapsedMinimal;
}

function computeNodeCounts(){

}