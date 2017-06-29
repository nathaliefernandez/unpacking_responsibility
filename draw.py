
import matplotlib.pyplot as plt

def draw(hierarchy, filename, **attr):
    # create figure
    fig = plt.figure(figsize=(12, 12))
    # get current axes (creating one if needed)
    ax = fig.gca()
    # turn axis on or off
    ax.axis('on')
    # draw the graph
    draw_graph(hierarchy, ax, .9, .1, .9, .1, .015)

    fig.savefig(filename)

    if attr.has_key('show') and attr['show']:
        plt.show()

    return None

'''
draws first node and calls recursive call to draw the others
parameters:
    ax          Axes instance       axes figure is drawn on
    right       float               x coordinate of right border
    left        float               x coordinate of left border
    top         float               y coordinate of top border
    bottom      float               y coordinate of bottom border
    size        float               diameter of node
return:
    None
'''
def draw_graph(hierarchy, ax, right, left, top, bottom, size=.015):
    if not hierarchy.graph.has_key('paths'):
        hierarchy.paths()

    height = float(top - bottom)
    length = float(right - left)

    x = length/2. + left
    y = bottom + .1

    # Circle(x coordinate, y coordinate, radius, color, edge color, zorder)
    circle = plt.Circle((x, y), size, color='w', ec='k', zorder=4)
    # add circle to 'axes' has to be added, it is an object of axes
    ax.add_artist(circle)

    ax.text(x-size, y-(size/3), hierarchy.nodes()[0], zorder=5)
    if hierarchy.node[hierarchy.nodes()[0]].has_key('threshold'):
        ax.text(x-.04, y-.006, hierarchy.node[hierarchy.nodes()[0]]['threshold'], zorder=5)
    
    # node
    __draw_graph(hierarchy, ax, left, height-bottom, length/len(hierarchy.predecessors(hierarchy.nodes()[0])), size, hierarchy.nodes()[0], (x, y), 0)

    return None
'''
draws a node and arrow to previous node(child node)
parameters:
    ax      Axes instance   axes figure is drawn on
    left    float           left border x coordinate
    height  float           height of figure
    length  float           length across figure
    size    float           diameter of nodes
    node    str             previously drawn node name
    pcoor   tuple           coordinates of previous node
    v       float           vertical spacing for previous node
return:
    None
'''
def __draw_graph(hierarchy, ax, left, height, length, size, node, pcoor, v):
    if hierarchy.predecessors(node) != []:
        for pred in xrange(len(hierarchy.predecessors(node))):
            # print 'pred %s' % pred
            c_spacing = length/2

            if hierarchy.graph['paths'].has_key(hierarchy.predecessors(node)[pred]):
                v = (height-pcoor[1])/float(len(hierarchy.graph['paths'][hierarchy.predecessors(node)[pred]]))
                x = c_spacing + length*pred + left
                y = pcoor[1] + v
            else:
                v = height - pcoor[1]
                x = c_spacing + length*pred + left
                y = pcoor[1] + v
                v = 0

            circle = plt.Circle((x, y), size, color='w', ec='k', zorder=4)
            # add circle to 'axes' has to be added, it is an object of axes
            ax.add_artist(circle)

            ax.text(x-size, y-(size/3), hierarchy.predecessors(node)[pred], zorder=5)
            if hierarchy.node[hierarchy.predecessors(node)[pred]].has_key('threshold'):
                ax.text(x-.04, y-.006, hierarchy.node[hierarchy.predecessors(node)[pred]]['threshold'], zorder=5)
            
            arrow = ax.arrow(x, y, pcoor[0] - x, pcoor[1] - y, length_includes_head=True, head_width=.01, head_length=.03, fc='k', ec='k')
            ax.add_artist(arrow)
            
            if hierarchy.predecessors(hierarchy.predecessors(node)[pred]) != []:
                __draw_graph(hierarchy, ax, left + length*pred, height, length/len(hierarchy.predecessors(hierarchy.predecessors(node)[pred])),
                                    size, hierarchy.predecessors(node)[pred], (x, y), v)
        return None
    else:
        return None