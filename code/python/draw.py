import matplotlib.pyplot as plt
import matplotlib.patches as patches
import _tkinter
import matplotlib.axes as ax

import os
from subprocess import call
from math import atan, sin, cos, pi
from random import shuffle
from hierarchy import Hierarchy


# list of color hue and saturation for each group
# [red, blue, green, purple, orange]
COLOR = [(0, 50), (210, 40), (150, 40), (15, 50)]
# COLOR = [(0, 100), (220, 100), (120, 60), (280, 100), (24, 100)]
# COLOR = [(0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0)]*50

ABC = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

# Trials
# abc = ABC[:]
# FIGSIZE = (15, 10)
# FONTSIZE = 20
# SIZE = .05
# LW = 3
# MW = .011
# ARROWLW = 1
# ARROW_L = .015
# ARROW_W = .0125
# NAME_H = 1.8
# BACKGROUND = 'white'
# OUTCOME = 'Office Goal'
# ALPHA = None
# EC = 32


# Tutorial and Comprehension
# FIGSIZE = (7.5, 5)
# FONTSIZE = 16
# SIZE = .09
# LW = 3
# MW = .02
# # + .05
# ARROWLW = 1
# ARROW_L = .021
# ARROW_W = .018
# NAME_H = 1.5
# ALPHA = None
# EC = 32


# Presentation
# abc = ABC[:]
# FIGSIZE = (15, 10)
# FONTSIZE = 20
# SIZE = .06
# LW = 5
# ARROWLW = 1
# MW = .015
# ARROW_L = .016
# ARROW_W = .015
# NAME_H = 1.8
# BACKGROUND
# OUTCOME = 'Outcome'
# ALPHA = None
# EC = 32




# Poster
abc = ABC[:]
FIGSIZE = (30, 20)
FONTSIZE = 24
WEIGHT = 500
SIZE = .05
LW = 6
MW = .011
ARROWLW = 3
ARROW_L = .015
ARROW_W = .01255
NAME_H = 1.9
# BACKGROUND = (225/255.0, 225/255.0, 225/255.0)
BACKGROUND = 'w'
OUTCOME = 'Outcome'
ALPHA = None
EC = 15
HIGHLIGHT = None


BBOX = dict(boxstyle='round, pad=0.35, rounding_size=1.0', facecolor=BACKGROUND, ec='k', lw=0, zorder=2)


'''
draw hierarchy
parameters:
    hierarchy   Hierarchy 
    **attr:
        file      str     file to save to
        arrow     list    nodes to NOT draw arrows FROM
        ID        int     trial ID, to save to experiment folder
        show      bool    whether to show the image
return:
    None
'''
def draw(hierarchy, **attr):
    shuffle(COLOR)
    shuffle(abc)

    # create figure
    if 'fig' in attr:
        if type(attr['fig']) == tuple:
            fig = plt.figure(attr['fig'])
        else:
            fig = attr['fig']
    else:
        fig = plt.figure(figsize=FIGSIZE)

    # ax.set_xlim(0, 2.0)

    # get current axes (creating one if needed)
    # ax = fig.gca()
    ax = plt.axes()
    plt.axis([0, 1.5, 0, 1])

    # turn axis on or off
    ax.axis('off')

    ax.patch.set_facecolor('black')    

    fig.subplots_adjust(left=0,bottom=0,right=1,top=1,wspace=0,hspace=0)

    if 'arrow' in attr:
        draw_hierarchy(hierarchy, ax, 1.4, .1, .9, 0.1, election=True, arrow=attr['arrow'])
    elif 'threshold' in attr:
        draw_hierarchy(hierarchy, ax, 1.4, .1, .9, 0.1, threshold=True)
    else:
        draw_hierarchy(hierarchy, ax, 1.4, .1, .9, 0.1)

    if 'file' in attr:
        fig.savefig(attr['file'], facecolor=BACKGROUND)
    else:
        if 'ID' in attr:
            ID = attr['ID']
            fig.savefig('experiment/static/images/hierarchies/hierarchy%d.png' % ID, facecolor=BACKGROUND)
        else:
            fig.savefig('images/hierarchy.png', facecolor=BACKGROUND)

    if 'show' in attr and attr['show']:
        plt.show()

    return fig

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
def draw_hierarchy(hierarchy, ax, right, left, top, bottom, size=SIZE, **attr):
    if 'paths' not in hierarchy.graph:
        hierarchy.paths()

    height = float(top - bottom)
    length = float(right - left)

    x = length/2. + left
    y = bottom + .1

    hierarchy.node[hierarchy.outcome()]['coord'] = (x, y)

    add_node(hierarchy, ax, x, y, size, None, hierarchy.outcome(), None)



    if 'threshold' not in attr:
        label_threshold(hierarchy, ax, x, y, size, hierarchy.outcome(), None)
        g=5
    if 'election' in attr:
        label_node(hierarchy, ax, x, y, size, hierarchy.outcome(), None, election=True)

        if 'arrow' in attr:
            __draw_hierarchy(hierarchy, ax, left, height-bottom, length/len(hierarchy.predecessors(hierarchy.outcome())), size, hierarchy.outcome(), (x, y), 0, COLOR, arrow=attr['arrow'], election=True)
        else:
            __draw_hierarchy(hierarchy, ax, left, height-bottom, length/len(hierarchy.predecessors(hierarchy.outcome())), size, hierarchy.outcome(), (x, y), 0, COLOR, election=True)
        return None
    else:
        label_node(hierarchy, ax, x, y, size, hierarchy.outcome(), None)
    # node
    if 'arrow' in attr:
        __draw_hierarchy(hierarchy, ax, left, height-bottom, length/len(hierarchy.predecessors(hierarchy.outcome())), size, hierarchy.outcome(), (x, y), 0, COLOR, arrow=attr['arrow'])
    else:
        __draw_hierarchy(hierarchy, ax, left, height-bottom, length/len(hierarchy.predecessors(hierarchy.outcome())), size, hierarchy.outcome(), (x, y), 0, COLOR)

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
def __draw_hierarchy(hierarchy, ax, left, height, length, size, node, pcoor, v, color, **attr):
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

            hierarchy.node[hierarchy.predecessors(node)[pred]]['coord'] = (x, y)

            add_node(hierarchy, ax, x, y, size, color[pred] if type(color) != tuple else color, node, pred)

            label_node(hierarchy, ax, x, y, size, node, pred)

            if 'threshold' not in attr:
                label_threshold(hierarchy, ax, x, y, size, node, pred)
                g=5
            dx = pcoor[0] - x 
            dy = pcoor[1] - y 

            slope = dx/dy

            if dx != 0:
                dy += (size*1.1)*sin(atan(1/slope))*(-1 if slope < 0 else 1)
                dx += cos(atan(1/slope))*(size*1.1)*(-1 if slope < 0 else 1)

            else:
                dy += size*1.1

            if 'arrow' in attr:
                if hierarchy.predecessors(node)[pred] not in attr['arrow']:
                    draw_arrow(ax, x, y, dx, dy)
            else: 
                draw_arrow(ax, x, y, dx, dy)

            if 'election' in attr:
                label_node(hierarchy, ax, x, y, size, node, pred, election=True)
                if hierarchy.predecessors(hierarchy.predecessors(node)[pred]) != []:
                    __draw_hierarchy(hierarchy, ax, left + length*pred, height, length/len(hierarchy.predecessors(hierarchy.predecessors(node)[pred])),
                                    size, hierarchy.predecessors(node)[pred], (x, y), v, color[pred] if type(color) != tuple else color, election=True)                
                    return None
            else:
                label_node(hierarchy, ax, x, y, size, node, pred)

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
    if pred == None and node == hierarchy.outcome():
        if 'color' in hierarchy.node[hierarchy.outcome()]:
            print hierarchy.node[hierarchy.outcome()]
            circle = plt.Circle((x, y), radius=size, aa=True, lw=LW, color=hierarchy.node[hierarchy.outcome()]['color'], ec=hierarchy.node[hierarchy.outcome()]['ec'], alpha=ALPHA, zorder=4)
        else:
            circle = plt.Circle((x, y), radius=size, aa=True, lw=LW, color='.3', ec='k', zorder=4)
        # add circle to 'axes' has to be added, it is an object of axes
        ax.add_artist(circle)
    else:
        color = get_color(hierarchy, color, node, pred)
        circle = plt.Circle((x, y), radius=size, aa=True, lw=LW, color=color[0], ec=color[1], alpha=ALPHA, zorder=4)
        # add circle to 'axes' has to be added, it is an object of axes
        ax.add_artist(circle)

    # circle = plt.Circle((x, y), radius=size, aa=True, lw=0, color='.5', ec='.5', alpha=.1, zorder=4)
    # ax.add_artist(circle)
    # circle = plt.Circle((x, y), radius=size, aa=True, lw=3, color=color[0], alpha=.5, ec=color[1], zorder=7)
    # ax.add_artist(circle)
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
        if 'color' not in hierarchy.node[hierarchy.predecessors(node)[pred]]:
        
            h = color[0]
            s = color[1]

            levels = hierarchy.node[hierarchy.outcome()]['level']
            lightness = 80/levels

            l = (levels - hierarchy.node[hierarchy.predecessors(node)[pred]]['level'])*lightness + 12

            hierarchy.node[hierarchy.predecessors(node)[pred]]['color'] = hsl_to_rgb(h, s, l)
            if l > 32:
                hierarchy.node[hierarchy.predecessors(node)[pred]]['ec'] = hsl_to_rgb(h, s, l-EC)
            else:
                hierarchy.node[hierarchy.predecessors(node)[pred]]['ec'] = hsl_to_rgb(h, s, 0)

            print hierarchy.node[hierarchy.predecessors(node)[pred]]['ec']
            print
        return (hierarchy.node[hierarchy.predecessors(node)[pred]]['color'], hierarchy.node[hierarchy.predecessors(node)[pred]]['ec'])

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
def label_node(hierarchy, ax, x, y, size, node, pred, **attr):

    if 'election' in attr:
        if pred == None:
            ax.text(x, y+NAME_H*size, 'Outcome', fontsize=FONTSIZE, weight=WEIGHT, bbox=BBOX, horizontalalignment='center', verticalalignment='center', zorder=2)
        else:
            # ax.text(x, y, hierarchy.outcome(), size=18, zorder=5)
            if hierarchy.predecessors(hierarchy.predecessors(node)[pred]) == []:
                ax.text(x, y+NAME_H*size, hierarchy.node[hierarchy.predecessors(node)[pred]]['name'], fontsize=FONTSIZE, weight=WEIGHT, horizontalalignment='center', verticalalignment='center', zorder=2)
            else:
                if 'team' in hierarchy.node[hierarchy.predecessors(node)[pred]]:
                    ax.text(x, y+NAME_H*size, 'Team %s' % hierarchy.node[hierarchy.predecessors(node)[pred]]['team'], fontsize=FONTSIZE, weight=WEIGHT, bbox=BBOX, horizontalalignment='center', verticalalignment='center', zorder=2)
                else:
                    groups = hierarchy.groups()
                    i = groups.index(hierarchy.predecessors(node)[pred])
                    hierarchy.node[hierarchy.predecessors(node)[pred]]['team'] = abc[i]
                    ax.text(x, y+NAME_H*size, 'Team %s' % abc[i], fontsize=FONTSIZE, weight=WEIGHT, bbox=BBOX, horizontalalignment='center', verticalalignment='center', zorder=2)
        return None

    if pred == None:
        ax.text(x, y+NAME_H*size, OUTCOME, fontsize=FONTSIZE, weight=WEIGHT, bbox=BBOX, horizontalalignment='center', verticalalignment='center', zorder=2)
    else:
        # ax.text(x, y, hierarchy.outcome(), size=18, zorder=5)
        if hierarchy.predecessors(hierarchy.predecessors(node)[pred]) == []:
            ax.text(x, y+NAME_H*size, hierarchy.node[hierarchy.predecessors(node)[pred]]['name'], fontsize=FONTSIZE, weight=WEIGHT, horizontalalignment='center', verticalalignment='center', zorder=2)
        else:
            if 'team' in hierarchy.node[hierarchy.predecessors(node)[pred]]:
                ax.text(x, y+NAME_H*size, 'Team %s' % hierarchy.node[hierarchy.predecessors(node)[pred]]['team'], fontsize=FONTSIZE, weight=WEIGHT, bbox=BBOX, horizontalalignment='center', verticalalignment='center', zorder=2)
            else:
                groups = hierarchy.groups()
                i = groups.index(hierarchy.predecessors(node)[pred])
                hierarchy.node[hierarchy.predecessors(node)[pred]]['team'] = abc[i]
                ax.text(x, y+NAME_H*size, 'Team %s' % abc[i], fontsize=FONTSIZE, weight=WEIGHT, bbox=BBOX, horizontalalignment='center', verticalalignment='center', zorder=2)

    
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
        ax.text(x-1.8*size, y-.005, '%d' % hierarchy.node[hierarchy.outcome()]['threshold'], size=FONTSIZE, bbox=BBOX, horizontalalignment='center', verticalalignment='center', zorder=2)
    elif 'threshold' in hierarchy.node[hierarchy.predecessors(node)[pred]]:
        ax.text(x-1.8*size, y-.005, '%d' % hierarchy.node[hierarchy.predecessors(node)[pred]]['threshold'], fontsize=FONTSIZE, bbox=BBOX, horizontalalignment='center', verticalalignment='center', zorder=2)
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

    arrow = ax.arrow(x, y, dx , dy, aa=True, lw=ARROWLW, length_includes_head=True, head_width=ARROW_W, head_length=ARROW_L, fc='k', ec='k', zorder=1)
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

def draw_outcomes(situation, fig, **attr):
    ax = fig.gca()

    # get current axes (creating one if needed)
    for node in situation.nodes():
        coord = situation.node[node]['coord']

        if 'value' in situation.node[node]:
            if situation.node[node]['value'] == True:
                positive(situation, ax, node, coord[0], coord[1], size=SIZE)
            else:
                negative(situation, ax, node, coord[0], coord[1], size=SIZE)

    # fig.savefig('images/situation%d.png' % attr['data']['ID'])
    # fig.savefig('experiment/static/images/instructions/instructions%d.png' % attr['data']['ID'])
    if 'file' in attr:
        fig.savefig(attr['file'], facecolor=BACKGROUND)
    elif 'ID' in attr:
        fig.savefig('experiment/static/images/situations/situation%d.png' % attr['ID'], facecolor=BACKGROUND)
    else:
        fig.savefig('images/situation.png', facecolor=BACKGROUND)

    return None

'''
draws checkmark on node 
parameters:
    siutation   Situation   hierarchy with outcomes
    ax          Axis        
    x           float       node's x position
    y           float       node's y position
return:
    None
'''
def positive(situation, ax, node, x, y, size, **attr):
    
    check = patches.Rectangle((x - (.25*size*cos(pi/4)), y - (.5*size*sin(pi/4)) - (MW*sin(pi/4))), size, MW, color='w', angle=45, zorder=6)
    mark = patches.Rectangle((x - (.25*size*cos(pi/4)), y - (.5*size*sin(pi/4)) - (MW*sin(pi/4))), MW, .5*size, color='w', angle=45, zorder=6)
    # plt.plot(x+.5*size, y+.5*size, x-.5*size, y-.5*size, linewidth=5, color='w', linestyle='solid', zorder=1)
    
    ax.add_artist(check)
    ax.add_artist(mark)
    return None

'''
draws X on node 
parameters:
    siutation   Situation   hierarchy with outcomes
    ax          Axis        
    x           float       node's x position
    y           float       node's y position
return:
    None
'''
def negative(situation, ax, node, x, y, size, **attr):
    right = patches.Rectangle((x - (.5*size*cos(pi/4)) + (.5*MW*cos(pi/4)), y - (.5*size*sin(pi/4)) - (.5*MW*sin(pi/4))), size, MW, color='w', angle=45, aa=True, zorder=10)
    left = patches.Rectangle((x + (.5*size*cos(pi/4)) - (.5*MW*cos(pi/4)), y - (.5*size*sin(pi/4)) - (.5*MW*sin(pi/4))), MW, size, color='w', angle=45, aa=True, zorder=10)

    ax.add_artist(left)
    ax.add_artist(right)
    return None

'''
highlight cause and effect nodes of interest
parameters:
    hierarchy   Hierarchy
    fig         
    cause       str     
    effect      str
    **attr:

'''
def highlight_cause_effect(hierarchy, fig, cause, effect, size=SIZE, **attr):

    ax = fig.gca()

    if cause != None:
        coord = hierarchy.node[cause]['coord']
        circle = patches.Circle((coord[0], coord[1]), radius=size+.023, aa=True, color=HIGHLIGHT, alpha=.2, lw=0, ec='.2', zorder=3)
        ax.add_patch(circle)

    if effect != None:
        coord = hierarchy.node[effect]['coord']
        effect = patches.Circle((coord[0], coord[1]), radius=size+.023, aa=True, color=HIGHLIGHT, alpha=.2, lw=0, ec='.2', zorder=3)
        ax.add_patch(effect)

    if 'file' in attr:
        fig.savefig(attr['file'], facecolor=BACKGROUND)
    else:
        fig.savefig('experiment/static/images/highlighted/highlighted%d.png' % attr['ID'], facecolor=BACKGROUND)

    return fig

'''
show predictions
parameter:
    hierarchy   Hierarchy
    fig
    cause       
    effect
    **attr:
        pivotalityr     pivotality from leaf nodes
        pivotality      pivotality from all nodes
        criticality
        file                 
'''
def show_predictions(hierarchy, fig, cause, effect, **attr):

    ax = fig.gca()

    if 'pivotalityr' in attr:
        if 'pivotality' in attr:
            if 'criticality' in attr:
                fig.suptitle('criticality: %f       pivotality: %f      pivotality*: %f' % (attr['criticality'], attr['pivotalityr'], attr['pivotality']), fontsize=26, verticalalignment='top')

    if 'file' in attr:
        fig.savefig(attr['file'], facecolor=BACKGROUND)
    else:
        fig.savefig('experiment/static/images/predictions/prediction%d.png' % attr['ID'], facecolor=BACKGROUND)

    return


