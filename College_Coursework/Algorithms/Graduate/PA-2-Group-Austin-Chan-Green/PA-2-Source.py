import os
os.environ['PATH'] = os.path.dirname(os.path.abspath(__file__)) + "\\Graphviz2.38\\bin;" + os.environ['PATH']
import tkinter
from tkinter import messagebox
import pydot_ng as pydot
from PIL import Image, ImageTk

class DirTree:

    def __init__(self):

        #Initialize variables
        self.adj_list = {}
        self.graph = pydot.Dot(graph_type='digraph')
        self.sccWindow = None
        self.gui = None
        self.image = None
        self.sccImage = None
        self.imageCanvas = None

    def run(self):
        #Put together pieces of the GUI
        self.gui = tkinter.Tk()

        canvasFrame = tkinter.Frame(self.gui, height=300, width=900)
        canvasFrame.grid(row=0, column=0)
        self.imageCanvas = tkinter.Canvas(canvasFrame, height=300, width=900, scrollregion=(0,-500,1200, 500))
        canvasXScroll = tkinter.Scrollbar(canvasFrame, orient=tkinter.HORIZONTAL)
        canvasYScroll = tkinter.Scrollbar(canvasFrame)
        canvasXScroll.config(command=self.imageCanvas.xview)
        canvasYScroll.config(command=self.imageCanvas.yview)
        self.imageCanvas.config(xscrollcommand=canvasXScroll.set, yscrollcommand=canvasYScroll.set)
        self.imageCanvas.yview_moveto(0.35)
        self.imageCanvas.xview_moveto(0.125)



        addNodeEntry = tkinter.Entry(self.gui, width=15)
        remNodeEntry = tkinter.Entry(self.gui, width=15)
        addEdgeSourceEntry = tkinter.Entry(self.gui, width=15)
        addEdgeSinkEntry = tkinter.Entry(self.gui, width=15)
        remEdgeSourceEntry = tkinter.Entry(self.gui, width=15)
        remEdgeSinkEntry = tkinter.Entry(self.gui, width=15)


        addNodeButton = tkinter.Button(self.gui, text="Add Node", height=2, width=15, command=lambda:self.addNode(addNodeEntry.get()))
        remNodeButton = tkinter.Button(self.gui, text="Remove Node", height=2, width=15,command=lambda: self.delNode(remNodeEntry.get()))
        addEdgeButton = tkinter.Button(self.gui, text="Add Edge", height=2, width=15,command=lambda: self.addEdge(addEdgeSourceEntry.get(), addEdgeSinkEntry.get()))
        remEdgeButton = tkinter.Button(self.gui, text="Remove Edge", height=2, width=15,command=lambda: self.delEdge(remEdgeSourceEntry.get(), remEdgeSinkEntry.get(), False))
        SCCButton = tkinter.Button(self.gui, text="SCC", height=2, width=15,command=lambda: self.SCC())
        quitButton = tkinter.Button(self.gui, text="Quit", height=2, width=15,command=self.gui.destroy)

        addNodeLabel = tkinter.Label(self.gui, text="Enter the name of a node in the box above")
        remNodeLabel = tkinter.Label(self.gui, text="Enter the name of a node in the box above")
        addEdgeLabel = tkinter.Label(self.gui, text="Enter the source node in the left box and sink node in the right")
        remEdgeLabel = tkinter.Label(self.gui, text="Enter the source node in the left box and sink node in the right")
        sccLabel = tkinter.Label(self.gui, text="Generate the strongly connected components\n of the graph")

        canvasFrame.pack()
        canvasXScroll.pack(side=tkinter.BOTTOM, fill=tkinter.X)
        canvasYScroll.pack(side=tkinter.RIGHT, fill=tkinter.Y)
        self.imageCanvas.pack(side=tkinter.LEFT, expand=True, fill=tkinter.BOTH)
        addNodeEntry.pack()
        remNodeEntry.pack()
        addEdgeSourceEntry.pack()
        addEdgeSinkEntry.pack()
        remEdgeSourceEntry.pack()
        remEdgeSinkEntry.pack()
        addNodeButton.pack()
        remNodeButton.pack()
        addEdgeButton.pack()
        remEdgeButton.pack()
        addNodeLabel.pack()
        remNodeLabel.pack()
        addEdgeLabel.pack()
        remEdgeLabel.pack()
        SCCButton.pack()
        sccLabel.pack()
        quitButton.pack()

        self.gui.geometry('{}x{}'.format(960, 600))
        canvasFrame.place(x=30, y=25)
        addNodeEntry.place(x=100, y=375)
        addNodeLabel.place(x=40, y=400)
        addNodeButton.place(x=90, y=425)
        remNodeEntry.place(x=100, y=500)
        remNodeLabel.place(x=40, y=525)
        remNodeButton.place(x=90, y=550)
        addEdgeSourceEntry.place(x=400, y=375)
        addEdgeSinkEntry.place(x=500, y=375)
        addEdgeLabel.place(x=340, y=400)
        addEdgeButton.place(x=440, y=425)
        remEdgeSourceEntry.place(x=400, y=500)
        remEdgeSinkEntry.place(x=500, y=500)
        remEdgeLabel.place(x=340, y=525)
        remEdgeButton.place(x=440, y=550)
        SCCButton.place(x=750, y=425)
        sccLabel.place(x=683, y=475)
        quitButton.place(x=830, y=555)

        #Start the gui
        self.gui.mainloop()

#Make sure all functions are working properly








    def addNode(self, newNode):
        #Check is node has a name
        if(newNode == ""):
            messagebox.showerror("Error", "Node entry box must not be empty.")

        elif not (newNode in self.adj_list.keys()):
            #If node has a name that is not already in the graph, add the node to the adjaceny list and the graph
            self.adj_list[newNode] = []
            self.graph.add_node(pydot.Node(newNode))
            self.updateGraph()

        else:
            #Otherwise, the node is already in the graph
            messagebox.showerror("Error", "Node already exists in graph.")

    def addEdge(self, sourceNode, sinkNode):
        #Make sure both nodes have names
        if(sourceNode == ""):
            messagebox.showerror("Error", "Source node entry box must not be empty.")

        elif(sinkNode == ""):
            messagebox.showerror("Error", "Node entry box must not be empty.")

        else:
            #If either node is not in the graph, add it to the adjacency list and the graph
            if not (sourceNode in self.adj_list.keys()):
                self.adj_list[sourceNode] = []
                self.graph.add_node(pydot.Node(sourceNode))

            if not (sinkNode in self.adj_list.keys()):
                self.adj_list[sinkNode] = []
                self.graph.add_node(pydot.Node(sinkNode))

            #Add new adjacency information to adjacency list and add edge to graph
            self.adj_list[sourceNode].append(sinkNode)
            self.adj_list[sourceNode].sort()
            self.graph.add_edge(pydot.Edge(sourceNode, sinkNode))
            self.updateGraph()


    def delNode(self, toDel):
        #Make sure node has a name
        if(toDel == ""):
            messagebox.showerror("Error", "Node entry box must not be empty.")

        #Make sure node exists in graph
        elif not (toDel in self.adj_list.keys()):
            messagebox.showerror("Error", "Node does not exist in graph.")

        else:
            #If node exists in graph, remove all edges connected to node, update adjacency information,
            #and then delete the node from the graph
            for node in self.adj_list.keys():
                while node in self.adj_list[toDel]:
                    self.delEdge(toDel, node, True)

                while toDel in self.adj_list[node]:
                    self.delEdge(node, toDel, True)

            del self.adj_list[toDel]
            self.graph.del_node(toDel)
            self.updateGraph()


    def delEdge(self, sourceNode, sinkNode, nodeDel):
        #Make sure both nodes have names
        if(sourceNode == ""):
            messagebox.showerror("Error", "Source node entry box must not be empty.")

        elif(sinkNode == ""):
            messagebox.showerror("Error", "Sink node entry box must not be empty.")

        #Make sure source node is part of the graph
        elif not (sourceNode in self.adj_list.keys()):
            messagebox.showerror("Error", "Source node does not exist")

        #Make sure there is an edge from the source node to the sink node
        elif not (sinkNode in self.adj_list[sourceNode]):
            messagebox.showerror("Error", "Edge does not exist")

        else:
            #remove the edge from the graph
            self.adj_list[sourceNode].remove(sinkNode)
            self.graph.del_edge(sourceNode, sinkNode, 0)
            if not nodeDel:
                self.updateGraph()








    def updateGraph(self):
        #Update the appearance of the graph in the GUI
        path_check = os.environ["PATH"].split(";")
        if not (os.path.dirname(os.path.abspath(__file__)) + "\\Graphviz2.38\\bin" in path_check):
            print("Not there")
            os.environ['PATH'] = os.path.dirname(os.path.abspath(__file__)) + "\\Graphviz2.38\\bin;" + os.environ[
                'PATH']
        self.graph.write_png("graph.png")
        image = Image.open("graph.png")
        #resized = image.resize((900, 300), Image.ANTIALIAS)
        self.image = ImageTk.PhotoImage(image)
        self.imageCanvas.delete("all")
        self.imageCanvas.create_image(600, 0, image=self.image)


    def DFS(self, adjList, visitOrder, findingSCC):
        #Depth first search algorithm
        vertexInfo = {}
        sccArr = []
        vertices = []
        #Initialize information for the vertices [color, predecessor, firsttime, lasttime]
        for vertex in adjList.keys():
            vertexInfo[vertex] = ['white', None, 0, 0]
            vertices.append(vertex)

        #If visit order not provided, set default
        if visitOrder == None:
            visitOrder = vertexInfo.keys()

        #Initialize time
        time = 0

        for vertex in visitOrder:
            if(vertexInfo[vertex][0] == 'white'):
                #Visit unfinished vertices
                time = self.DFSVisit(adjList, vertexInfo, vertex, time)
                #If DFS is being called in order to find strongly connected components
                #Collect information about strong components
                if(findingSCC):
                    toAdd = []
                    for remaining in vertices:
                        if vertexInfo[remaining][0] == 'black':
                            toAdd.append(remaining)

                    for complete in toAdd:
                        vertices.remove(complete)
                    sccArr.append(toAdd)

        #If DFS is being called in order to find strongly connected components
        #Return the list of components
        if findingSCC:
            return sccArr

        #Otherwise, return the information about the vertices
        return vertexInfo


    def DFSVisit(self, adjList, vertexInfo, vertex, time):
        #Set vertex as having been visited; update firsttime and time
        vertexInfo[vertex][0] = 'grey'
        vertexInfo[vertex][2] = time
        time += 1
        #Visit unvisited neighbors of the vertex
        for adjacent in adjList[vertex]:
            if vertexInfo[adjacent][0] == 'white':
                vertexInfo[adjacent][1] = vertex
                time = self.DFSVisit(adjList, vertexInfo, adjacent, time)

        #Set the vertex as being finished; update lasttine and time
        vertexInfo[vertex][0] = 'black'
        vertexInfo[vertex][3] = time
        return time + 1

    def createTranspose(self):
        #Create the transpose of the graph using its adjacency list
        transpose = {}
        for vertex in self.adj_list.keys():
            transpose[vertex] = []

        for vertex in self.adj_list.keys():
            for edge in self.adj_list[vertex]:
                transpose[edge].append(vertex)

        for vertex in transpose.keys():
            transpose[vertex].sort()

        return transpose


    def findOrder(self, vertexInfo):
        #Determing the order that vertices should be visited for finding strongly connected components
        order = []
        #Find the vertex with the highest lasttime, append it to the list of order,
        #and remove it from list of vertices to check
        while(len(vertexInfo.keys()) > 0):
            biggestTime = -1
            biggestTimeKey = ''
            for vertex in vertexInfo.keys():
                if vertexInfo[vertex][3] > biggestTime:
                    biggestTime = vertexInfo[vertex][3]
                    biggestTimeKey = vertex

            order.append(biggestTimeKey)
            del vertexInfo[biggestTimeKey]

        return order


    def SCC(self):
        #Make sure graph has nodes
        if len(self.adj_list.keys()) == 0:
            messagebox.showerror("Error", "Graph has no nodes.  No strongly connected components can be generated.")

        else:
            #Get strongly connected components
            vertexInfo = self.DFS(self.adj_list, None, False)
            strong_comps = self.DFS(self.createTranspose(), self.findOrder(vertexInfo), True)

            #Prepare visual for strongly connected components
            strong_comps_vis = pydot.Dot(graph_type='digraph')
            for component in strong_comps:
                for vertex in component:
                    strong_comps_vis.add_node(pydot.Node(vertex))
                if len(component) > 1:
                    for edge in range(-1, len(component) - 1):
                        strong_comps_vis.add_edge(pydot.Edge(component[edge], component[edge + 1]))

            path_check = os.environ["PATH"].split(";")
            if not (os.path.dirname(os.path.abspath(__file__)) + "\\Graphviz2.38\\bin" in path_check):
                print("Not there")
                os.environ['PATH'] = os.path.dirname(os.path.abspath(__file__)) + "\\Graphviz2.38\\bin;" + os.environ[
                'PATH']

            #Visualize strongly connected components
            strong_comps_vis.write_png("scc.png")
            image = Image.open("scc.png")
            # resized = image.resize((900, 300), Image.ANTIALIAS)
            self.sccImage = ImageTk.PhotoImage(image)

            #Delete old window and create new one
            if self.sccWindow != None:
                self.sccWindow.destroy()
            self.sccWindow = tkinter.Toplevel()
            sccImageLabel = tkinter.Label(self.sccWindow, image=self.sccImage)

            sccImageLabel.pack()




#Run application
DR = DirTree()
DR.run()