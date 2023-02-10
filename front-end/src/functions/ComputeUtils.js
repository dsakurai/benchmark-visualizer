export default {
    computeElapsedMinimal,
    computeNodeCounts,
}


function computeElapsedMinimal(elapsedData, allIDs){
    let dataLength = elapsedData.length;
    let elapsedMinimal = {}
    allIDs.forEach(function(entry){
        elapsedMinimal[entry] = 0;
    });
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

function computeNodeCounts(filteredData, allIDs){
    let dateLength = filteredData.length;
    let nodeCounts = {};
    allIDs.forEach(function(entry){
        nodeCounts[entry] = 0;
    });
    for (let i = 0; i < dateLength; i++) {
        let key = filteredData[i].eval_node_id;
        if (!(key in nodeCounts)) {
            nodeCounts[key] = 1;
        } else {
            nodeCounts[filteredData[i].eval_node_id] += 1;
        }
    }
    return nodeCounts;
}