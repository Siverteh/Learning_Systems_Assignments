from random import random, choice

# Dataset for breast cancer patients
data = [
    {'Menop.': 'ge40', 'Inv-nodes': '3-5', 'Deg-malig': 3, 'Recur.': 'yes'},
    {'Menop.': 'lt40', 'Inv-nodes': '0-2', 'Deg-malig': 3, 'Recur.': 'no'},
    {'Menop.': 'ge40', 'Inv-nodes': '6-8', 'Deg-malig': 3, 'Recur.': 'yes'},
    {'Menop.': 'ge40', 'Inv-nodes': '0-2', 'Deg-malig': 2, 'Recur.': 'no'},
    {'Menop.': 'premeno', 'Inv-nodes': '0-2', 'Deg-malig': 3, 'Recur.': 'yes'},
    {'Menop.': 'premeno', 'Inv-nodes': '0-2', 'Deg-malig': 1, 'Recur.': 'no'}
]

# Function to evaluate conditions
def evaluate_condition(observation, condition):
    truth_value_of_condition = True
    for feature in observation:
        literal = f"{feature}={observation[feature]}"
        if literal in condition and observation[feature] == False:
            truth_value_of_condition = False
            break
        if f"NOT {literal}" in condition and observation[feature] == True:
            truth_value_of_condition = False
            break
    return truth_value_of_condition

# Class for memory management (rules learning)
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
        if literal not in self.memory:
            return
        if random() <= self.memorize_value and self.memory[literal] < 10:
            self.memory[literal] += 1
            
    def forget(self, literal):
        if literal not in self.memory:
            return
        if random() <= self.forget_value and self.memory[literal] > 1:
            self.memory[literal] -= 1
            
    def memorize_always(self, literal):
        if literal not in self.memory:
            return
        if self.memory[literal] < 10:
            self.memory[literal] += 1

# Initializing memory for Recurrence and Non-Recurrence
recurrence_rule = Memory(0.5, 0.5, {
    'Deg-malig=3': 5, 'NOT Deg-malig=3': 5, 
    'Menop.=ge40': 5, 'NOT Menop.=ge40': 5, 
    'Inv-nodes=0-2': 5, 'NOT Inv-nodes=0-2': 5,
    'Inv-nodes=3-5': 5, 'NOT Inv-nodes=3-5': 5
})

non_recurrence_rule = Memory(0.5, 0.5, {
    'Inv-nodes=0-2': 5, 'NOT Inv-nodes=0-2': 5,
    'Deg-malig=3': 5, 'NOT Deg-malig=3': 5,
    'Menop.=lt40': 5, 'NOT Menop.=lt40': 5
})

# Type I feedback: learning positive rules
def type_i_feedback(observation, memory):
    remaining_literals = memory.get_literals()
    condition = memory.get_condition()
    if evaluate_condition(observation, condition) == True:
        for feature in observation:
            feature_literal = f"{feature}={observation[feature]}"
            if feature_literal in memory.get_literals():
                memory.memorize(feature_literal)
                if feature_literal in remaining_literals:
                    remaining_literals.remove(feature_literal)
            neg_literal = f"NOT {feature_literal}"
            if neg_literal in memory.get_literals() and observation[feature] == False:
                memory.memorize(neg_literal)
                if neg_literal in remaining_literals:
                    remaining_literals.remove(neg_literal)
    for literal in remaining_literals:
        memory.forget(literal)

# Type II feedback: learning negative rules
def type_ii_feedback(observation, memory):
    condition = memory.get_condition()
    if evaluate_condition(observation, condition) == True:
        for feature in observation:
            feature_literal = f"{feature}={observation[feature]}"
            if observation[feature] == False:
                neg_literal = f"NOT {feature_literal}"
                memory.memorize_always(neg_literal)
            else:
                memory.memorize_always(feature_literal)

# Training with a mix of Type I and Type II feedback
for i in range(1000):
    observation_id = choice(range(len(data)))
    observation = data[observation_id]
    
    if observation['Recur.'] == 'yes':
        type_i_feedback(observation, recurrence_rule)
    else:
        type_ii_feedback(observation, non_recurrence_rule)

# Displaying the learned rules
print("Recurrence Rule Memory:", recurrence_rule.get_memory())
print("Non-Recurrence Rule Memory:", non_recurrence_rule.get_memory())

print("IF " + " AND ".join(recurrence_rule.get_condition()) + " THEN Recurrence")
print("IF " + " AND ".join(non_recurrence_rule.get_condition()) + " THEN Non-Recurrence")

# Function to classify a new observation
def classify(observation, recurrence_rule, non_recurrence_rule):
    vote_sum = 0
    if evaluate_condition(observation, recurrence_rule.get_condition()):
        vote_sum += 1
    if evaluate_condition(observation, non_recurrence_rule.get_condition()):
        vote_sum -= 1
    return "Recurrence" if vote_sum > 0 else "Non-recurrence"

# Classifying the dataset
for patient in data:
    print(f"Patient: {patient}, Classification: {classify(patient, recurrence_rule, non_recurrence_rule)}")
