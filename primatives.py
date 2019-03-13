class samplepoint(object):
  def __init__(self,position=[0.0,0.0],qstate=None):
    self.position = position
    self.qstate = qstate
    self.halfedge = None

class samplehalfedge(object):
  def __init__(self,startpoint,endpoint):
    assert type(startpoint) is samplepoint
    assert type(endpoint) is samplepoint
    self.startpoint = startpoint
    self.endpoint = endpoint
    self.startpoint.halfedge = self
    self.cell = None

  def twin(self):
    self.twin = samplehalfedge(self.endpoint,self.startpoint)
    return self.twin

class samplecell(object):
  def __init__(self,shalfedges):
    assert type(shalfedges[0]) is samplehalfedge
    assert type(shalfedges[1]) is samplehalfedge
    assert type(shalfedges[2]) is samplehalfedge
    self.halfedges = shalfedges
    assert shalfedges[0].startpoint == shalfedges[2].endpoint
    self.vertices = [shalfedges[0].startpoint]
    assert shalfedges[1].startpoint == shalfedges[0].endpoint
    self.vertices.append(shalfedges[1].startpoint)
    assert shalfedges[2].startpoint == shalfedges[1].endpoint
    self.vertices.append(shalfedges[2].startpoint)
    for halfedge in self.halfedges:
        halfedge.cell = self

def test():
    a = samplepoint([0.0,0.0],3)
    b = samplepoint([1.0,0.0],3)
    c = samplepoint([0.5,0.866],4)

    ab = samplehalfedge(a,b)
    ba = ab.twin()
    ab = ba.twin()
    bc = samplehalfedge(b,c)
    cb = bc.twin()
    bc.twin = cb
    ca = samplehalfedge(c,a)
    ac = ca.twin()
    ca.twin = ac

    abc = samplecell([ab,bc,ca])
    cba = samplecell([cb,ba,ac])

if __name__ == '__main__':
    test()
