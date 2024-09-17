from random import random, choice

# Dataset for breast cancer patients
recurrence = [
    {'Menop.=ge40': True, 'Menop.=lt40': False, 'Menop.=premeno': False, 'Inv-nodes=0-2': False, 'Inv-nodes=3-5': True, 'Inv-nodes=6-8': False, 'Deg-malig=3': True, 'Deg-malig=1': False, 'Deg-malig=2': False},
    {'Menop.=ge40': True, 'Menop.=lt40': False, 'Menop.=premeno': False, 'Inv-nodes=0-2': False, 'Inv-nodes=3-5': False, 'Inv-nodes=6-8': True, 'Deg-malig=3': True, 'Deg-malig=1': False, 'Deg-malig=2': False},
    {'Menop.=ge40': False, 'Menop.=lt40': False, 'Menop.=premeno': True, 'Inv-nodes=0-2': True, 'Inv-nodes=3-5': False, 'Inv-nodes=6-8': False, 'Deg-malig=3': True, 'Deg-malig=1': False, 'Deg-malig=2': False}
]


non_recurrence= [
    {'Menop.': 'lt40', 'Inv-nodes': '0-2', 'Deg-malig': 3},
    {'Menop.': 'ge40', 'Inv-nodes': '0-2', 'Deg-malig': 2},
    {'Menop.': 'premeno', 'Inv-nodes': '0-2', 'Deg-malig': 1},
]

def evaluate_condition(observation, condition):
    total = 0
    
    # Rule R1: If Deg-malig = 3 and Menop. != lt40, then recurrence
    if 'Deg-malig=3' in condition and 'NOT Menop.=lt40' in condition:
        if observation['Deg-malig=3'] == True and observation['Menop.=lt40'] != True:
            total += 1
    
    # Rule R2: If Deg-malig = 3, then recurrence
    if 'Deg-malig=3' in condition:
        if observation['Deg-malig=3'] == True:
            total += 1
    
    # Rule R3: If Inv-nodes = 0-2, then non-recurrence
    if 'Inv-nodes=0-2' in condition:
        if observation['Inv-nodes=0-2'] == True:
            total -= 1
    
    # Standard feature evaluation
    truth_value_of_condition = True
    for feature in observation:
        feature_literal = f"{feature}={observation[feature]}"
        
        # Check for positive feature match
        if feature_literal in condition and observation[feature] == False:
            truth_value_of_condition = False
            break
        
        # Check for negated feature match
        if f"NOT {feature_literal}" in condition and observation[feature] == True:
            truth_value_of_condition = False
            break
    
    # If feature checks hold true, return total score
    if truth_value_of_condition or total > 0:
        return True
    else:
        return False  # Indicating a feature mismatch or non-recurrence


class Memory:
    def __init__(self, forget_value, memorize_value, memory):
        self.memory = memory
        self.forget_value = forget_value
        self.memorize_value = memorize_value
    
    def get_memory(self):
        return self.memory
    
    def get_literals(self):
        return list(self.memory.keys())
    
    def get_condition(self):
        condition = []
        for literal in self.memory:
            if self.memory[literal] >= 6:
                condition.append(literal)
        return condition
        
    def memorize(self, literal):
        if random() <= self.memorize_value and self.memory[literal] < 10:
            self.memory[literal] += 1
            
    def forget(self, literal):
        if random() <= self.forget_value and self.memory[literal] > 1:
            self.memory[literal] -= 1
            
    def memorize_always(self, literal):
        if  self.memory[literal] < 10:
            self.memory[literal] += 1

initial_memory = {
    'Menop.=ge40': 5, 'Menop.=lt40': 5, 'Menop.=premeno': 5,
    'Inv-nodes=0-2': 5, 'Inv-nodes=3-5': 5, 'Inv-nodes=6-8': 5,
    'Deg-malig=1': 5, 'Deg-malig=2': 5, 'Deg-malig=3': 5,
    'NOT Menop.=ge40': 5, 'NOT Menop.=lt40': 5, 'NOT Menop.=premeno': 5,
    'NOT Inv-nodes=0-2': 5, 'NOT Inv-nodes=3-5': 5, 'NOT Inv-nodes=6-8': 5,
    'NOT Deg-malig=1': 5, 'NOT Deg-malig=2': 5, 'NOT Deg-malig=3': 5
}

recurrence_rule_memory = Memory(0.8, 0.2, initial_memory.copy())

def type_i_feedback(observation, memory):
    remaining_literals = memory.get_literals()

    if evaluate_condition(observation, memory.get_condition()) == True:
        for feature in observation:
            if observation[feature] == True:
                memory.memorize(feature)
                remaining_literals.remove(feature)
            elif observation[feature] == False:
                memory.memorize('NOT ' + feature)
                remaining_literals.remove('NOT ' + feature)
    for literal in remaining_literals:
        memory.forget(literal)

for i in range(100):
    observation_id = choice([0,1,2])
    type_i_feedback(recurrence[observation_id], recurrence_rule_memory)

print(recurrence_rule_memory.get_memory())

print("IF " + " AND ".join(recurrence_rule_memory.get_condition()) + " THEN Reccurance")