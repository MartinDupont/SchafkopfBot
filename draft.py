# -*- coding: utf-8 -*-
"""
Created on Sun Jul 29 21:20:17 2018

@author: martin
"""

class MCTS(DumbBot):

class Node:
    def __init__(self, state):
        self.Q = 0
        self.N = 0
        self.untried_actions = set(iter(state.actions()))
        self.untried_actions = {} #needs to be set of all cards which have not been ruled out yet. 
        self.children = {}
        self.parent = None
        self.state = state
        self.plausible_hands = {}
        self.p_num
        
    def is_fully_expanded(self):
        if self.untried_actions:
            return False
        return True
   
    def __repr__(self):
        thing = "========== Node ==========\n"
        thing += ("State: "+str(self.state)+"\n")
        thing += "Q: {}, N: {}\n".format(self.Q, self.N)
        thing += "Parent: {} \n".format(id(self.parent))
        thing += "Children: \n"
        for key, value in self.children.items():
            thing += "Action:{}, location: {}\n".format(key, id(value))
        return thing
    
    def print_tree(self):
        def print_util(node, prefix="", depth = 0):
            printstr = ""
            for i in range(depth):
                printstr += "     "
            printstr += "|___"
            printstr += str(prefix)
            printstr += " Q: {}, N: {}\n".format(node.Q, node.N)
            print(printstr)
            for key, value in node.children.items():
                print_util(value, prefix = key, depth = depth+1)
        print_util(self)
        
    def depth(self):
        def depth_util(node, count = 0):
            if node.parent is None:
                return count
            else:
                count += 1
                return depth_util(node.parent, count)
        return depth_util(self)



def generate_plausible_hands(state, hand, my_p_num):
    ### If i have generated plausible hands for one node, then I have plausible
    # hands for the rest of time, right??? Yeah but no. For a node, there may be many
    # contradictory plausible hands. 
    tups = state.player_card_tuples(state.history)
    remaining_cards = set(copy.deepcopy(con.ALL_CARDS))
    n_needed = {i:8 for in [(i+1)%4 for i in range(3)]}
    for p, card in tups:
        remaining_cards.remove(card)
        n_needed[p] -=1
        
    for card in hand:
        remaining_cards.remove(card)
        
    plausible_hands = {i:{} for in [(i+1)%4 for i in range(3)]}
    for key, poss in plausible_hands.items():
        for _ in range(n_needed[key]):
            poss.add(remaining_cards.pop())
    # Dumb plausible hands, doesn't pay attention to who played what. Ignored CSP.
    return plausible_hands


class MonteCarloPlayer(BasePlayer):
    
    def __init__(self, player_id):
        super().__init__()
        self.state_to_node = {}
        self.root_node = None
    
    # -------------------------  
    def tree_policy(self, node):
        while not node.state.terminal_test():
            if not node.is_fully_expanded():
                try:
                    return self.expand_node(node)
                except CannotExpandError:
                    # The node actually IS fully expanded.
                    # This loop will break if one can never generate a single successor
                    continue
                    
            elif node.children(): # if its fully expanded and actually has children.
                node, _ = self.best_child(node)
                
            else:
                # climb back up the tree. 
                new_node = node.parent
                node.parent = None
                del new_node. remove this child
        return node   
    
    def default_policy(self, state):
        p_id = state.player()
        while not state.terminal_test():
            action = random.choice(state.actions())
            state = state.result(action)
        return 1 if state.utility(p_id) < 0 else -1
    
    def back_up(self, node, delta):
        while not(node is None):
            node.N += 1
            node.Q += delta
            delta = -delta
            node = node.parent  
            
    def expand_node(self, input_node):
        while input_node.untried_actions:
            a = input_node.untried_actions.pop()
            new_state = input_node.state.result(a)
            try:
                new = Node(new_state) # try generating plausible hands
                new.parent = input_node
                input_node.children[a] = new
                break
            except:
                continue
        raise CannotExpandError
            
        return new
            
    # ----------------------------------
    def best_child(self, node, c=math.sqrt(2)):
        """ has been checked, is delivering the best children, given the inputs"""
        best_action, best_node = max(node.children.items(),
                          key=lambda x: (x[1].Q / x[1].N) 
                          + (c * math.sqrt(2 * math.log(node.N) / x[1].N)))
        return best_node, best_action
    
    def get_action(self, state):
        if (state.ply_count < 2) or state.terminal_test():
            self.queue.put(random.choice(state.actions()))
        else:
            self.uct_search(state)
        
    def uct_search(self,state):
        #print(state.actions())
        #start = time.time()
        #if True: 
        self.root_node = Node(state)
            
        i=0
        while True:
            #print(i)
            v = self.tree_policy(self.root_node)
            delta = self.default_policy(v.state)
            self.back_up(v, delta)
            node, action = self.best_child(self.root_node, 0)
            self.queue.put(action)
            i+=1
    