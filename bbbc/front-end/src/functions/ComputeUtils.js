export default {
    computeElapsedMinimal,
    computeNodeCounts,
    rotateValues,
    getLocatedMinima,
    computeStepMinimal,
}

function computeStepMinimal(solverData, allIDs) {
    /** Compute Best value for each node upon receiving solver execution data
     * solverData: solver execution data
     * allIDs: id of all the nodes
     * return: dict of array with the best minimal at each step and node id as key
     */
    let dataLength = solverData.length;
    let elapsedMinimal = {}
    allIDs.forEach(function(entry){
        elapsedMinimal[entry] = new Array(dataLength).fill(0.0);
    });
    // Corner case
    elapsedMinimal[solverData[0].eval_node_id][0] = solverData[0].y_org;
    for (let i=1;i<dataLength;i++){
        let currentNodeId = solverData[i].eval_node_id;
        let currentValue = solverData[i].y_org;
        allIDs.forEach(function(nodeId){
            elapsedMinimal[nodeId][i] = elapsedMinimal[nodeId][i-1];
            if (nodeId === currentNodeId){
                if (elapsedMinimal[nodeId][i] > currentValue){
                    elapsedMinimal[nodeId][i] = currentValue;
                }
            }
        });
    }
    return elapsedMinimal;
}

function getLocatedMinima(stepMinimals, endStep, allIDs){
    let locatedMinima = {};
    allIDs.forEach(function(nodeId){
        locatedMinima[nodeId] = stepMinimals[nodeId][endStep];
    });
    return locatedMinima;
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
