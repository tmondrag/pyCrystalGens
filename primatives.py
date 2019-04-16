import math
from itertools import izip

class samplepoint(object):
    def __init__(self,position=[0.0,0.0],qstate=None):
        assert len(position) > 1 # point position should be an iterable af at least size 2
        for coordinate in position:
            assert 0 == coordinate * 0 # all objects in position iterable should be numeric

        self.position = position
        self.qstate = qstate
        self.halfedge = None

class samplehalfedge(object):
    def __init__(self,startpoint,endpoint):
        if type(startpoint) is samplepoint:
            self.startpoint = startpoint
        else:
            for coord in startpoint:
                assert 0 == 0 * coord  # coordinates must be numeric
            self.startpoint = samplepoint(startpoint)

        if type(endpoint) is samplepoint:
            self.endpoint = endpoint
        else:
            for coord in endpoint:
                assert 0 == 0 * coord  # coordinates must be numeric
            self.endpoint = samplepoint(endpoint)

        assert len(self.startpoint.position) == len(self.endpoint.position) # the start and end points must have the same dimensionality
        self.startpoint.halfedge = self
        self.cell = None
        self.twin = None
        self.calculateLength()
        self.calculateMidpoint()

    def createTwin(self):
        self.twin = samplehalfedge(self.endpoint,self.startpoint)
        self.twin.twin = self
        return self.twin

    def calculateLength(self):
        it = izip(self.startpoint.position,self.endpoint.position)
        self.length = 0
        for a,b in it:
            self.length += (a-b)*(a-b)

        self.length = math.sqrt(self.length)
        return self.length

    def calculateMidpoint(self):
        self.midpoint = []
        for i in range(len(self.startpoint.position)):
            self.midpoint.append(self.startpoint.position[i] + self.endpoint.position[i])
            self.midpoint[i] = self.midpoint[i]/2
        return self.midpoint

class sampleedge(object):
    def __init__(self, startpoint,endpoint):
        self.halfedges = [None,None]
        self.halfedges[0] = samplehalfedge(startpoint,endpoint)
        self.halfedges[1] = self.halfedges[0].createTwin()
        self.startpoint = self.halfedges[0].startpoint
        self.endpoint = self.halfedges[0].endpoint
        self.length = self.halfedges[0].length
        self.midpoint = self.halfedges[0].midpoint
        self.broken = self.startpoint.qstate != self.endpoint.qstate # not a super deep comparison, might give erroneous results if qstates are more complex than simple dicts


class samplecell(object):
    def __init__(self,bounds):
        assert len(bounds) == 3 # bounds defines the boundaries of a triangle so it must be an iterable of length 3
        if type(bounds[1]) is samplehalfedge:
            self.createTriangleFromHalfedges(bounds)
        else if type(bounds[2]) is samplepoint:
            self.createTriangleFromVertices(bounds)
        else:
            self.createTriangleFromCoordinates(bounds)

    def createTriangleFromHalfedges(self,hedges):
        assert type(hedges[0]) is samplehalfedge
        assert type(hedges[1]) is samplehalfedge
        assert type(hedges[2]) is samplehalfedge
        assert hedges[0].startpoint == hedges[2].endpoint
        self.vertices = [hedges[0].startpoint]
        assert hedges[1].startpoint == hedges[0].endpoint
        self.vertices.append(hedges[1].startpoint)
        assert hedges[2].startpoint == hedges[1].endpoint
        self.vertices.append(hedges[2].startpoint)
        self.halfedges = hedges
        for halfedge in self.halfedges:
            halfedge.cell = self

    def createTriangleFromVertices(self,points):
        assert type(points[0]) is samplepoint
        assert type(points[1]) is samplepoint
        assert type(points[2]) is samplepoint
        self.vertices = points
        self.halfedges = []
        self.halfedges.append(samplehalfedge(points[0],points[1]))
        self.halfedges.append(samplehalfedge(points[1],points[2]))
        self.halfedges.append(samplehalfedge(points[2],points[0]))
        for halfedge in self.halfedges:
            halfedge.cell = self

    def createTriangleFromCoordinates(self,coords):
        assert len(coords[0]) == len(coords[1])
        assert len(coords[2]) == len(coords[1])
        self.vertices = []
        self.vertices.append(coords[0])
        self.vertices.append(coords[1])
        self.vertices.append(coords[2])
        points = self.vertices
        self.halfedges = []
        self.halfedges.append(samplehalfedge(points[0],points[1]))
        self.halfedges.append(samplehalfedge(points[1],points[2]))
        self.halfedges.append(samplehalfedge(points[2],points[0]))
        for halfedge in self.halfedges:
            halfedge.cell = self

    def calculateSteiner(self):
        self.SteinerPoint = [0.0,0.0]


def test():
    a = samplepoint([0.0,0.0],3)
    b = samplepoint([1.0,0.0],3)
    c = samplepoint([0.5,0.866],4)

    ab = samplehalfedge(a,b)
    ba = ab.createTwin()
    ba.twin = ab
    bc = samplehalfedge(b,c)
    cb = bc.createTwin()
    bc.twin = cb
    ca = samplehalfedge(c,a)
    ac = ca.twin()
    ca.twin = ac

    abc = samplecell([ab,bc,ca])
    cba = samplecell([cb,ba,ac])

if __name__ == '__main__':
    test()
