from Agent import Agent
from SociallyMotivatedAgent import SMagent
from Message import Message
import numpy as np
import pandas as pd
from Simulation import Simulation, SimulationSociallyMotivatedEnvironment
from Simulation import SimulationEgoistsEnvironment, SimulationAltruistsEnvironment
import openpyxl
from Data import Data, SimulationData, AllSimulationData
import copy

final_iteration = 1000


def analysis_save_to_excel(sim):
    simulations_data = pd.DataFrame(sim.simulations_mean_data)
    equality_data = pd.DataFrame(sim.equality_data)
    xlName = "All_Simulation.xlsx"
    xlwriter = pd.ExcelWriter(xlName)
    simulations_data.to_excel(xlwriter, sheet_name='all simulations analysis', index=False)
    equality_data.to_excel(xlwriter, sheet_name='equality analysis', index=False)
    xlwriter.close()


# ----------------------------------------------------------------------------------------------------------
def neighbours2agent(neighbours, agents, agent_id):
    send = {}
    # neighbours_id is list of neighbours id
    neighbours_id = neighbours[agent_id]
    for neighbour_id in neighbours_id:
        # { key: id, value: neighbour}
        send[neighbour_id] = agents[neighbour_id]
    return send


def constraints2agent(constraints, agent_id):
    return constraints[agent_id]


def get_agent(agents, agent_id):
    return agents[agent_id]


# ----------------------------------------------------------------------------------------------------------
def simulation_same_type_run(id, simulation_data, agent_type, agents, neighbours, constraints):
    data = Data()  # save data here
    data.set_neighbours_data(neighbours)  # update data - save connections
    for agent_id in agents.keys():
        # for every agent - initiate
        a_neighbours = neighbours2agent(neighbours, agents, agent_id)
        a_constraints = constraints2agent(constraints, agent_id)
        agent = get_agent(agents, agent_id)
        agent.initiate(a_neighbours, a_constraints)
    # start running the algorithm
    i = 0
    while i < final_iteration:
        up = False
        for agent_id in agents.keys():
            agent = get_agent(agents, agent_id)
            agent.listen()
        for agent_id in agents.keys():
            agent = get_agent(agents, agent_id)
            agent.reply()
            if agent.phase == 4:
                data.update_data(agent.get_data())  # save data here
                up = True
        if up:
            i = i + 1
    # save_to_excel(id, data, "Simulation"+agent_type )
    simulation_data.update_data(data, agent_type)


# _________________________________________________________________________________________________________________
def simulation_environment(id):
    sEgo = SimulationEgoistsEnvironment(id, 50, 10, 35)
    sAltru = SimulationAltruistsEnvironment(id, 50, 10, 35)
    sSoci = SimulationSociallyMotivatedEnvironment(id, 50, 10, 35)
    # --------------------------------------------same seed
    Egoagents = sEgo.create_agents()
    Altruagents = sAltru.create_agents()
    Sociagents = sSoci.create_agents()
    neighbours = sEgo.create_connections()
    constraints = sEgo.create_constraints()
    # --------------------------------------------DATA
    simulation_data = SimulationData()
    # --------------------------------------------RUN
    simulation_same_type_run(id, simulation_data, "Egoist", copy.deepcopy(Egoagents), copy.deepcopy(neighbours),
                             copy.deepcopy(constraints))
    simulation_same_type_run(id, simulation_data, "Socially Motivated", copy.deepcopy(Sociagents),
                             copy.deepcopy(neighbours),
                             copy.deepcopy(constraints))
    simulation_same_type_run(id, simulation_data, "Altruist", copy.deepcopy(Altruagents), copy.deepcopy(neighbours),
                             copy.deepcopy(constraints))
    # --------------------------------------------Analysis
    # simulation_save_to_excel(id, simulation_data)
    print("id:", id)
    return simulation_data


# ******************************************************************************************************
def run_simulations(how_many):
    sim_data = []
    for index in range(0, how_many):
        sim_data.append(simulation_environment(index))
    all_simulation_data_analysis = AllSimulationData(sim_data)
    all_simulation_data_analysis.update_data()
    analysis_save_to_excel(all_simulation_data_analysis)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    run_simulations(50)
