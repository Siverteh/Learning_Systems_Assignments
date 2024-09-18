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

    else:
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
    
    print("RECURRENCE MEMORY AFTER TRAINING:") if is_recurrence else print("NON-RECURRENCE MEMORY AFTER TRAINING:")
    print(memory.get_memory())

    print()

    print("RECURRENCE RULE GENERATED:") if is_recurrence else print("NON-RECURRENCE RULE GENERATED:")
    print("IF " + " AND ".join(memory.get_condition()) + " THEN Recurrence") if is_recurrence else print("IF " + " AND ".join(memory.get_condition()) + " THEN Non-Recurrence")

    print()

def train_multiple_runs(memory, dataset1, dataset2, epochs, num_runs=3):
    rule_counts = {literal: 0 for literal in memory.get_literals()}

    for _ in range(num_runs):
        # Reset memory for each run
        current_memory = Memory(memory.forget_value, memory.memorize_value, initial_memory.copy())
        
        for epoch in range(epochs):
            observation_id = choice([0, 1, 2])
            choice_nr = choice([0,1])
            if choice_nr == 1:
                type_i_feedback(dataset1[observation_id], current_memory)
            else:
                type_ii_feedback(dataset2[observation_id], current_memory)
        
        # Determine the general rule based on final memory values
        for literal in current_memory.get_literals():
            if current_memory.get_memory()[literal] >= 6:  # Use threshold of 6 to include in the rule
                rule_counts[literal] += 1

    return rule_counts

# Plot the general rule using a bubble chart
def plot_bubble_chart(general_rules, values, literals, title):
    plt.figure(figsize=(10, 6))
    
    for i, value in enumerate(values):
        x = [i] * len(literals)  # x-axis is for each combination of memorize/forget values
        y = np.arange(len(literals))  # y-axis is for each literal (feature)
        sizes = [general_rules[i][literal] * 100 for literal in literals]  # Size of bubbles corresponds to rule inclusion count
        
        plt.scatter(x, y, s=sizes, alpha=0.5, label=f'Mem: {value[1]}, Forget: {value[0]}')
    
    plt.xticks(range(len(values)), [f'Mem: {v[1]}, Forget: {v[0]}' for v in values], rotation=45)
    plt.yticks(range(len(literals)), literals)
    plt.xlabel('Memorize/Forget Values')
    plt.ylabel('Features (Literals)')
    plt.title(f'General Rule Formation - {title}')
    plt.legend(loc='upper right')
    plt.grid(True)
    plt.tight_layout()
    plt.show()


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
    
def run_manual_classification():
    print("MANUAL CLASSIFICATION USING RULES R1, R2, and R3:")
    manual_classify(recurrences)
    manual_classify(non_recurrences)
    print()

def run_training_with_visualization(forget: float, memoize: float):
    recurrence_rule_memory = Memory(forget, memoize, initial_memory.copy())
    non_recurrence_rule_memory = Memory(forget, memoize, initial_memory.copy())
    train(recurrence_rule_memory, recurrences, non_recurrences, epochs=500, is_recurrence=True, visualize=True)
    train(non_recurrence_rule_memory, non_recurrences, recurrences, epochs=500, is_recurrence=False, visualize=True)

def run_training_with_classification(forget: float, memoize: float):
    recurrence_rule_memory = Memory(forget, memoize, initial_memory.copy())
    non_recurrence_rule_memory = Memory(forget, memoize, initial_memory.copy())
    train(recurrence_rule_memory, recurrences, non_recurrences, epochs=500, is_recurrence=True, visualize=False)
    train(non_recurrence_rule_memory, non_recurrences, recurrences, epochs=500, is_recurrence=False, visualize=False)
    print("Classifying Recurrence Dataset:")
    for i, patient in enumerate(recurrences):
        result = classify(patient, [recurrence_rule_memory], [non_recurrence_rule_memory])
        print(f"Patient {i + 1} in Recurrence Dataset: {result}")
    print("\nClassifying Non-Recurrence Dataset:")
    for i, patient in enumerate(non_recurrences):
        result = classify(patient, [recurrence_rule_memory], [non_recurrence_rule_memory])
        print(f"Patient {i + 1} in Non-Recurrence Dataset: {result}")

def run_training_with_bubble_graph():
    values = [[0.8, 0.2], [0.5, 0.5], [0.2, 0.8]]

    recurrence_general_rules = []
    non_recurrence_general_rules = []

    for value in values:
        # Initialize memory
        recurrence_rule_memory = Memory(value[0], value[1], initial_memory.copy())
        non_recurrence_rule_memory = Memory(value[0], value[1], initial_memory.copy())
        
        # Run multiple trainings and get the general rule
        recurrence_general_rule = train_multiple_runs(recurrence_rule_memory, recurrences, non_recurrences, epochs=100, num_runs=10)
        non_recurrence_general_rule = train_multiple_runs(non_recurrence_rule_memory, non_recurrences, recurrences, epochs=100, num_runs=10)
        
        recurrence_general_rules.append(recurrence_general_rule)
        non_recurrence_general_rules.append(non_recurrence_general_rule)

    # Get the literals (features) for plotting
    literals = recurrence_rule_memory.get_literals()

    # Plot the bubble chart for recurrence rules
    plot_bubble_chart(recurrence_general_rules, values, literals, title="Recurrence Rule Generalization")

    # Plot the bubble chart for non-recurrence rules
    plot_bubble_chart(non_recurrence_general_rules, values, literals, title="Non-Recurrence Rule Generalization")

if __name__ == "__main__":
    """MANUAL CLASSIFICATION"""
    #run_manual_classification()

    """TRAINING WITH VISUALIZATION"""
    #run_training_with_visualization(forget=0.8, memoize=0.2)

    """TRAINING WITH CLASSIFICATION"""
    #run_training_with_classification(forget=0.8, memoize=0.2)
    
    """TRAINING WITH BUBBLE GRAPH"""
    run_training_with_bubble_graph()
    