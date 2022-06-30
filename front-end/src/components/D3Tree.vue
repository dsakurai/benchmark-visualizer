<template>
    <el-container>
        <el-header>
            <el-card>
                -> TODO: Control properties here
            </el-card>
        </el-header>
        <el-main>
            <svg id="d3tree"></svg>
        </el-main>
    </el-container>
</template>

<script>
import axios from 'axios';
import * as d3 from 'd3';

export default {
    name: "D3Tree",
    data() {
        return {
            treeData: {
                'name': 'Top Level'
                // 'children': [
                //   {
                //     'name': 'Level 2: A',
                //     'children': [
                //       { 'name': 'Son of A' },
                //       { 'name': 'Daughter of A' }
                //     ]
                //   },
                //   { 'name': 'Level 2: B' }
                // ]
            },
            svg: '',
            responseData:'',
            duration: null,
            i: null,
            treemap: null,
            root:'',
            currentNode: {
                id: null,
                data: { name: '' }
            },
            newNode: {
                id: 0,
                name: ''
            },
            nodeObj: null
        };
    },
    created() {
        this.getDemoTree();
    },
    methods: {
        getDemoTree() {
            axios.get("/api/get_demo_problem/").then(response => {
                this.responseData = response.data;
                this.drawGraph();
            });
        },
        drawGraph() {
            let margin = {top: -200, right: 90, bottom: 30, left: 90}
            let width = 960 - margin.left - margin.right
            let height = 500 - margin.top - margin.bottom
            this.svg = d3.select("#d3tree").attr('viewBox', [-10, -10, width, height]).append('g').attr('transform', 'translate(' +
                margin.left + ',' + margin.top + ')')
            this.nodeObj = d3.hierarchy.prototype.constructor
            this.i = 0
            // this.root = null
            this.duration = 750
            // declares a tree layout and assigns the size
            this.treemap = d3.tree().size([height, width])
            // Assigns parent, children, height, depth
            this.root = d3.hierarchy(this.treeData, function (d) { return d.children })
            this.root.x0 = height / 2
            this.root.y0 = 0
            // Collapse after the second level
            // root.children.forEach(collapse)

            // ****************  zoom ************************
            // add zoom capabilities
            let zoomHandler = d3.zoom()
                .on('zoom', zoomActions)
                .scaleExtent([1 / 2, 8])

            this.svg.call(zoomHandler).on('dblclick.zoom', null)
            zoomHandler(this.svg)

            // Zoom functions
            function zoomActions () {
                // gNode.attr('transform', d3.event.transform)
                // gLink.attr('transform', d3.event.transform)
            }
            // ***********************************************

            this.update(this.root)
        },
        update (source) {
            // Assigns the x and y position for the nodes
            let treeMapData = this.treemap(this.root)

            // Compute the new tree layout.
            this.nodes = treeMapData.descendants()
            this.links = treeMapData.descendants().slice(1)

            // Normalize for fixed-depth.
            this.nodes.forEach(function (d) { d.y = d.depth * 180 })

            // ****************** Nodes section ***************************

            // Update the nodes...
            let node = this.svg.selectAll('g.node')
                .data(this.nodes, function (d) { return d.id || (d.id = ++this.i) })

            // Enter any new modes at the parent's previous position.
            let nodeEnter = node.enter().append('g')
                .attr('class', 'node')
                .attr('transform', function () {
                    return 'translate(' + source.y0 + ',' + source.x0 + ')'
                })
                .on('click', this.click)

            // Add Circle for the nodes
            nodeEnter.append('circle')
                .attr('class', 'node')
                .attr('r', 1e-6)
                .style('fill', function (d) {
                    return d._children ? 'lightsteelblue' : '#000'
                })

            // Add labels for the nodes
            nodeEnter.append('text')
                .attr('dy', '.35em')
                .attr('x', function (d) {
                    return d.children || d._children ? -13 : 13
                })
                .attr('text-anchor', function (d) {
                    return d.children || d._children ? 'end' : 'start'
                })
                .text(function (d) { return d.data.name })

            // UPDATE
            let nodeUpdate = nodeEnter.merge(node)

            // update the text
            node.select('text')
                .attr('dy', '.35em')
                .attr('x', function (d) {
                    return d.children || d._children ? -13 : 13
                })
                .attr('text-anchor', function (d) {
                    return d.children || d._children ? 'end' : 'start'
                })
                .text(function (d) { return d.data.name })

            // Transition to the proper position for the node
            nodeUpdate.transition()
                .duration(this.duration)
                .attr('transform', function (d) {
                    return 'translate(' + d.y + ',' + d.x + ')'
                })

            // Update the node attributes and style
            nodeUpdate.select('circle.node')
                .attr('r', 10)
                .style('fill', function (d) {
                    return d._children ? 'lightsteelblue' : 'steelblue'
                })
                .attr('cursor', 'pointer')

            // Remove any exiting nodes
            let nodeExit = node.exit().transition()
                .duration(this.duration)
                .attr('transform', function () {
                    return 'translate(' + source.y + ',' + source.x + ')'
                })
                .remove()

            // On exit reduce the node circles size to 0
            nodeExit.select('circle')
                .attr('r', 1e-6)

            // On exit reduce the opacity of text labels
            nodeExit.select('text')
                .style('fill-opacity', 1e-6)

            // ****************** links section ***************************

            // Update the links...
            let link = this.svg.selectAll('path.link')
                .data(this.links, function (d) { return d.id })

            // Enter any new links at the parent's previous position.
            let linkEnter = link.enter().insert('path', 'g')
                .attr('class', 'link')
                .attr('d', function () {
                    let o = { x: source.x0, y: source.y0 }
                    return diagonal(o, o)
                })

            // UPDATE
            let linkUpdate = linkEnter.merge(link)

            // Transition back to the parent element position
            linkUpdate.transition()
                .duration(this.duration)
                .attr('d', function (d) { return diagonal(d, d.parent) })

            // Remove any exiting links
            link.exit().transition()
                .duration(this.duration)
                .attr('d', function () {
                    let o = { x: source.x, y: source.y }
                    return diagonal(o, o)
                })
                .remove()

            // Store the old positions for transition.
            this.nodes.forEach(function (d) {
                d.x0 = d.x
                d.y0 = d.y
            })

            // Creates a curved (diagonal) path from parent to the child nodes
            function diagonal (s, d) {
                let path = `M ${s.y} ${s.x}
            C ${(s.y + d.y) / 2} ${s.x},
              ${(s.y + d.y) / 2} ${d.x},
              ${d.y} ${d.x}`
                return path
            }
        },
        // Toggle children on click.
        click (d) {
            this.currentNode = d
            if (d.children) {
                d._children = d.children
                d.children = null
            } else {
                d.children = d._children
                d._children = null
            }
            this.update(d)
        }
    },
}
</script>

<style scoped>
#d3tree circle {
    fill: #fff;
    stroke: steelblue;
    stroke-width: 3px;
}

#d3tree .node text {
    font: 12px sans-serif;
}

#d3tree .link {
    fill: none;
    stroke: #ccc;
    stroke-width: 2px;
}
</style>