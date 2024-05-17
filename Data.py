from statistics import mean


class Data:
    def __init__(self):
        self.utility_data = {}
        self.agent_data = {'Iteration': [], 'ID': [], 'Assignment': [], 'Utility': []}
        self.neighbours_data = {'ID': [], 'neighbours': []}
        self.global_utility_data = {'Iteration': [], 'Global Utility': []}
        self.any_time_data = {'Iteration': [], 'Best Global Utility': []}
        # ------------------------------------------helper for calculations:
        self.total_agents = 0
        self.best_global_iteration = 0  # when global utility is max

    def set_neighbours_data(self, data):
        for agent_id in data.keys():
            self.neighbours_data['ID'].append(agent_id)
            self.neighbours_data['neighbours'].append(data[agent_id])
        self.total_agents = len(data)
        # ---------------------------------------------------------------------update num agents for utility_data cols
        for agent_id in data.keys():
            self.utility_data[agent_id] = []

    def update_data(self, data):
        # Iteration, ID, Assignment, Utility
        iteration = data[0]
        id = data[1]
        assignment = data[2]
        utility = data[3]
        # ------------------------------------------------------------------------agent_data
        self.agent_data['Iteration'].append(iteration)
        self.agent_data['ID'].append(id)
        self.agent_data['Assignment'].append(assignment)
        self.agent_data['Utility'].append(utility)
        # ------------------------------------------------------------------------utility_data
        self.utility_data[id].append(utility)
        # ------------------------------------------------------------------------global_utility_data
        if id == (self.total_agents - 1):
            self.global_utility_data['Iteration'].append(iteration)
            global_uti = 0
            for agent_id in range(self.total_agents):
                global_uti += self.utility_data[agent_id][-1]
            self.global_utility_data['Global Utility'].append(global_uti)
            if iteration == 0:
                self.any_time_data['Iteration'].append(iteration)
                self.any_time_data['Best Global Utility'].append(global_uti)
            # ------------------------------------------------------------------------any_time_data
            elif global_uti >= max(self.any_time_data['Best Global Utility']):
                self.any_time_data['Iteration'].append(iteration)
                self.best_global_iteration = iteration
                self.any_time_data['Best Global Utility'].append(global_uti)
            else:
                self.any_time_data['Iteration'].append(iteration)
                self.any_time_data['Best Global Utility'].append(self.any_time_data['Best Global Utility'][-1])


# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

class SimulationData:
    def __init__(self):
        self.simulation_data = {'Altruist - Global': [], 'Egoist - Global': [], 'SM - Global': [],
                                'Altruist - AnyTime': [], 'Egoist - AnyTime': [], 'SM - AnyTime': []}
        self.equality_data = {'Altruists': [], 'Egoists': [], 'SociallyMotivated': []}

    def update_data(self, data, agent_type):
        best_iteration = data.best_global_iteration
        if agent_type == 'Altruist':
            self.simulation_data['Altruist - Global'].extend(data.global_utility_data['Global Utility'])
            self.simulation_data['Altruist - AnyTime'].extend(data.any_time_data['Best Global Utility'])
            for agent_id in range(data.total_agents):
                self.equality_data['Altruists'].append(data.utility_data[agent_id][best_iteration])
            self.equality_data['Altruists'].sort()
        elif agent_type == 'Egoist':
            self.simulation_data['Egoist - Global'].extend(data.global_utility_data['Global Utility'])
            self.simulation_data['Egoist - AnyTime'].extend(data.any_time_data['Best Global Utility'])
            for agent_id in range(data.total_agents):
                self.equality_data['Egoists'].append(data.utility_data[agent_id][best_iteration])
            self.equality_data['Egoists'].sort()
        elif agent_type == 'Socially Motivated':
            self.simulation_data['SM - Global'].extend(data.global_utility_data['Global Utility'])
            self.simulation_data['SM - AnyTime'].extend(data.any_time_data['Best Global Utility'])
            for agent_id in range(data.total_agents):
                self.equality_data['SociallyMotivated'].append(data.utility_data[agent_id][best_iteration])
            self.equality_data['SociallyMotivated'].sort()


# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
class AllSimulationData:
    def __init__(self, sims_list):
        self.simulations_list_data = {'Altruist - Global': [], 'Egoist - Global': [], 'SM - Global': [],
                                      'Altruist - AnyTime': [], 'Egoist - AnyTime': [], 'SM - AnyTime': []}
        self.simulations_mean_data = {'Altruist - Global': [], 'Egoist - Global': [], 'SM - Global': [],
                                      'Altruist - AnyTime': [], 'Egoist - AnyTime': [], 'SM - AnyTime': []}
        self.equality_calculations = {'Altruists': [], 'Egoists': [], 'SociallyMotivated': []}
        self.equality_data = {'Population': [], 'Altruists': [], 'Egoists': [], 'SociallyMotivated': [],
                              'Cumulative % Population': [], '% Altruists-income': [], '% Egoists-income': [],
                              '% SociallyMotivated-income': []}
        self.all_simulations = sims_list
        # ---------------------------------------------------------------------------------------------helpers
        self.titles = ['Altruist - Global', 'Altruist - AnyTime', 'Egoist - Global', 'Egoist - AnyTime', 'SM - Global',
                       'SM - AnyTime']
        self.titles_income = ['Altruists', 'Egoists', 'SociallyMotivated']
        self.num_iterations = 1000
        self.num_agents = 50

    def update_data(self):
        for title in self.titles:
            for row in range(self.num_iterations):
                self.simulations_list_data[title].append([])
                self.simulations_list_data[title][row] = []
        for title in self.titles:
            for data in self.all_simulations:
                for row in range(self.num_iterations):
                    cell = data.simulation_data[title][row]
                    self.simulations_list_data[title][row].append(cell)
        for title in self.titles:
            for row in range(self.num_iterations):
                list_cell = self.simulations_list_data[title][row]
                mean_cell = mean(list_cell)
                self.simulations_mean_data[title].append(mean_cell)
        # __________________________________________________________________________Population
        for index in range(0, self.num_agents + 1):
            self.equality_data['Population'].append(index)
        # __________________________________________________________________________Income - sorted
        for title in self.titles_income:
            for agent_num in range(self.num_agents):
                self.equality_calculations[title].append([])
                self.equality_calculations[title][agent_num] = []
        for title in self.titles_income:
            for data in self.all_simulations:
                for agent_num in range(0, self.num_agents):
                    cell = data.equality_data[title][agent_num]
                    self.equality_calculations[title][agent_num].append(cell)
        for title in self.titles_income:
            self.equality_data[title].append(0)
            for agent_num in range(self.num_agents):
                list_cell = self.equality_calculations[title][agent_num]
                mean_cell = mean(list_cell)
                self.equality_data[title].append(mean_cell)
        # __________________________________________________________________________% Population
        for index in range(0, self.num_agents + 1):
            self.equality_data['Cumulative % Population'].append((index / self.num_agents) * 100)
        # __________________________________________________________________________% Income - sorted
        sum_income_altruists = self.simulations_mean_data['Altruist - AnyTime'][-1]
        sum_income_egoists = self.simulations_mean_data['Egoist - AnyTime'][-1]
        sum_income_sm = self.simulations_mean_data['SM - AnyTime'][-1]
        for index in range(0, self.num_agents + 1):
            self.equality_data['% Altruists-income'].append(
                (self.equality_data['Altruists'][index] / sum_income_altruists) * 100)
            self.equality_data['% Egoists-income'].append(
                (self.equality_data['Egoists'][index] / sum_income_egoists) * 100)
            self.equality_data['% SociallyMotivated-income'].append(
                (self.equality_data['SociallyMotivated'][index] / sum_income_sm) * 100)
