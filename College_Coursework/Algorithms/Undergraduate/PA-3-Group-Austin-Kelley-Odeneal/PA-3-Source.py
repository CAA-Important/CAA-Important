import pydot
from PIL import Image, ImageTk
import tkinter as tk
import copy
import os

class Graph:
    def __init__(self, gui):
        # Initialize variables for the class
        self.graph = pydot.Dot(graph_type='graph')
        self.adjacencyList = {}
        self.toDisplay = "AL"
        self.graphImage = ""
        self.dfsTime = 0

        # Setup the gui and its parts
        self.gui = gui
        self.frame = tk.Frame(self.gui)

        # Setup text display and scrollbars
        self.scrollVert = tk.Scrollbar(self.frame)
        (self.scrollVert).pack(side=tk.RIGHT, fill=tk.Y)

        self.scrollHoriz = tk.Scrollbar(self.frame, orient=tk.HORIZONTAL)
        (self.scrollHoriz).pack(side=tk.BOTTOM, fill=tk.X)

        self.display = tk.Text(self.frame, yscrollcommand=(self.scrollVert).set, xscrollcommand=(self.scrollHoriz).set,
                               wrap=tk.NONE)
        (self.scrollVert).configure(command=(self.display).yview)
        (self.scrollHoriz).configure(command=(self.display).xview)
        (self.display).pack()

        # Setup gui elements for node adding and removing in graph
        self.nodeFrame = tk.Frame(self.gui)
        self.nodeFrame1 = tk.Frame(self.gui)
        self.nodeFrame2 = tk.Frame(self.gui)
        self.nodeLabel = tk.Label(self.nodeFrame, text="Enter your node in the box below")
        self.nodeEntry = tk.Entry(self.nodeFrame)
        self.nodeButton = tk.Button(self.nodeFrame1, text="Add Node",
                                    command=lambda: self.AddNode((self.nodeEntry).get()))
        self.nodeRmvButton = tk.Button(self.nodeFrame1, text="Remove Node",
                                       command=lambda: self.RemoveNode((self.nodeEntry).get()))
        self.nodeErrorLabel = tk.Label(self.nodeFrame2, text="")
        (self.nodeLabel).pack()
        (self.nodeEntry).pack()
        (self.nodeButton).pack(side=tk.LEFT)
        (self.nodeRmvButton).pack()
        (self.nodeErrorLabel).pack()

        # Setup gui elements for edge adding and removing in graph
        self.edgeFrame1 = tk.Frame(self.gui)
        self.edgeFrame2 = tk.Frame(self.gui)
        self.edgeFrame3 = tk.Frame(self.gui)
        self.edgeFrame4 = tk.Frame(self.gui)
        self.edgeLabel = tk.Label(self.edgeFrame1,
                                  text="Enter your source node in the left box and sink node in the right.\nNodes will be added to the graph if they are not in it already.")
        self.edgeEntry1 = tk.Entry(self.edgeFrame2)
        self.edgeEntry2 = tk.Entry(self.edgeFrame2)
        self.edgeButton = tk.Button(self.edgeFrame3, text="Add Edge",
                                    command=lambda: self.AddEdge((self.edgeEntry1).get(), (self.edgeEntry2).get()))
        self.edgeRmvButton = tk.Button(self.edgeFrame3, text="Remove Edge",
                                       command=lambda: self.RemoveEdge((self.edgeEntry1).get(),
                                                                       (self.edgeEntry2).get()))
        self.edgeErrorLabel = tk.Label(self.edgeFrame4, text="")
        (self.edgeLabel).pack()
        (self.edgeEntry1).pack(side=tk.LEFT)
        (self.edgeEntry2).pack()
        (self.edgeButton).pack(side=tk.LEFT)
        (self.edgeRmvButton).pack()
        (self.edgeErrorLabel).pack()

        # Setup gui elements for displaying graph information and traversals
        self.displayFrame = tk.Frame(self.gui)
        self.displayAdjacent = tk.Button(self.displayFrame, text="Display Adjacency List",
                                         command=self.DisplayAdjacencyList)
        self.displayAdjacentMat = tk.Button(self.displayFrame, text="Display Adjacency Matrix",
                                            command=self.DisplayAdjacencyMatrix)
        self.displayGraph = tk.Button(self.displayFrame, text="Display Graph", command=self.DisplayGraph)
        self.displayBFS = tk.Button(self.displayFrame, text="Breadth First Search", command=self.BFS)
        self.displayDFS = tk.Button(self.displayFrame, text="Depth First Search", command=self.DFS)
        (self.displayAdjacent).pack(side=tk.LEFT)
        (self.displayAdjacentMat).pack(side=tk.LEFT)
        (self.displayGraph).pack(side=tk.LEFT)
        (self.displayBFS).pack(side=tk.LEFT)
        (self.displayDFS).pack(side=tk.LEFT)

        # Place all of the pieces of the gui on the gui and display them
        (self.frame).place(x=163, y=50)
        (self.nodeFrame).place(x=200, y=475)
        (self.nodeFrame1).place(x=220, y=518)
        (self.nodeFrame2).place(x=200, y=538)
        (self.edgeFrame1).place(x=500, y=475)
        (self.edgeFrame2).place(x=540, y=515)
        (self.edgeFrame3).place(x=603, y=535)
        (self.edgeFrame4).place(x=540, y=555)
        (self.displayFrame).place(x=200, y=650)

    def AddNode(self, node):
        # Adds a new node to the graph
        if (node == ''):
            (self.nodeErrorLabel)['text'] = "Error: Node must have a value."

        elif (self.adjacencyList).has_key(node):
            (self.nodeErrorLabel)['text'] = "Error: Node already exists."

        else:
            (self.nodeErrorLabel)['text'] = ""
            (self.adjacencyList)[node] = []
            (self.graph).add_node(pydot.Node(node))
            self.Display()

    def AddEdge(self, sourceNode, sinkNode):
        # Adds a new edge to the graph.  If either of the nodes is not already in the graph, it is added
        if (sourceNode == '' or sinkNode == ''):
            (self.edgeErrorLabel)['text'] = "Error: The source and sink nodes must have values."
        else:
            (self.edgeErrorLabel)['text'] = ""
            if (not (self.adjacencyList).has_key(sourceNode)):
                (self.adjacencyList)[sourceNode] = []
            if (not (self.adjacencyList).has_key(sinkNode)):
                (self.adjacencyList)[sinkNode] = []
            (self.adjacencyList)[sourceNode].append(sinkNode)
            if(sinkNode != sourceNode):
                (self.adjacencyList)[sinkNode].append(sourceNode)
            (self.graph).add_edge(pydot.Edge(sourceNode, sinkNode))
            self.Display()

    def RemoveEdge(self, sourceNode, sinkNode):
        # Removes an edge from the graph.
        if (sourceNode == '' or sinkNode == ''):
            (self.edgeErrorLabel)['text'] = "Error: The source and sink nodes must have values."
        elif (not (sourceNode in (self.adjacencyList).keys())) or (not (sinkNode in (self.adjacencyList).keys())):
            (self.edgeErrorLabel)['text'] = "Error: At least one of those nodes does not exist in the graph."
        else:
            if (sinkNode in (self.adjacencyList)[sourceNode]):
                (self.edgeErrorLabel)['text'] = ""
                ((self.adjacencyList)[sourceNode]).remove(sinkNode)
                if(sinkNode != sourceNode):
                    ((self.adjacencyList)[sinkNode]).remove(sourceNode)
                self.ConstructGraph()
            else:
                (self.edgeErrorLabel)['text'] = "Edge does not exist in graph."

    def RemoveNode(self, node):
        # Removes a node from the graph
        if (node == ""):
            (self.nodeErrorLabel)['text'] = "Error: Node must have a value."
        elif (not (node in (self.adjacencyList).keys())):
            (self.nodeErrorLabel)['text'] = "Error: Node does not exist in graph."
        else:
            (self.nodeErrorLabel)['text'] = ""
            otherNodes = (self.adjacencyList).keys()
            otherNodes.sort()
            for otherNode in otherNodes:
                while (node in (self.adjacencyList)[otherNode]):
                    ((self.adjacencyList)[otherNode]).remove(node)
            (self.adjacencyList).pop(node, None)
            self.ConstructGraph()

    def ConstructGraph(self):
        # Puts a graph together using the adjacency list
        (self.graph) = pydot.Dot(graph_type="graph")
        nodes = copy.deepcopy((self.adjacencyList).keys())
        nodes.sort()
        nodeCount = 0
        for source in nodes:
            (self.graph).add_node(pydot.Node(source))
            for sink in (self.adjacencyList)[source]:
                if(sink in nodes):
                    (self.graph).add_edge(pydot.Edge(source, sink))
            nodes[nodeCount] = ''
            nodeCount += 1
        self.Display()

    def DisplayAdjacencyList(self):
        # Displays the adjacency list
        self.toDisplay = "AL"
        (self.display).delete(1.0, tk.END)
        (self.display).insert(tk.INSERT, "Adjacency List:\n\n")
        nodes = (self.adjacencyList).keys()
        nodes.sort()
        # For every node in the graph, create and display the string containing its adjacent nodes
        for sourceNode in nodes:
            toDisplay = sourceNode + "|   |--->"
            ((self.adjacencyList)[sourceNode]).sort()
            for sinkNode in (self.adjacencyList)[sourceNode]:
                toDisplay = toDisplay + "| " + sinkNode + " |   |--->"
            toDisplay = toDisplay[:(len(toDisplay) - 4)]
            toDisplay = list(toDisplay)
            toDisplay[-3] = "\\"
            toDisplay = "".join(toDisplay)
            toDisplay = toDisplay + "\n"
            (self.display).insert(tk.INSERT, toDisplay)

    def DisplayAdjacencyMatrix(self):
        # Constructs and displays the adjacency matrix using the adjacency list
        self.toDisplay = "AM"
        (self.display).delete(1.0, tk.END)
        (self.display).insert(tk.INSERT, "Adjacency Matrix:\n\n")
        adjacencyMatrix = {}
        adjacencyMatrixRow = {}
        nodes = (self.adjacencyList).keys()
        nodes.sort()
        # Initializes the rows of the adjacency matrix
        for i in nodes:
            adjacencyMatrixRow[i] = 0
        for j in nodes:
            adjacencyMatrix[j] = copy.deepcopy(adjacencyMatrixRow)

        # Fill adjacency matrix with proper values and display it row by row
        for k in nodes:
            for l in (self.adjacencyList)[k]:
                (adjacencyMatrix[k])[l] += 1
        displayString = "\t"
        for node in nodes:
            displayString = displayString + node + "\t"
        displayString = displayString + "\n"
        (self.display).insert(tk.INSERT, displayString)
        for nodeAM in nodes:
            displayString = nodeAM + "\t"
            rowNodes = (adjacencyMatrix[nodeAM]).keys()
            rowNodes.sort()
            for nodeAMRow in rowNodes:
                displayString = displayString + str((adjacencyMatrix[nodeAM])[nodeAMRow]) + "\t"
            displayString = displayString + "\n"
            (self.display).insert(tk.INSERT, displayString)

    def Display(self):
        # General display
        if (self.toDisplay == "AL"):
            self.DisplayAdjacencyList()
        elif (self.toDisplay == "AM"):
            self.DisplayAdjacencyMatrix()

    def DisplayGraph(self):
        # Opens a new window with the picture of the graph in it
        Dir = "SavedGraphs\\"
        if not os.path.exists(os.path.dirname(Dir)):
            os.makedirs(Dir)
        # Save graph as image to open
        (self.graph).write_png(Dir + "temp.png")
        graphWindow = tk.Toplevel(self.gui)

        # Open image
        graphImage = Image.open(Dir + "temp.png")
        graphImage = ImageTk.PhotoImage(graphImage)
        self.graphImage = graphImage

        # Setup scrollbars and canvas
        graphScrollVert = tk.Scrollbar(graphWindow)
        graphScrollVert.pack(side=tk.RIGHT, fill=tk.Y)

        graphScrollHoriz = tk.Scrollbar(graphWindow, orient=tk.HORIZONTAL)
        graphScrollHoriz.pack(side=tk.BOTTOM, fill=tk.X)

        graphCanvas = tk.Canvas(graphWindow, height=700, width=300, yscrollcommand=graphScrollVert.set,
                                xscrollcommand=graphScrollHoriz.set)
        # Use canvas to display the graph image
        graphCanvas.create_image(0, 0, image=(self.graphImage), anchor=tk.NW)
        graphCanvas.configure(scrollregion=graphCanvas.bbox("all"))
        graphScrollVert.configure(command=graphCanvas.yview)
        graphScrollHoriz.configure(command=graphCanvas.xview)
        graphCanvas.pack()

    def BFS(self):
        # Performs Breadth First Search of a graph
        visitOrders = []
        nodeQueue = []
        nodeColors = {}
        nodes = (self.adjacencyList).keys()
        nodes.sort()
        found = False

        # Initialize node color and predecessor
        for node in nodes:
            nodeColors[node] = ["white", ""]

        for checkNode in nodes:
            newVisitList = []
            # Check if a node needs to be visited
            if (nodeColors[checkNode])[0] == "white":
                nodeQueue.append(checkNode)
                (nodeColors[checkNode])[0] = "gray"
                (nodeColors[checkNode])[1] = 0
                newVisitList.append(checkNode)

            # Check if adjacent nodes need to be visited
            while (len(nodeQueue) != 0):
                currentNode = nodeQueue[0]
                nodeQueue.remove(currentNode)
                for adjacent in (self.adjacencyList)[currentNode]:
                    if (nodeColors[adjacent])[0] == "white":
                        (nodeColors[adjacent])[0] = "gray"
                        (nodeColors[adjacent])[1] = currentNode
                        nodeQueue.append(adjacent)
                        newVisitList.append(adjacent)
                    elif (nodeColors[adjacent])[1] == "":
                        (nodeColors[adjacent])[1] = currentNode

                (nodeColors[currentNode])[0] = "black"

            # See if new nodes were visited in this loop.  If so, see if parts of their components have already been put in a list
            if newVisitList != []:
                found = False
                for component in visitOrders:
                    for adjacent in (self.adjacencyList)[newVisitList[0]]:
                        if adjacent in component:
                            found = True
                            for item in newVisitList:
                                component.append(item)
                            break
                    if (found):
                        break
                if (not found):
                    visitOrders.append(newVisitList)

        # Display components using order of visited nodes
        (self.display).delete(1.0, tk.END)
        (self.display).insert(tk.INSERT, "BFS Results:\n\n")
        for components in visitOrders:
            (self.display).insert(tk.INSERT, "\tComponent " + components[0] + " visit order:\n")
            displayString = "\t\t"
            for node in components:
                displayString = displayString + node + " "
            displayString = displayString + "\n\n"
            (self.display).insert(tk.INSERT, displayString)

    def DFS(self):
        # Performs Depth First Search
        visitOrders = []
        toAppend = []
        nodeColors = {}
        (self.dfsTime) = 0
        nodes = (self.adjacencyList).keys()
        nodes.sort()
        found = False

        # Define Depth First Search visit for recursion
        def DFSVisit(theNode):
            toAppend.append(theNode)
            (nodeColors[theNode])[0] = "gray"
            (nodeColors[theNode])[2] = self.dfsTime
            self.dfsTime += 1
            for adjacent in (self.adjacencyList)[theNode]:
                if (nodeColors[adjacent])[0] == "white":
                    (nodeColors[adjacent])[1] = theNode
                    DFSVisit(adjacent)
                elif (nodeColors[adjacent])[1] == "":
                    (nodeColors[adjacent])[1] = theNode
            (nodeColors[theNode])[0] = "gray"
            (nodeColors[theNode])[2] = self.dfsTime
            self.dfsTime += 1

        # Initialize nodes with color, predecessor, first time, and last time
        for node in nodes:
            nodeColors[node] = ["white", "", 0, 0]
        # See if a node needs to be visited.  If so, find if its component has already been saved
        for checkNode in nodes:
            if (nodeColors[checkNode])[0] == "white":
                toAppend = []
                DFSVisit(checkNode)
                found = False
                for component in visitOrders:
                    for cnAdjacent in (self.adjacencyList)[checkNode]:
                        if cnAdjacent in component:
                            for connected in toAppend:
                                component.append(connected)
                            found = True
                            break
                    if (found):
                        break
                if (not found):
                    visitOrders.append(toAppend)

        # Display components
        (self.display).delete(1.0, tk.END)
        (self.display).insert(tk.INSERT, "DFS Results:\n\n")
        for component in visitOrders:
            (self.display).insert(tk.INSERT, "\tComponent " + component[0] + " visit order:\n")
            displayString = "\t\t"
            for item in component:
                displayString = displayString + item + " "
            displayString = displayString + "\n\n"
            (self.display).insert(tk.INSERT, displayString)

        return nodeColors


class DiGraph:
    def __init__(self, gui):
        #Initialize variables for the class
        self.graph = pydot.Dot(graph_type='digraph')
        self.adjacencyList = {}
        self.toDisplay = "AL"
        self.graphImage = ""
        self.dfsTime = 0

        #Setup the gui and its parts
        self.gui = gui
        self.frame = tk.Frame(self.gui)

        #Setup text display and scrollbars
        self.scrollVert = tk.Scrollbar(self.frame)
        (self.scrollVert).pack(side= tk.RIGHT, fill=tk.Y)

        self.scrollHoriz = tk.Scrollbar(self.frame, orient= tk.HORIZONTAL)
        (self.scrollHoriz).pack(side= tk.BOTTOM, fill=tk.X)

        self.display = tk.Text(self.frame, yscrollcommand= (self.scrollVert).set, xscrollcommand= (self.scrollHoriz).set, wrap=tk.NONE)
        (self.scrollVert).configure(command=(self.display).yview)
        (self.scrollHoriz).configure(command=(self.display).xview)
        (self.display).pack()

        #Setup gui elements for node adding and removing in graph
        self.nodeFrame = tk.Frame(self.gui)
        self.nodeFrame1 = tk.Frame(self.gui)
        self.nodeFrame2 = tk.Frame(self.gui)
        self.nodeLabel = tk.Label(self.nodeFrame, text="Enter your node in the box below")
        self.nodeEntry = tk.Entry(self.nodeFrame)
        self.nodeButton = tk.Button(self.nodeFrame1, text = "Add Node", command = lambda:self.AddNode((self.nodeEntry).get()))
        self.nodeRmvButton = tk.Button(self.nodeFrame1, text="Remove Node", command=lambda: self.RemoveNode((self.nodeEntry).get()))
        self.nodeErrorLabel = tk.Label(self.nodeFrame2, text="")
        (self.nodeLabel).pack()
        (self.nodeEntry).pack()
        (self.nodeButton).pack(side=tk.LEFT)
        (self.nodeRmvButton).pack()
        (self.nodeErrorLabel).pack()

        #Setup gui elements for edge adding and removing in graph
        self.edgeFrame1 = tk.Frame(self.gui)
        self.edgeFrame2 = tk.Frame(self.gui)
        self.edgeFrame3 = tk.Frame(self.gui)
        self.edgeFrame4 = tk.Frame(self.gui)
        self.edgeLabel = tk.Label(self.edgeFrame1, text="Enter your source node in the left box and sink node in the right.\nNodes will be added to the graph if they are not in it already.")
        self.edgeEntry1 = tk.Entry(self.edgeFrame2)
        self.edgeEntry2 = tk.Entry(self.edgeFrame2)
        self.edgeButton = tk.Button(self.edgeFrame3, text = "Add Edge", command = lambda:self.AddEdge((self.edgeEntry1).get(), (self.edgeEntry2).get()))
        self.edgeRmvButton = tk.Button(self.edgeFrame3, text="Remove Edge", command=lambda: self.RemoveEdge((self.edgeEntry1).get(), (self.edgeEntry2).get()))
        self.edgeErrorLabel = tk.Label(self.edgeFrame4, text="")
        (self.edgeLabel).pack()
        (self.edgeEntry1).pack(side=tk.LEFT)
        (self.edgeEntry2).pack()
        (self.edgeButton).pack(side=tk.LEFT)
        (self.edgeRmvButton).pack()
        (self.edgeErrorLabel).pack()

        #Setup gui elements for displaying graph information and traversals
        self.displayFrame = tk.Frame(self.gui)
        self.displayAdjacent = tk.Button(self.displayFrame, text= "Display Adjacency List", command=self.DisplayAdjacencyList)
        self.displayAdjacentMat = tk.Button(self.displayFrame, text= "Display Adjacency Matrix", command=self.DisplayAdjacencyMatrix)
        self.displayGraph = tk.Button(self.displayFrame, text= "Display Graph", command=self.DisplayGraph)
        self.displayBFS = tk.Button(self.displayFrame, text= "Breadth First Search", command=self.BFS)
        self.displayDFS = tk.Button(self.displayFrame, text="Depth First Search", command=self.DFS)
        (self.displayAdjacent).pack(side=tk.LEFT)
        (self.displayAdjacentMat).pack(side=tk.LEFT)
        (self.displayGraph).pack(side=tk.LEFT)
        (self.displayBFS).pack(side=tk.LEFT)
        (self.displayDFS).pack(side=tk.LEFT)

        #Place all of the pieces of the gui on the gui and display them
        (self.frame).place(x = 163, y = 50)
        (self.nodeFrame).place(x = 200, y=475)
        (self.nodeFrame1).place(x=220, y=518)
        (self.nodeFrame2).place(x=200, y=538)
        (self.edgeFrame1).place(x=500, y=475)
        (self.edgeFrame2).place(x=540, y=515)
        (self.edgeFrame3).place(x=603, y=535)
        (self.edgeFrame4).place(x=540, y=555)
        (self.displayFrame).place(x = 200, y = 650)

    def AddNode(self, node):
        #Adds a new node to the graph
        if(node == ''):
            (self.nodeErrorLabel)['text'] = "Error: Node must have a value."

        elif (self.adjacencyList).has_key(node):
            (self.nodeErrorLabel)['text'] = "Error: Node already exists."

        else:
            (self.nodeErrorLabel)['text'] = ""
            (self.adjacencyList)[node] = []
            (self.graph).add_node(pydot.Node(node))
            self.Display()

    def AddEdge(self, sourceNode, sinkNode):
        #Adds a new edge to the graph.  If either of the nodes is not already in the graph, it is added
        if(sourceNode == '' or sinkNode == ''):
            (self.edgeErrorLabel)['text'] = "Error: The source and sink nodes must have values."
        else:
            (self.edgeErrorLabel)['text'] = ""
            if(not (self.adjacencyList).has_key(sourceNode)):
                (self.adjacencyList)[sourceNode] = []
            if(not (self.adjacencyList).has_key(sinkNode)):
                (self.adjacencyList)[sinkNode] = []
            (self.adjacencyList)[sourceNode].append(sinkNode)
            (self.graph).add_edge(pydot.Edge(sourceNode, sinkNode))
            self.Display()

    def RemoveEdge(self, sourceNode, sinkNode):
        #Removes an edge from the graph.
        if(sourceNode == '' or sinkNode == ''):
            (self.edgeErrorLabel)['text'] = "Error: The source and sink nodes must have values."
        elif (not (sourceNode in (self.adjacencyList).keys())) or (not (sinkNode in (self.adjacencyList).keys())):
            (self.edgeErrorLabel)['text'] = "Error: At least one of those nodes does not exist in the graph."
        else:
            if(sinkNode in (self.adjacencyList)[sourceNode]):
                (self.edgeErrorLabel)['text'] = ""
                ((self.adjacencyList)[sourceNode]).remove(sinkNode)
                self.ConstructGraph()
            else:
                (self.edgeErrorLabel)['text'] = "Edge does not exist in graph."

    def RemoveNode(self, node):
        #Removes a node from the graph
        if(node == ""):
            (self.nodeErrorLabel)['text'] = "Error: Node must have a value."
        elif(not (node in (self.adjacencyList).keys())):
            (self.nodeErrorLabel)['text'] = "Error: Node does not exist in graph."
        else:
            (self.nodeErrorLabel)['text'] = ""
            otherNodes = (self.adjacencyList).keys()
            otherNodes.sort()
            for otherNode in otherNodes:
                while(node in (self.adjacencyList)[otherNode]):
                    ((self.adjacencyList)[otherNode]).remove(node)
            (self.adjacencyList).pop(node, None)
            self.ConstructGraph()

    def ConstructGraph(self):
        #Puts a graph together using the adjacency list
        (self.graph) = pydot.Dot(graph_type="digraph")
        nodes = copy.deepcopy((self.adjacencyList).keys())
        nodes.sort()
        for source in nodes:
            ((self.graph).add_node(pydot.Node(source)))
            for sink in (self.adjacencyList)[source]:
                (self.graph).add_edge(pydot.Edge(source, sink))
        self.Display()

    def DisplayAdjacencyList(self):
        #Displays the adjacency list
        self.toDisplay = "AL"
        (self.display).delete(1.0, tk.END)
        (self.display).insert(tk.INSERT, "Adjacency List:\n\n")
        nodes = (self.adjacencyList).keys()
        nodes.sort()
        #For every node in the graph, create and display the string containing its adjacent nodes
        for sourceNode in nodes:
            toDisplay = sourceNode + "|   |--->"
            ((self.adjacencyList)[sourceNode]).sort()
            for sinkNode in (self.adjacencyList)[sourceNode]:
                toDisplay = toDisplay + "| " + sinkNode + " |   |--->"
            toDisplay = toDisplay[:(len(toDisplay) - 4)]
            toDisplay = list(toDisplay)
            toDisplay[-3] = "\\"
            toDisplay = "".join(toDisplay)
            toDisplay = toDisplay + "\n"
            (self.display).insert(tk.INSERT, toDisplay)

    def DisplayAdjacencyMatrix(self):
        #Constructs and displays the adjacency matrix using the adjacency list
        self.toDisplay = "AM"
        (self.display).delete(1.0, tk.END)
        (self.display).insert(tk.INSERT, "Adjacency Matrix:\n\n")
        adjacencyMatrix = {}
        adjacencyMatrixRow = {}
        nodes = (self.adjacencyList).keys()
        nodes.sort()
        #Initializes the rows of the adjacency matrix
        for i in nodes:
            adjacencyMatrixRow[i] = 0
        for j in nodes:
            adjacencyMatrix[j] = copy.deepcopy(adjacencyMatrixRow)

        #Fill adjacency matrix with proper values and display it row by row
        for k in nodes:
            for l in (self.adjacencyList)[k]:
                (adjacencyMatrix[k])[l] += 1
        displayString = "\t"
        for node in nodes:
            displayString = displayString + node + "\t"
        displayString = displayString + "\n"
        (self.display).insert(tk.INSERT, displayString)
        for nodeAM in nodes:
            displayString = nodeAM + "\t"
            rowNodes = (adjacencyMatrix[nodeAM]).keys()
            rowNodes.sort()
            for nodeAMRow in rowNodes:
                displayString = displayString + str((adjacencyMatrix[nodeAM])[nodeAMRow]) + "\t"
            displayString = displayString + "\n"
            (self.display).insert(tk.INSERT, displayString)

    def Display(self):
        #General display
        if(self.toDisplay == "AL"):
            self.DisplayAdjacencyList()
        elif(self.toDisplay == "AM"):
            self.DisplayAdjacencyMatrix()

    def DisplayGraph(self):
        #Opens a new window with the picture of the graph in it
        Dir = "SavedGraphs\\"
        if not os.path.exists(os.path.dirname(Dir)):
            os.makedirs(Dir)
        #Save graph as image to open
        (self.graph).write_png(Dir + "temp.png")
        graphWindow = tk.Toplevel(self.gui)

        #Open image
        graphImage = Image.open(Dir + "temp.png")
        graphImage = ImageTk.PhotoImage(graphImage)
        self.graphImage = graphImage

        #Setup scrollbars and canvas
        graphScrollVert = tk.Scrollbar(graphWindow)
        graphScrollVert.pack(side= tk.RIGHT, fill=tk.Y)

        graphScrollHoriz = tk.Scrollbar(graphWindow, orient= tk.HORIZONTAL)
        graphScrollHoriz.pack(side= tk.BOTTOM, fill=tk.X)

        graphCanvas = tk.Canvas(graphWindow, height=700, width=300, yscrollcommand=graphScrollVert.set, xscrollcommand=graphScrollHoriz.set)
        #Use canvas to display the graph image
        graphCanvas.create_image(0,0,image=(self.graphImage), anchor=tk.NW)
        graphCanvas.configure(scrollregion=graphCanvas.bbox("all"))
        graphScrollVert.configure(command=graphCanvas.yview)
        graphScrollHoriz.configure(command=graphCanvas.xview)
        graphCanvas.pack()

    def BFS(self):
        #Performs Breadth First Search of a graph
        visitOrders = []
        nodeQueue = []
        nodeColors = {}
        nodes = (self.adjacencyList).keys()
        nodes.sort()
        found = False

        #Initialize node color and predecessor
        for node in nodes:
            nodeColors[node] = ["white", ""]

        for checkNode in nodes:
            newVisitList = []
            #Check if a node needs to be visited
            if (nodeColors[checkNode])[0] == "white":
                nodeQueue.append(checkNode)
                (nodeColors[checkNode])[0] = "gray"
                (nodeColors[checkNode])[1] = 0
                newVisitList.append(checkNode)

            #Check if adjacent nodes need to be visited
            while(len(nodeQueue) != 0):
                currentNode = nodeQueue[0]
                nodeQueue.remove(currentNode)
                for adjacent in (self.adjacencyList)[currentNode]:
                    if(nodeColors[adjacent])[0] == "white":
                        (nodeColors[adjacent])[0] = "gray"
                        (nodeColors[adjacent])[1] = currentNode
                        nodeQueue.append(adjacent)
                        newVisitList.append(adjacent)
                    elif(nodeColors[adjacent])[1] == "":
                        (nodeColors[adjacent])[1] = currentNode

                (nodeColors[currentNode])[0] = "black"

            #See if new nodes were visited in this loop.  If so, see if parts of their components have already been put in a list
            if newVisitList != []:
                found = False
                for component in visitOrders:
                    for adjacent in (self.adjacencyList)[newVisitList[0]]:
                        if adjacent in component:
                            found = True
                            for item in newVisitList:
                                component.append(item)
                            break
                    if(found):
                        break
                if(not found):
                    visitOrders.append(newVisitList)

        #Display components using order of visited nodes
        (self.display).delete(1.0, tk.END)
        (self.display).insert(tk.INSERT, "BFS Results:\n\n")
        for components in visitOrders:
            (self.display).insert(tk.INSERT, "\tComponent " + components[0] + " visit order:\n")
            displayString = "\t\t"
            for node in components:
                displayString = displayString + node + " "
            displayString = displayString + "\n\n"
            (self.display).insert(tk.INSERT, displayString)



    def DFS(self):
        #Performs Depth First Search
        visitOrders = []
        toAppend = []
        nodeColors = {}
        (self.dfsTime) = 0
        nodes = (self.adjacencyList).keys()
        nodes.sort()
        found = False

        #Define Depth First Search visit for recursion
        def DFSVisit(theNode):
            toAppend.append(theNode)
            (nodeColors[theNode])[0] = "gray"
            (nodeColors[theNode])[2] = self.dfsTime
            self.dfsTime += 1
            for adjacent in (self.adjacencyList)[theNode]:
                if(nodeColors[adjacent])[0] == "white":
                    (nodeColors[adjacent])[1] = theNode
                    DFSVisit(adjacent)
                elif(nodeColors[adjacent])[1] == "":
                    (nodeColors[adjacent])[1] = theNode
            (nodeColors[theNode])[0] = "gray"
            (nodeColors[theNode])[2] = self.dfsTime
            self.dfsTime += 1

        #Initialize nodes with color, predecessor, first time, and last time
        for node in nodes:
            nodeColors[node] = ["white", "", 0, 0]
        #See if a node needs to be visited.  If so, find if its component has already been saved
        for checkNode in nodes:
            if(nodeColors[checkNode])[0] == "white":
                toAppend = []
                DFSVisit(checkNode)
                found = False
                for component in visitOrders:
                    for cnAdjacent in (self.adjacencyList)[checkNode]:
                        if cnAdjacent in component:
                            for connected in toAppend:
                                component.append(connected)
                            found = True
                            break
                    if(found):
                        break
                if(not found):
                    visitOrders.append(toAppend)

        #Display components
        (self.display).delete(1.0, tk.END)
        (self.display).insert(tk.INSERT, "DFS Results:\n\n")
        for component in visitOrders:
            (self.display).insert(tk.INSERT, "\tComponent " + component[0] + " visit order:\n")
            displayString = "\t\t"
            for item in component:
                displayString = displayString + item + " "
            displayString = displayString + "\n\n"
            (self.display).insert(tk.INSERT, displayString)

        return nodeColors



def makeGraph(gui, button1, button2):
    button1.destroy()
    button2.destroy()
    graph=Graph(gui)
def makeDiGraph(gui, button1, button2):
    button1.destroy()
    button2.destroy()
    graph=DiGraph(gui)

#Begin program execution
theGui = tk.Tk()
graphButton = tk.Button(theGui, text="Undirected Graph", command=lambda:makeGraph(theGui, graphButton, diGraphButton))
diGraphButton = tk.Button(theGui, text="Directed Graph", command=lambda:makeDiGraph(theGui, graphButton, diGraphButton))
theGui.resizable(width=False, height=False)
theGui.geometry('{}x{}'.format(1000, 850))
graphButton.place(x=400, y=425)
diGraphButton.place(x=510, y=425)
theGui.mainloop()




