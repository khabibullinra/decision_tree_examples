"""
Расчет ценности информации с использованием деревьев решений

2024
"""

import matplotlib.pyplot as plt
import matplotlib.patches
import matplotlib.path

from matplotlib.patches import Circle, Rectangle, FancyArrowPatch, RegularPolygon, Path


# ==================================================================
# отображение дерева с использованием matplotlib
# ==================================================================

def _patch_terminal(x, y, ax, 
                    val=None, 
                    prob=None,
                    details=2):
    """
    избражение терминального узла, форма, размеры, цвет
    x, y - координаты на узла на рисунке
    ax - оси matplotlib на который рисунок формируется
    val - итоговое значение выигрыша терминального узла
    prob - итоговая вероятность выигрыша терминального узла
    details - детализация отображения (показывать расчетные итоги или нет)
    """
    xshift = 20
    yshift = -10
    p = RegularPolygon((x, y), 3, radius=0.2, orientation=3.14/2, ec="b", fc='g')
    ax.add_artist(p)

    if val != None and p != None and details > 2:
        label = f'v = {val:.2f} \np = {prob:.2f}'
        ax.annotate(label, (x, y), xycoords='data',
                    xytext=(xshift, yshift), textcoords='offset points')
    
    return p

def _patch_decision(x, y, 
                    ax, 
                    label="", 
                    emv=None, 
                    voi=None,
                    details=2):
    """
    избражение узла принятия решений, форма, размеры, цвет
    x, y - координаты на узла на рисунке
    ax - оси matplotlib на который рисунок формируется
    label - название узла
    emv - расчетная ожидаемая доходность узла
    voi - расчетная ценность информации узла, если в дереве есть соответствующие метки для расчета
    details - детализация отображения (показывать расчетные итоги или нет)
    """
    p = Rectangle((x-0.2, y-0.2), 0.4, 0.4, ec="b", fc='r')
    ax.add_artist(p)
    if details > 0:
        ax.annotate(label, (0.5, 1.05), xycoords=p, ha='center', va='bottom')
    if details > 1:
        label2 = f'EMV={emv:.1f} \n' if emv!=None else ""
        label3 = f'VOI={voi:.2f}' if voi!=None else ""
        label4 = label2 + label3
        ax.annotate(label4, (0.5, -0.25), xycoords=p, ha='center', va='top')
    return p   
    
def _patch_chance(x, y, 
                  ax, 
                  label="", 
                  emv=None,
                  details=2):
    """
    избражение вероятностного узла, форма, размеры, цвет
    x, y - координаты на узла на рисунке
    ax - оси matplotlib на который рисунок формируется
    label - название узла
    emv - расчетная ожидаемая доходность узла
    details - детализация отображения (показывать расчетные итоги или нет)
    """
    p = Circle((x, y), 0.2, ec="b", fc='y')
    ax.add_artist(p)
    if details > 0:
        ax.annotate(label, (0.5, 1.05), xycoords=p, ha='center', va='bottom')
    if details > 1:
        label2 = f'EMV={emv:.1f}' if emv!=None else ""
        ax.annotate(label2, (0.5, -0.25), xycoords=p, ha='center', va='top')

    return p

def _patch_edge(x1, y1, 
                x2, y2, 
                ax, 
                label="", 
                payoff=None, 
                probability=None,
                width=1,
                details=2):
    """
    избражение связи узлов, форма, размеры, цвет
    x1, y1 - координаты первого узла на рисунке
    x2, y2 - координаты второго узла на рисунке
    ax - оси matplotlib на который рисунок формируется
    label - название связи
    payoff - выигрыш/затраты для связи
    probability - вероятность связи для вероятностного узла, признак решения для узла решений
    width - ширина соединительной линии для отображения
    details - детализация отображения (показывать расчетные итоги или нет)
    """
    yshift = -5
    vertices = [(x1+0.25, y1), (x1+0.75, y1), (x1+1, y2), (x2-0.25, y2)]
    codes = [matplotlib.path.Path.MOVETO,
             matplotlib.path.Path.LINETO,
             matplotlib.path.Path.LINETO,
             matplotlib.path.Path.LINETO,
             ]

    path = Path(vertices, codes)

    l = FancyArrowPatch(path=path, 
                        arrowstyle="->, head_length=4, head_width=3",
                        connectionstyle = "arc,angleA=0,angleB=180,armA=5,armB=5,rad=0",
                        linewidth=width,
        )
    if details > 0:
        ax.annotate(label, (x1+1.1, y2), 
                    xycoords='data', 
                    xytext=(0, 5), 
                    textcoords='offset points')
    if details > 2:
        ax.annotate(f'$v={payoff:.0f}$, $p={probability:.2f}$', (x1+1.05, y2), 
                    xycoords='data',
                    xytext=(2, yshift), 
                    textcoords='offset points', 
                    va='top')
    
    ax.add_artist(l)
    return l


def _num_terminal_nodes(node, num=0):
    """
    подсчет терминальных узлов
    - определение y координат терминальных узлов
    """

    if 'child_edges' in node:
        for edge in node['child_edges']:
            child_node = edge['child_node']
            if child_node['type'] == 'terminal':
                child_node['num'] = num
                num = num + 1
            else:
                num = _num_terminal_nodes(child_node, num)
    return num

def _num_maxlevel(node, level=0):
    node['level'] = level

    if 'child_edges' in node:
        num_list:list = []
        for edge in node['child_edges']:
            child_node = edge['child_node']
            num = _num_maxlevel(child_node, level+1) 
            num_list.append(num)
        maxlevel = max(num_list) 
        return maxlevel
    else:
        return level


def _num_other_nodes(node, level=0, num=0):
    """
    вычисление координат узлов на основе терминальных узлов (должны быть подсчитаны ранее)
    """
    node['level'] = level
    #node['num'] = num

    if 'child_edges' in node:
        num_list:list = []
        for edge in node['child_edges']:
            child_node = edge['child_node']
            num = _num_other_nodes(child_node, level+1) 
            num_list.append(num)
        #print(num_list)
        num = sum(num_list) / len(num_list) if len(num_list) > 0 else 1
        node['num'] = num
        return num
    else:
        #tree['y'] = num
        if node['type'] == 'terminal':
            return node['num']
        else:
            return num

def _plot(node, ax, prob=1,  xshift=3, details=2):
    name = node['name'] if 'name' in node else ""
    if node['type'] == 'decision':
        p = _patch_decision(x = node['level'] * xshift, 
                            y = node['num'], 
                            ax = ax, 
                            label = name,
                            emv = node['emv'] if 'emv' in node else None,
                            voi = node['voi'] if 'voi' in node else None,
                            details=details)
    if node['type'] == 'chance':
        p = _patch_chance(x = node['level'] * xshift, 
                          y = node['num'], 
                          ax = ax, 
                          label = name,
                          emv = node['emv'] if 'emv' in node else None,
                          details=details)
    if node['type'] == 'terminal':
        p = _patch_terminal(x = node['level'] * xshift, 
                            y = node['num'], 
                            ax = ax,
                            val = node['value'] if 'value' in node else None,
                            prob = node['probability'] if 'probability' in node else None,
                            details=details)

    if 'child_edges' in node:
        for edge in node['child_edges']:
            child_node = edge['child_node']
            prob_val = edge['probability'] if 'probability' in edge else 0
            _plot(child_node, ax, 
                       prob = prob *  prob_val, 
                       xshift=xshift, 
                       details=details)
            edge_name = edge['name'] if 'name' in edge else ""
            _patch_edge(node['level'] * xshift, node['num'], 
                        child_node['level'] * xshift, child_node['num'],
                        ax=ax, 
                        label=edge_name, 
                        payoff=edge['payoff'] if 'payoff' in edge else 0,
                        probability=prob_val, 
                        width=2 if prob * prob_val > 0 else 1,
                        details=details)
            

def plot_tree(tree, ax, xshift=3, details=2):
    """ 
    отрисовка дерева с использованием matplotlib на оси ax
    tree
    ax
    xshift - сдвиг по оси х 
    details - уровень детализации подписей (0 - нет подписей, 1 - подписи узлов, 2 - подписи все)
    """

    my = _num_terminal_nodes(tree)
    _num_other_nodes(tree)
    _plot(tree, ax, xshift=xshift, details=details)
    mx = _num_maxlevel(tree)
    #print(f' max level = {mx}')
    ax.set_xlim(-1, mx * xshift + 2)
    ax.set_ylim(-1, my )
    ax.axis('off')
    ax.set_aspect('equal')
    #print(mx, my)
    
def solve_tree(tree):

    # два раза запустим решение (пока так надо чтобы рассчитать вероятности лучших решений)
    _solve_tree(tree)
    _solve_tree(tree)


def _solve_tree(node, _value_terminal=0, _probability_terminal=1):
    """
    рекурсивное решение дерева заданного в виде словаря
    node -- узел дерева для расчета. для расчета всего дерева - корневой узел
    _value_terminal - расчетное значение итогового выигрыша
    _probability_terminal - расчетное значение итоговой вероятности
    """
    
    if node['type'] == 'terminal':
        # для терминального узла сохраняем в нем итоговые выигрыши и вероятности
        node['emv'] = 0
        node['value'] = _value_terminal
        node['probability'] = _probability_terminal
    else:
        # или 'decision' или 'chance' с дочерними узлами
        node['emv'] = 0                             # задаем начальное приближение emv узла
        if node['type'] == 'decision':
            node['emv_child_nodes'] = {}            # готовим словарь для подсчета emv дочерних узлов
        num = 0                                 # сбрасываем счетчик
        
        for edge in node['child_edges']:            # переберем все связи рассматриваемого узла
            if node['type'] == 'decision':          
                edge['id'] = num
                num = num + 1

            # рекурсивно рассчитаем параметры дочерних узлов
            child_node_value = _value_terminal + edge['payoff'] 
            child_node_probability = _probability_terminal * edge['probability'] if 'probability' in edge else 1
            _solve_tree(edge['child_node'], child_node_value, child_node_probability)

            # рассчитаем emv рассматриваемого узла
            if node['type'] == 'decision':
                # для узла принятия решений соберем emv все дочерних узлов, чтобы найти оптимальный потом
                node['emv_child_nodes'][edge['id']] = edge['child_node']['emv'] + edge['payoff']
            else:
                # для вероятностного узла - сразу считаем emv по формуле полной вероятности при переборе потомков
                node['emv'] = node['emv'] + (edge['child_node']['emv'] + edge['payoff']) * edge['probability']

        # для узла решения определим оптимальное - из максимизации EMV
        if node['type'] == 'decision':
            node['emv'] = max(node['emv_child_nodes'].values())
            for edge in node['child_edges']:
                if node['emv_child_nodes'][edge['id']] == node['emv']:
                    edge['probability'] = 1
                else:
                    edge['probability'] = 0
            # оценим VOI для узла решения
            emv_wi = 0
            emv_woi = 0
            calc_voi = [False, False]
            for edge in node['child_edges']:
                if 'voi_info' in edge:
                    if edge['voi_info']=='with_info':
                        emv_wi = node['emv_child_nodes'][edge['id']] - edge['payoff']
                        calc_voi[0] = True
                    if edge['voi_info']=='without_info':
                        emv_woi = node['emv_child_nodes'][edge['id']] - edge['payoff']
                        calc_voi[1] = True
            if calc_voi == [True, True]:
                node['voi'] = emv_wi - emv_woi
      



def print_tree(tree, level=0):
    if level == 0:
        print('|','-'*level,  f" {tree['type']} : {tree['name'] if 'name' in tree else ''} [ {tree['emv']}]" )
    else:
        if 'child_node' in tree:
            print('|', '-'*level,  
                  f" {tree['name']} ",
                  f" [payoff:{tree['payoff']} { (' p = ' + str(tree['probability'])) if 'probability' in tree else '' }] -> ",
                  f"  {tree['child_node']['type']} : {tree['child_node']['name'] if 'name' in tree['child_node'] else ''} [ emv = {tree['child_node']['emv']}]",
                  f" ({tree['child_node']['probability']} {tree['child_node']['value']})" if tree['child_node']['type']=='terminal' else '' )


    if 'child_edges' in tree:
        for edge in tree['child_edges']:
            print_tree(edge, level=level+2)
            print_tree(edge['child_node'], level=level+2)


def tree_to_mermaid_chart(tree):
    """
    преобразует дерево в строку пригодную для отображения диаграмм mermaid (https://mermaid.js.org/)
    """
    def get_node_list(tree, nodes=[], i=0):
        """
        рекурсивно вытаскиваем и нумеруем все узлы для отображения
        """
        if tree['type'] == 'terminal':
            snode =  ( "  p = " + str(tree['p']) if 'p' in tree else "")
            snode = snode + ( " <br> v = " + str(tree['v']) if 'v' in tree else "")
            snode = "." if snode=="" else snode
            nodes.append(str(i) +"{"+snode+"}")
            nodes.append("style "+str(i)+"  fill:#00C853")
        if tree['type'] == 'decision':
            snode = tree['name']
            snode = snode + ( " <br> payoff = " + f"{tree['payoff']:.2f}" if 'payoff' in tree else "")
            snode = snode + ( " <br> emv = " + f"{tree['emv']:.2f}" if 'emv' in tree else "")
            snode = snode + ( " <br> voi = " + f"{tree['voi']:.2f}" if 'voi' in tree else "")
            nodes.append(str(i) + "[" +snode+"]")
            nodes.append("style "+str(i)+"  fill:#FF6D00")
        if tree['type'] == 'chance':
            snode = tree['name']
            snode = snode + ( " <br> payoff = " + f"{tree['payoff']:.2f}" if 'payoff' in tree else "")
            snode = snode + ( " <br> p = " + f"{tree['probability']:.2f}" if 'probability' in tree else "")
            snode = snode + ( " <br> emv = " + f"{tree['emv']:.2f}" if 'emv' in tree else "")
            nodes.append(str(i) + "(("+snode+"))")
            nodes.append("style "+str(i)+"  fill:#FFD600")
        tree['_id_'] = i
        i = i + 1
        if 'child_edges' in tree:
            for edge in tree['child_edges']:
                i = get_node_list(edge['child_node'], nodes, i)
        return i

    def get_edge_list(tree, nodes=[]):
        """
        рекурсивно строим связи для всех узлов
        """
        if tree['type'] != 'terminal':
            if 'child_edges' in tree:
                for edge in tree['child_edges']:
                    sedge = edge['name']
                    sedge = sedge + ( " <br> payoff = " + str(edge['payoff']) if 'payoff' in edge else "")
                    sedge = sedge + ( " <br> p = " + str(edge['probability']) if 'probability' in edge else "")
                    
                    nodes.append(str(tree['_id_']) +"--" + sedge +"-->" + str(edge['child_node']['_id_'] ))
                    get_edge_list(edge['child_node'], nodes)
                    
    nodes = ["```mermaid", " flowchart LR"]
    tr = tree.copy()            
    get_node_list(tr, nodes)
    get_edge_list(tr, nodes)
    st=""
    for s in nodes:
        st = st + s + " \n"
    return st
