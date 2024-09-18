import matplotlib
matplotlib.use('TkAgg')  # For non-GUI backends in scripts
import matplotlib.pyplot as plt
import numpy as np
from random import random, choice
from dataset import recurrences, non_recurrences, initial_memory, R1, R2, R3
import matplotlib.animation as animation

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

def manual_classify(patients: list):
    for patient in patients:
        count = 0
        if evaluate_condition(patient, R1):
            count += 1
        if evaluate_condition(patient, R2):
            count += 1
        if evaluate_condition(patient, R3):
            count -= 1
        classification = "Recurrence" if count > 0 else "Non-Recurrence"
        print(f"Patient: {patient}")
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


# Dynamic visualization function using plt.pause()
def train(memory: Memory, dataset1: list[dict], dataset2: list[dict], epochs: int, is_recurrence: bool, visualize: bool):

    if not visualize:
        for _ in range(epochs):
            # Simulate memory updates (Training loop here)
            observation_id = choice([0, 1, 2])
            choice_nr = choice([0, 1])
            if choice_nr == 1:
                type_i_feedback(dataset1[observation_id], memory)
            else:
                type_ii_feedback(dataset2[observation_id], memory)
        return

    # Setup the plot
    fig, ax = plt.subplots(figsize=(10, 6))
    literals = memory.get_literals()
    x_positions = np.arange(len(literals))  # Positions for each feature on x-axis
    y_values = [memory.get_memory()[literal] for literal in literals]  # Initial memory values
    scatter = ax.scatter(x_positions, y_values)  # Scatter plot of feature memory values

    ax.set_title('Feature Memory Values Moving Up/Down Over Epochs')
    ax.set_xlabel('Features')
    ax.set_ylabel('Memory Value (0-10)')
    ax.set_ylim(0, 10)
    ax.set_xticks(x_positions)
    ax.set_xticklabels(literals, rotation=45, ha='right')
    ax.grid(True)

    # Update the plot after each epoch
    for _ in range(epochs):
        # Simulate memory updates (Training loop here)
        observation_id = choice([0, 1, 2])
        choice_nr = choice([0, 1])
        if choice_nr == 1:
            type_i_feedback(dataset1[observation_id], memory)
        else:
            type_ii_feedback(dataset2[observation_id], memory)

        # Update y-values with the latest memory values
        y_values = [memory.get_memory()[literal] for literal in literals]
        scatter.set_offsets(np.c_[x_positions, y_values])  # Update scatter plot positions
        plt.pause(0.1)  # Pause to allow the plot to update

    plt.show()
    
    print(memory.get_memory())

    print()

    print("IF " + " AND ".join(memory.get_condition()) + " THEN Recurrence") if is_recurrence else print("IF " + " AND ".join(memory.get_condition()) + " THEN Non-Recurrence")

    print('\n----------------------------------------------------------------------------------------\n')


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

if __name__ == "__main__":
    #Manual classification
    print("MANUAL CLASSIFICATION USING RULES R1, R2, and R3:")
    manual_classify(recurrences)
    manual_classify(non_recurrences)
    print()

    #Set up rules:
    recurrence_rule_memory = Memory(0.8, 0.2, initial_memory.copy())
    non_recurrence_rule_memory = Memory(0.8, 0.2, initial_memory.copy())

    #Training for recurrence rule with visualization:
    train(recurrence_rule_memory, recurrences, non_recurrences, epochs=500, is_recurrence=True, visualize=True)
    
    train(non_recurrence_rule_memory, non_recurrences, recurrences, epochs=500, is_recurrence=False, visualize=True)


    #Classification using learned rule:
    print("Classifying Recurrence Dataset:")
    for i, patient in enumerate(recurrences):
        result = classify(patient, [recurrence_rule_memory], [non_recurrence_rule_memory])
        print(f"Patient {i + 1} in Recurrence Dataset: {result}")

    print("\nClassifying Non-Recurrence Dataset:")
    for i, patient in enumerate(non_recurrences):
        result = classify(patient, [recurrence_rule_memory], [non_recurrence_rule_memory])
        print(f"Patient {i + 1} in Non-Recurrence Dataset: {result}")