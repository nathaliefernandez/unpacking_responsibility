import matplotlib.pyplot as plt
import matplotlib.patches as patches

from math import atan, sin, cos, pi
from random import shuffle

# list of color hue and saturation for each group
# [green, blue, red, orange]
COLOR = [(0, 100), (220, 100), (120, 60), (60, 100), (24, 100)]

'''
draw hierarchy
parameters:
    hierarchy   Hierarchy 
    filename    str         file name to save graph to
return:
    None
'''
def draw(hierarchy, **attr):
    # shuffle(COLOR)

    # create figure
    fig = plt.figure(figsize=(12, 12))
    # get current axes (creating one if needed)
    ax = fig.gca()
    # turn axis on or off
    ax.axis('off')

    draw_hierarchy(hierarchy, ax, .9, .1, .9, .1)

    if 'ID' in attr:
        ID = attr['ID']
        fig.savefig('images/hierarchy%d.png' % ID)
    else:
        fig.savefig('images/hierarchy%d.png' % 0)

    if 'situation'  in attr:
        draw_situation(hierarchy, ax, .9, .1, .9, .1)
        if 'ID' in attr:
            fig.savefig('images/situation%d.png' % ID)
        else:
            fig.savefig('images/situation%d.png' % 0)

    if 'show' in attr and attr['show']:
        plt.show()

    return ax

'''
draws first node and calls recursive call to draw the others
parameters:
    ax          Axes instance       axes figure is drawn on
    right       tuple               x coordinate of right border
    left        tuple               x coordinate of left border
    top         tuple               y coordinate of top border
    bottom      tuple               y coordinate of bottom border
    size        tuple               diameter of node
return:
    None
'''
def draw_hierarchy(hierarchy, ax, right, left, top, bottom, size=.05):
    if 'paths' not in hierarchy.graph:
        hierarchy.paths()

    height = float(top - bottom)
    length = float(right - left)

    x = length/2. + left
    y = bottom + .1

    add_node(hierarchy, ax, x, y, size, None, hierarchy.nodes()[0], None)

    label_node(hierarchy, ax, x, y, size, 0, None)

    label_threshold(hierarchy, ax, x, y, size, 0, None)
    
    # node
    __draw_hierarchy(hierarchy, ax, left, height-bottom, length/len(hierarchy.predecessors(hierarchy.nodes()[0])), size, hierarchy.nodes()[0], (x, y), 0, COLOR)

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
    pcoor   float           coordinates of previous node
    v       float           vertical spacing for previous node
return:
    None
'''
def __draw_hierarchy(hierarchy, ax, left, height, length, size, node, pcoor, v, color):
    if hierarchy.predecessors(node) != []:
        for pred in xrange(len(hierarchy.predecessors(node))):
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

            add_node(hierarchy, ax, x, y, size, color[pred] if type(color) != tuple else color, node, pred)

            label_node(hierarchy, ax, x, y, size, node, pred)

            label_threshold(hierarchy, ax, x, y, size, node, pred)

            dx = pcoor[0] - x 
            dy = pcoor[1] - y 

            slope = dx/dy

            if dx != 0:
                dy += (size)*sin(atan(1/slope))*(-1 if slope < 0 else 1)
                dx += cos(atan(1/slope))*(size)*(-1 if slope < 0 else 1)

            else:
                dy += size

            
            draw_arrow(ax, x, y, dx, dy)
            
            if hierarchy.predecessors(hierarchy.predecessors(node)[pred]) != []:
                __draw_hierarchy(hierarchy, ax, left + length*pred, height, length/len(hierarchy.predecessors(hierarchy.predecessors(node)[pred])),
                                    size, hierarchy.predecessors(node)[pred], (x, y), v, color[pred] if type(color) != tuple else color)
        return None
    else:
        return None

'''
draw node 
parameters:
    ax      Axes
    x       float       x coordinate
    y       float       y coordinate
    color   float       (hue[0-360], saturation[0-100])
return :
    None
'''
def add_node(hierarchy, ax, x, y, size, color, node, pred):
    if pred == None:
        circle = plt.Circle((x, y), radius=size, color='w', ec='k', zorder=4)
        # add circle to 'axes' has to be added, it is an object of axes
        ax.add_artist(circle)
    else:
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
        lightness = 70/levels

        l = (levels- hierarchy.node[hierarchy.predecessors(node)[pred]]['level'])*lightness + 12
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
    if pred != None:
        # ax.text(x, y, hierarchy.nodes()[0], size=18, zorder=5)
        if hierarchy.predecessors(hierarchy.predecessors(node)[pred]) == []:
            ax.text(x, y+1.5*size, hierarchy.node[hierarchy.predecessors(node)[pred]]['name'], size=18, horizontalalignment='center', verticalalignment='center', zorder=5)
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
        ax.text(x-1.5*size, y, hierarchy.node[hierarchy.nodes()[node]]['threshold'], size=18, horizontalalignment='center', verticalalignment='center', zorder=5)
    elif 'threshold' in hierarchy.node[hierarchy.predecessors(node)[pred]]:
        ax.text(x-1.5*size, y, hierarchy.node[hierarchy.predecessors(node)[pred]]['threshold'], fontsize=18, horizontalalignment='center', verticalalignment='center', zorder=5)
    return None
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

'''
draws first node and calls recursive call to draw the others
parameters:
    ax          Axes instance       axes figure is drawn on
    right       tuple               x coordinate of right border
    left        tuple               x coordinate of left border
    top         tuple               y coordinate of top border
    bottom      tuple               y coordinate of bottom border
    size        tuple               diameter of node
return:
    None
'''
def draw_situation(situation, ax, right, left, top, bottom, size=.05):
    if 'paths' not in situation.graph:
        situation.paths()

    height = float(top - bottom)
    length = float(right - left)

    x = length/2. + left
    y = bottom + .1

    if situation.node[situation.nodes()[0]]['value'] == True:
        positive(situation, ax, x, y, size)
    else:
        negative(situation, ax, x, y, size)

    __draw_situation(situation, ax, left, height-bottom, length/len(situation.predecessors(situation.nodes()[0])), size, situation.nodes()[0], (x, y), 0, COLOR)

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
    pcoor   float           coordinates of previous node
    v       float           vertical spacing for previous node
return:
    None
'''
def __draw_situation(situation, ax, left, height, length, size, node, pcoor, v, color):
    if situation.predecessors(node) != []:
        for pred in xrange(len(situation.predecessors(node))):
            c_spacing = length/2

            if situation.predecessors(node)[pred] in situation.graph['paths']:
                v = (height-pcoor[1])/float(len(situation.graph['paths'][situation.predecessors(node)[pred]]))
                x = c_spacing + length*pred + left
                y = pcoor[1] + v
            else:
                v = height - pcoor[1]
                x = c_spacing + length*pred + left
                y = pcoor[1] + v
                v = 0
            
            if situation.predecessors(situation.predecessors(node)[pred]) != []:
                __draw_situation(situation, ax, left + length*pred, height, length/len(situation.predecessors(situation.predecessors(node)[pred])),
                                    size, situation.predecessors(node)[pred], (x, y), v, color[pred] if type(color) != tuple else color)
        return None
    else:
        return None

def positive(situation, ax, x, y, size):
    check = patches.Rectangle((x - (.25*size*cos(pi/4)), y - (.5*size*sin(pi/4)) - (.01*sin(pi/4))), size, .01, color='k', angle=45, zorder=10)
    mark = patches.Rectangle((x - (.25*size*cos(pi/4)), y - (.5*size*sin(pi/4)) - (.01*sin(pi/4))), .01, .5*size, color='k', angle=45, zorder=10)
    # plt.plot(x+.5*size, y+.5*size, x-.5*size, y-.5*size, linewidth=5, color='w', linestyle='solid', zorder=1)
    
    ax.add_artist(check)
    ax.add_artist(mark)
    return None

def negative(situation, ax, x, y, size):
    right = patches.Rectangle((x - (.5*size*cos(pi/4)) + (.5*.01*cos(pi/4)), y - (.5*size*sin(pi/4)) - (.5*.01*sin(pi/4))), size, .01, color='k', angle=45, zorder=10)
    left = patches.Rectangle((x + (.5*size*cos(pi/4)) - (.5*.01*cos(pi/4)), y - (.5*size*sin(pi/4)) - (.5*.01*sin(pi/4))), .01, size, color='k', angle=45, zorder=10)

    ax.add_artist(left)
    ax.add_artist(right)
    return None