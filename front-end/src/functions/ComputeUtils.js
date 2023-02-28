export default {
    computeElapsedMinimal,
    computeNodeCounts,
    rotateValues,
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
            elapsedMinimal[key] = elapsedData[i].y_org;
        }
        else{
            if (elapsedMinimal[key] > elapsedData[i].y_org){
                elapsedMinimal[key] = elapsedData[i].y_org
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

function rotateValues(x,y){
    let radians = (Math.PI / 180) * 45,
        cos = Math.cos(radians),
        sin = Math.sin(radians),
        nx = (cos * (x)) + (sin * (y)),
        ny = (cos * (y)) - (sin * (x));
    return [nx, ny];
}