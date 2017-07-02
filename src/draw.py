<<<<<<< HEAD
=======

>>>>>>> d8d5659f3d1012540de7533f715b57d8160863a6
import matplotlib.pyplot as plt
from math import atan, sin, cos
import matplotlib.patches as patches

<<<<<<< HEAD
# list of color hue and saturation for each group
# [green, blue, red, orange]
COLOR = [(120, 60), (220, 100), (0, 100), (15, 100)]

'''
draw hierarchy
parameters:
    hierarchy   Hierarchy 
    filename    str         file name to save graph to
return:
    None
'''
=======
>>>>>>> d8d5659f3d1012540de7533f715b57d8160863a6
def draw(hierarchy, filename, **attr):
    # create figure
    fig = plt.figure(figsize=(12, 12))
    # get current axes (creating one if needed)
    ax = fig.gca()
    # turn axis on or off
    ax.axis('on')
    # draw the graph
    draw_graph(hierarchy, ax, .9, .1, .9, .1)

    fig.savefig(filename)

    if 'show' in attr and attr['show']:
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
def draw_graph(hierarchy, ax, right, left, top, bottom, size=.05):
    if 'paths' not in hierarchy.graph:
        hierarchy.paths()
<<<<<<< HEAD
=======
    print 'draw', size
>>>>>>> d8d5659f3d1012540de7533f715b57d8160863a6

    height = float(top - bottom)
    length = float(right - left)

    x = length/2. + left
    y = bottom + .1

    # Circle(x coordinate, y coordinate, radius, color, edge color, zorder)
    circle = plt.Circle((x, y), radius=size, color='w', ec='k', zorder=4)
    # add circle to 'axes' has to be added, it is an object of axes
    ax.add_artist(circle)
<<<<<<< HEAD

    label_node(hierarchy, ax, x, y, size, 0, None)

    label_threshold(hierarchy, ax, x, y, size, 0, None)
    
    # node
    __draw_graph(hierarchy, ax, left, height-bottom, length/len(hierarchy.predecessors(hierarchy.nodes()[0])), size, hierarchy.nodes()[0], (x, y), 0, COLOR)
=======
    print '1st (x, y)', (x, y)
    ax.text(x, y, hierarchy.nodes()[0], zorder=5)
    if 'threshold' in hierarchy.node[hierarchy.nodes()[0]]:
        ax.text(x, y, hierarchy.node[hierarchy.nodes()[0]]['threshold'], zorder=5)
    
    # node
    __draw_graph(hierarchy, ax, left, height-bottom, length/len(hierarchy.predecessors(hierarchy.nodes()[0])), size, hierarchy.nodes()[0], (x, y), 0)
>>>>>>> d8d5659f3d1012540de7533f715b57d8160863a6

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
<<<<<<< HEAD
def __draw_graph(hierarchy, ax, left, height, length, size, node, pcoor, v, color):
    if hierarchy.predecessors(node) != []:
        for pred in xrange(len(hierarchy.predecessors(node))):
=======
def __draw_graph(hierarchy, ax, left, height, length, size, node, pcoor, v):
    if hierarchy.predecessors(node) != []:
        for pred in xrange(len(hierarchy.predecessors(node))):
            # print 'pred %s' % pred
>>>>>>> d8d5659f3d1012540de7533f715b57d8160863a6
            c_spacing = length/2

            if hierarchy.predecessors(node)[pred] in hierarchy.graph['paths']:
                v = (height-pcoor[1])/float(len(hierarchy.graph['paths'][hierarchy.predecessors(node)[pred]]))
                x = c_spacing + length*pred + left
                y = pcoor[1] + v
            else:
                v = height - pcoor[1]
                x = c_spacing + length*pred + left
                y = pcoor[1] + v
                v = 0

<<<<<<< HEAD
            add_node(hierarchy, ax, x, y, node, pred, size, color[pred] if type(color[pred]) == tuple else color)

            label_node(hierarchy, ax, x, y, size, node, pred)

            label_threshold(hierarchy, ax, x, y, size, node, pred)
=======
            circle = plt.Circle((x, y), radius=size, color='w', ec='k', zorder=4)
            # add circle to 'axes' has to be added, it is an object of axes
            ax.add_artist(circle)

            ax.text(x, y, hierarchy.predecessors(node)[pred], zorder=5)
            if 'threshold' in hierarchy.node[hierarchy.predecessors(node)[pred]]:
                ax.text(x-.04, y-.006, hierarchy.node[hierarchy.predecessors(node)[pred]]['threshold'], zorder=5)
>>>>>>> d8d5659f3d1012540de7533f715b57d8160863a6


            dx = pcoor[0] - x 
            dy = pcoor[1] - y 

<<<<<<< HEAD
            slope = dx/dy

            if dx != 0:
                dy += (size)*sin(atan(1/slope))*(-1 if slope < 0 else 1)
                dx += cos(atan(1/slope))*(size)*(-1 if slope < 0 else 1)

            else:
                dy += size

            
            draw_arrow(ax, x, y, dx, dy)
            
            if hierarchy.predecessors(hierarchy.predecessors(node)[pred]) != []:
            
                __draw_graph(hierarchy, ax, left + length*pred, height, length/len(hierarchy.predecessors(hierarchy.predecessors(node)[pred])),
                                    size, hierarchy.predecessors(node)[pred], (x, y), v, color[pred] if type(color[pred]) == tuple else color)
        return None
    else:
        return None

'''
draw node 
parameters:
    ax      Axes
    x       float       x coordinate
    y       float       y coordinate
    color   tuple       (hue[0-360], saturation[0-100])
return :
    None
'''
def add_node(hierarchy, ax, x, y, node, pred, size, color):
    print 'add node'
    print hierarchy.predecessors(node)[pred]
    print 'color', color
    circle = plt.Circle((x, y), radius=size, color=get_color(hierarchy, color, node, pred), ec='k', zorder=4)
        
    # add circle to 'axes' has to be added, it is an object of axes
    ax.add_artist(circle)
    return None

'''
return color of node
parameters:
    hierarchy   Hierarchy   
    color       tuple       (hue[0-360], saturation[0-100]) 
    node        str         succesor 
    pred        int         index of node pred to be drawn
return:
    None
'''
def get_color(hierarchy, color, node, pred):

    if pred == None:
        return 'w'
    else:
        h = color[0]
        s = color[1]

        levels = hierarchy.node[hierarchy.nodes()[0]]['level']
        lightness = 60/levels

        print 'level', hierarchy.node[hierarchy.predecessors(node)[pred]]['level']
        l = (levels- hierarchy.node[hierarchy.predecessors(node)[pred]]['level'])*lightness
        print 
        print hierarchy.predecessors(node)[pred]
        print (h, s, l)
        return hsl_to_rgb(h, s, l)

'''
label name of node
parameters:
    Hierarchy   Hierarchy
    ax          Axes
    x           float       x coordinate
    y           float       y coordinate
    size        float       radius of node
    node        str         succesor
    pred        int         index of node pred to be drawn
'''
def label_node(hierarchy, ax, x, y, size, node, pred):
    if pred == None:
        ax.text(x, y, hierarchy.nodes()[0], zorder=5)
    else:
        ax.text(x, y, hierarchy.predecessors(node)[pred], zorder=5)
    return None

'''
label threshold of aggregate nodes to the left of node
parametes:
    hierarchy       Hierarchy
    ax              Axes
    x               float           x coordinate
    y               float           y coordinate
    size            float           radius of node
    node            str             sucessor
    pred            int             index of node pred to be drawn
return:
    None    
'''
def label_threshold(hierarchy, ax, x, y, size, node, pred):
    if pred == None:
        print hierarchy.node[hierarchy.nodes()[node]]
        ax.text(x - 2*size, y, hierarchy.node[hierarchy.nodes()[node]]['threshold'], zorder=5)
    elif 'threshold' in hierarchy.node[hierarchy.predecessors(node)[pred]]:
        ax.text(x - size, y, hierarchy.node[hierarchy.predecessors(node)[pred]]['threshold'], zorder=5)

'''
draw arrow from pred to node
parameters:
    ax      Axes
    x       float       x coordinate of pred
    y       float       y coorderinate of pred
    dx      float       change in x to reach successor
    dy      float       change in y to reach successor

'''
def draw_arrow(ax, x, y, dx, dy):
    newx = dx + x
    newy = dy + y
    #arrow = patches.FancyArrowPatch(posA=(x, y), posB=(newx, newy), shrinkB=2, zorder=1)

    arrow = ax.arrow(x, y, dx , dy, length_includes_head=True, head_width=.01, head_length=.02, fc='k', ec='k', zorder=3)
    ax.add_artist(arrow)
    return None

'''
convert hue saturation tuple to rgb format
parameters;
    h   int     hue[0-360]
    s   int     saturation[0-100]
    l   int     lightness[0-100]
return:
    tuple       RGB
'''
def hsl_to_rgb(h, s, l):
    h /= 360.0
    s /= 100.0
    l /= 100.0

    if(s == 0):
        # achromatic
        r = g = b = l 
    else:
        def hue_to_rgb(p, q, t):
            if t < 0:
                t += 1
            if t > 1:
                t -= 1
            if t < 1.0/6.0:
                return p + (q - p) * 6 * t
            if t < 1.0/2.0:
                return q
            if t < 2.0/3.0:
                return p + (q - p) * (2.0/3.0 - t) * 6
            return p

    q = l * (1 + s) if l < 0.5 else l + s - l * s
    p = 2 * l - q

    r = hue_to_rgb(p, q, h + 1.0/3.0)
    g = hue_to_rgb(p, q, h);
    b = hue_to_rgb(p, q, h - 1.0/3.0)

    return (r, g, b)
=======
            newx = pcoor[0] 
            newy = pcoor[1]

            slope = dx/dy
            print hierarchy.predecessors(node)[pred]
            if dx != 0:
                newy += (size+.002)*sin(atan(1/slope))*(-1 if slope < 0 else 1)
                print size
                print '0', (size+.002)*sin(atan(1/slope))*(-1 if slope < 0 else 1)
                newx += cos(atan(1/slope))*(size+.002)*(-1 if slope < 0 else 1)

            else:
                newy += size+.002
                print 'else', size


            print '(x, y)', (x, y)
            print 'points to (x, y)', (newx, newy)
            print
            arrow = patches.FancyArrowPatch(posA=(x, y), posB=(newx, newy), shrinkB=2, zorder=1)
            
            # arrow = ax.arrow(x, y, dx , dy, length_includes_head=True, head_width=.001, head_length=.002, fc='k', ec='k', zorder=7)
            ax.add_artist(arrow)
            
            if hierarchy.predecessors(hierarchy.predecessors(node)[pred]) != []:
                __draw_graph(hierarchy, ax, left + length*pred, height, length/len(hierarchy.predecessors(hierarchy.predecessors(node)[pred])),
                                    size, hierarchy.predecessors(node)[pred], (x, y), v)
        return None
    else:
        return None
>>>>>>> d8d5659f3d1012540de7533f715b57d8160863a6
