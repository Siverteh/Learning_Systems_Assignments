from random import random, choice

# Dataset for breast cancer patients
recurrences = [
    {'Menopause=ge40': True, 'Menopause=lt40': False, 'Menopause=premeno': False, 'Inv-nodes=0-2': False, 'Inv-nodes=3-5': True, 'Inv-nodes=6-8': False, 'Deg-malig=3': True, 'Deg-malig=1': False, 'Deg-malig=2': False},
    {'Menopause=ge40': True, 'Menopause=lt40': False, 'Menopause=premeno': False, 'Inv-nodes=0-2': False, 'Inv-nodes=3-5': False, 'Inv-nodes=6-8': True, 'Deg-malig=3': True, 'Deg-malig=1': False, 'Deg-malig=2': False},
    {'Menopause=ge40': False, 'Menopause=lt40': False, 'Menopause=premeno': True, 'Inv-nodes=0-2': True, 'Inv-nodes=3-5': False, 'Inv-nodes=6-8': False, 'Deg-malig=3': True, 'Deg-malig=1': False, 'Deg-malig=2': False},
    {'Menopause=ge40': False, 'Menopause=lt40': True, 'Menopause=premeno': False, 'Inv-nodes=0-2': True, 'Inv-nodes=3-5': False, 'Inv-nodes=6-8': False, 'Deg-malig=3': True, 'Deg-malig=1': False, 'Deg-malig=2': False},
]


non_recurrences = [
    
    {'Menopause=ge40': True, 'Menopause=lt40': False, 'Menopause=premeno': False, 'Inv-nodes=0-2': True, 'Inv-nodes=3-5': False, 'Inv-nodes=6-8': False, 'Deg-malig=3': False, 'Deg-malig=1': False, 'Deg-malig=2': True},
    {'Menopause=ge40': False, 'Menopause=lt40': False, 'Menopause=premeno': True, 'Inv-nodes=0-2': True, 'Inv-nodes=3-5': False, 'Inv-nodes=6-8': False, 'Deg-malig=3': False, 'Deg-malig=1': True, 'Deg-malig=2': False},
]

def evaluate_condition(observation, condition):
    # Standard feature evaluation
    truth_value_of_condition = True
    for feature in observation:
        # Check for positive feature match
        if feature in condition and observation[feature] == False:
            truth_value_of_condition = False
            break
        
        # Check for negated feature match
        if f"NOT {feature}" in condition and observation[feature] == True:
            truth_value_of_condition = False
            break
    # If feature checks hold true, return total score
    if truth_value_of_condition:
        return True
    else:
        return False  # Indicating a feature mismatch or non-recurrence
    
# Define your rules R1, R2, R3
R1 = {'Deg-malig=3', 'NOT Menopause=lt40'}  # Example rule
R2 = {'Deg-malig=3'}  # Example rule
R3 = {'Inv-nodes=0-2'}  # Example rule

# Combine both recurrences and non-recurrences into a single list
all_patients = [
    {'data': patient, 'label': 'Recurrence'} for patient in recurrences] + [
    {'data': patient, 'label': 'Non-Recurrence'} for patient in non_recurrences
]

# Loop through all patients, both recurrences and non-recurrences
for patient_info in all_patients:
    patient = patient_info['data']
    true_label = patient_info['label']
    
    count = 0

    # Evaluate rules
    if evaluate_condition(patient, R1):
        count += 1

    if evaluate_condition(patient, R2):
        count += 1

    if evaluate_condition(patient, R3):
        count -= 1
    
    # Classification based on the count
    classification = "Recurrence" if count >= 0 else "Non-Recurrence"
    
    # Print the patient data and classification result
    print(f"Patient: {patient}")
    print(f"True Label: {true_label}")
    print(f"Classified as: {classification}\n")



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
        if self.memory[literal] < 10:
            self.memory[literal] += 1

initial_memory = {
    'Menopause=ge40': 5, 'Menopause=lt40': 5, 'Menopause=premeno': 5,
    'Inv-nodes=0-2': 5, 'Inv-nodes=3-5': 5, 'Inv-nodes=6-8': 5,
    'Deg-malig=1': 5, 'Deg-malig=2': 5, 'Deg-malig=3': 5,
    'NOT Menopause=ge40': 5, 'NOT Menopause=lt40': 5, 'NOT Menopause=premeno': 5,
    'NOT Inv-nodes=0-2': 5, 'NOT Inv-nodes=3-5': 5, 'NOT Inv-nodes=6-8': 5,
    'NOT Deg-malig=1': 5, 'NOT Deg-malig=2': 5, 'NOT Deg-malig=3': 5
}

recurrence_rule_memory = Memory(0.8, 0.2, initial_memory.copy())
non_recurrence_rule_memory = Memory(0.8, 0.2, initial_memory.copy())


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

def type_ii_feedback(observation, memory):
    if evaluate_condition(observation, memory.get_condition()) == True:
        for feature in observation:
            if observation[feature] == False:
                memory.memorize_always(feature)
            elif observation[feature] == True:
                memory.memorize_always('NOT ' + feature)

for i in range(100):
    
    is_reccurence = choice([0,1])
    if is_reccurence == 1:
        observation_id = choice([0,1,2,3])
        type_i_feedback(recurrences[observation_id], recurrence_rule_memory)
    else:
        observation_id = choice([0,1])
        type_ii_feedback(non_recurrences[observation_id], recurrence_rule_memory)

for i in range(100):
    is_reccurence = choice([0,1])
    if is_reccurence == 1:
        observation_id = choice([0,1])
        type_i_feedback(non_recurrences[observation_id], non_recurrence_rule_memory)
    else:
        observation_id = choice([0,1,2,3])
        type_ii_feedback(recurrences[observation_id], non_recurrence_rule_memory)


print(recurrence_rule_memory.get_memory())

print()

print("IF " + " AND ".join(recurrence_rule_memory.get_condition()) + " THEN Reccurance")

print('\n----------------------------------------------------------------------------------------\n')

print(non_recurrence_rule_memory.get_memory())

print()

print("IF " + " AND ".join(non_recurrence_rule_memory.get_condition()) + " THEN Non-Reccurance")

print()

def classify(observation, recurrence_rules, non_recurrence_rules):
    vote_sum = 0
    for recurrence_rule in recurrence_rules:
        if evaluate_condition(observation, recurrence_rule.get_condition()) == True:
            vote_sum += 1
    for non_recurrence_rule in non_recurrence_rules:
        if evaluate_condition(observation, non_recurrence_rule.get_condition()) == True:
            vote_sum -= 1
    if vote_sum >= 0:
        return "Recurrence"
    else:
        return "Non-Recurrence"
    
# Classify all the patients in the recurrence and non-recurrence datasets
print("Classifying Recurrence Dataset:")
for i, patient in enumerate(recurrences):
    result = classify(patient, [recurrence_rule_memory], [non_recurrence_rule_memory])
    print(f"Patient {i + 1} in Recurrence Dataset: {result}")

print("\nClassifying Non-Recurrence Dataset:")
for i, patient in enumerate(non_recurrences):
    result = classify(patient, [recurrence_rule_memory], [non_recurrence_rule_memory])
    print(f"Patient {i + 1} in Non-Recurrence Dataset: {result}")
