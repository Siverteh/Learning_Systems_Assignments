import random
import plotly.graph_objects as go

class TsetlinAutomaton:
    def __init__(self, num_automata=5, num_states=10):
        #Set the number of states
        self.num_states = num_states
        #Set the lowest possible state to 0
        self.lowest_state = 0
        #Set the highest possible state to 2 times the number of states - 1
        self.highest_state = (num_states*2)-1
        #Initialize automatas with a random state between lowest no and lowest yes
        self.automata = [{'state': random.randint(num_states -1, num_states), 'yes_count': 0, 'no_count': 0} for _ in range(num_automata)]

    #Function to return wheter the action of the automaton is yes or no based on its state.
    def _get_action(self, automaton):
        """Return the action ('Yes' or 'No') based on the automaton's state."""
        return "Yes" if automaton['state'] >= self.num_states else "No"

    #Function to update the state of the automaton.
    def _update_automaton(self, automaton, reward_probability):
        """Update the automaton's state based on the reward probability."""
        #If the random.random() is lower than the reward probability reward the automaton.
        if random.random() < reward_probability:
            #If the current action is "yes" and the confidence is not at max reward it with +1.
            if self._get_action(automaton) == "Yes" and automaton['state'] < self.highest_state:
                automaton['state'] += 1
            #If the current action is "No" and the confidence is not at max reward it with -1.
            elif self._get_action(automaton) == "No" and automaton['state'] > self.lowest_state:
                automaton['state'] -= 1
        #Else give a penalty to the automaton
        else:
            #If the action is "Yes" decrease the confident by -1.
            if self._get_action(automaton) == "Yes":
                automaton['state'] -= 1
            #If the action is "No" decrease the confident by +1.
            elif self._get_action(automaton) == "No":
                automaton['state'] += 1

        #Update action counts based on new state
        if self._get_action(automaton) == "Yes":
            automaton['yes_count'] += 1
        else:
            automaton['no_count'] += 1

    #Function to print the statistcs for the simulation.
    def _print_statistics(self):
        """Prints the final statistics after the simulation is completed."""
        print("Final Statistics after the simulation:")

        #Loop and print the yes count and reward probability for each iteration.
        for data in self.iteration_data:
            print(f"Iteration: {data['iteration']}, Yes count: {data['yes_count']}, Reward probability: {data['reward_probability']:.1f}")
        print()
        
        #Print the final state, Yes count, and No count for each automaton.
        for i, automaton in enumerate(self.automata):
            print(f"Automaton {i + 1}: Final State = {automaton['state']}, Yes = {automaton['yes_count']}, No = {automaton['no_count']}")
        print()

        # Calculate totals for 'Yes' and 'No' across all iterations
        total_yes_count_all_iterations = sum(automaton['yes_count'] for automaton in self.automata)
        total_no_count_all_iterations = sum(automaton['no_count'] for automaton in self.automata)

        # Calculate averages per iteration
        average_yes_per_iteration = total_yes_count_all_iterations / len(self.iteration_data)
        average_no_per_iteration = total_no_count_all_iterations / len(self.iteration_data)

        # Estimating Nash Equilibrium
        total_decisions = total_yes_count_all_iterations + total_no_count_all_iterations
        yes_probability = total_yes_count_all_iterations / total_decisions
        no_probability = total_no_count_all_iterations / total_decisions

        print("\nEstimated Nash Equilibrium:")
        #Print the probability of "Yes" and the probability of "No"
        print(f"Probability of 'Yes': {yes_probability:.2f}")
        print(f"Probability of 'No': {no_probability:.2f}")
        
        # Print the average number of 'Yes' and 'No' automata per iteration
        print(f"Average number of automata in 'Yes' state per iteration: {average_yes_per_iteration:.2f}")
        print(f"Average number of automata in 'No' state per iteration: {average_no_per_iteration:.2f}")

    def _visualize(self):
        """Generates visualizations for the simulation."""
        # Plot 1: Number of 'Yes' actions over iterations
        fig1 = go.Figure()
        fig1.add_trace(go.Scatter(x=[data['iteration'] for data in self.iteration_data], 
                                  y=[data['yes_count'] for data in self.iteration_data],
                                  mode='lines',
                                  name='Yes Count'))
        fig1.update_layout(title='Number of Yes Actions over Iterations',
                           xaxis_title='Iteration',
                           yaxis_title='Yes Count')
        fig1.show()

        # Plot 2: Reward probabilities over iterations
        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(x=[data['iteration'] for data in self.iteration_data], 
                                  y=[data['reward_probability'] for data in self.iteration_data],
                                  mode='lines',
                                  name='Reward Probability'))
        fig2.update_layout(title='Reward Probability over Iterations',
                           xaxis_title='Iteration',
                           yaxis_title='Reward Probability')
        fig2.show()

    #Function to run the simulation.
    def run_simulation(self, num_iterations: int):
        """Run the Tsetlin Automaton simulation."""

        #Set up lists for storing information about the data for each iteration, yes count history, and reward probabilities.
        self.iteration_data = []
        self.yes_count_history = []
        self.reward_probabilities = []

        #Iterate for the chosen number of iterations.
        for iteration in range(num_iterations):
            
            #Count the current number of yest counts and append them to the yes count history.
            yes_count = sum(1 for automaton in self.automata if self._get_action(automaton) == "Yes")
            self.yes_count_history.append(yes_count)

            #Determine the reward probability based on the number of "Yes" actions and add it to the list of rewards probabilities.
            if yes_count <= 3:
                reward_probability = yes_count * 0.2
            else:
                reward_probability = 0.6 - (yes_count - 3) * 0.2

            self.reward_probabilities.append(reward_probability)

            #Update each automaton based on the reward probability
            for automaton in self.automata:
                self._update_automaton(automaton, reward_probability)

            #Collect iteration data for visualization and statistics.
            self.iteration_data.append({
                'iteration': iteration + 1,
                'yes_count': yes_count,
                'reward_probability': reward_probability
            })

        #Print the final statistics and visualize the results
        self._print_statistics()
        self._visualize()

if __name__ == "__main__":
    # Initialize the Tsetlin Automaton simulation with 5 automata
    tsetlinAutomaton = TsetlinAutomaton(num_automata=5, num_states=30)

    # Run the simulation with 100 iterations
    tsetlinAutomaton.run_simulation(num_iterations=100)
