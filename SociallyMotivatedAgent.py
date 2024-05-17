from Agent import Agent
import math
import random
from Message import Message
import numpy as np


class SMagent(Agent):
    def __init__(self, id, domainSize, bound, privacyLevel=1):
        Agent.__init__(self, id, domainSize, privacyLevel)
        self.baseLine = 0
        self.bound = bound

    def __str__(self):
        s = "I am a Socially Motivated agent, ID: " + str(self.id) + ", utility: " + str(self.utility) + ", baseLine: " \
            + str(self.baseLine) + ", bound:  " + str(self.bound)
        return s

    # DATA
    def get_data(self):
        # Iteration, Assignment, Utility, None, baseLine, bound
        data = [self.iteration, self.id, self.assignment, self.utility]
        return data

    # _____________________________________________________________________________PRIVET METHODS:
    # PHASE 1
    def update_base_line(self):
        base_line = (self.baseLine + self.utility) / 2
        self.baseLine = base_line

    # PHASE 2
    def calculate_next_assignment(self, indications):
        vote_list = [0] * self.domainSize
        gain_list = [0] * self.domainSize
        # __________________________________________neighbours pref
        for neighbour_id in self.neighbours:
            pref_list = indications[neighbour_id]  # assignment num
            for option in range(len(pref_list)):
                gain_list[option] = gain_list[option] + pref_list[option]
            vote = np.argmax(pref_list)
            vote_list[vote] = vote_list[vote] + 1
        # __________________________________________my pref
        criterion = -math.inf
        my_pref = self.assignment
        for assignment in range(self.domainSize):
            utility = self.calculate_utility(assignment)
            gain_list[assignment] = gain_list[assignment] + utility
            if utility > criterion:
                criterion = utility
                my_pref = assignment
        vote_list[my_pref] = vote_list[my_pref] + 1
        # __________________________________________analyze
        probability_list = np.array(vote_list) / (len(self.neighbours)+1)
        expectation_list = probability_list * np.array(gain_list)
        alter = np.argmax(expectation_list)
        self.alterValue = alter

    # PHASE 3
    def calculate_threshold(self, alternative_values):
        self.taboos = {}
        for neighbour_id in alternative_values:
            neighbour_alter_value = alternative_values[neighbour_id]
            perm_uti = self.only_one_change_assignment(neighbour_id)
            constraint_matrix_with_n = self.constraints[neighbour_id]
            new_uti = constraint_matrix_with_n[self.assignment][neighbour_alter_value]
            potential_utility = perm_uti + new_uti
            if potential_utility < (self.baseLine - self.baseLine * self.bound):
                content = neighbour_alter_value
                sender = self.id
                receiver = neighbour_id
                msg = Message(sender, receiver, content)
                self.taboos[neighbour_id] = msg

    # PHASE 4
    def change_assignment(self):
        self.assignment = self.alterValue

    # _____________________________________________________________________________ALGORITHM:

    def listen(self):
        if self.phase == 1:
            self.listen_phase_1()
        elif self.phase == 2:
            self.listen_phase_2()
        elif self.phase == 3:
            self.listen_phase_3()
        elif self.phase == 4:
            self.listen_phase_4()

    def reply(self):
        if self.phase == 1:
            self.reply_phase_1()
        elif self.phase == 2:
            self.reply_phase_2()
        elif self.phase == 3:
            self.reply_phase_3()
        elif self.phase == 4:
            self.reply_phase_4()

        # ______________________________________initiate:

    def initiate(self, neighbours, constraints):
        self.init_neighbours(neighbours)
        self.init_constraints(constraints)
        self.init_domain()
        messages_to_send = self.make_value_messages()
        self.send_messages(messages_to_send)
        self.phase = 1

        # ________________________________________________________PHASE 1

    def listen_phase_1(self):
        # update local view
        for msg in self.message_box:
            self.LocalView[msg.get_sender()] = msg.get_content()  # content = neighbor's assignment
        self.clear_message_box()
        # update utility
        self.utility = self.calculate_utility(self.assignment)
        self.update_base_line()

    def reply_phase_1(self):
        # send preferences to all neighbors
        messages_to_send = self.make_pref_messages()
        self.send_messages(messages_to_send)
        self.phase = 2

        # ________________________________________________________PHASE 2

    def listen_phase_2(self):
        # update indications
        indications = {}
        for msg in self.message_box:
            indications[msg.get_sender()] = msg.get_content()  # content = neighbor's list pref
        self.clear_message_box()
        # look for next assignment
        self.calculate_next_assignment(indications)

    def reply_phase_2(self):
        # send social_gain and alter_value to all neighbors
        messages_to_send = self.make_alternative_value_messages()
        self.send_messages(messages_to_send)
        self.phase = 3

        # ________________________________________________________PHASE 3

    def listen_phase_3(self):
        # update alternative values
        alternative_values = {}
        for msg in self.message_box:
            alternative_values[msg.get_sender()] = msg.get_content()  # content = neighbor's alter val
        self.clear_message_box()
        # check threshold
        # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        self.calculate_threshold(alternative_values)  # { key: neighbour_id, value: taboo}
        # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    def reply_phase_3(self):
        # send taboo to all neighbors
        self.send_messages(self.taboos)
        self.phase = 4

        # ________________________________________________________PHASE 4

    def listen_phase_4(self):  # not monotony
        # update taboo messages
        # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        taboos = {}
        for msg in self.message_box:
            taboos[msg.get_sender()] = msg.get_content()  # content = taboo
        self.clear_message_box()
        # check limitations
        if not taboos:  # if no taboos
            self.change_assignment()
        # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        self.clear_message_box()
        # self.change_assignment()

    def reply_phase_4(self):
        # send value messages
        messages_to_send = self.make_value_messages()
        self.send_messages(messages_to_send)
        if self.bound - 0.0005 < 0:
            self.bound = self.bound - 0.0005
        # finish iteration
        self.iteration = self.iteration + 1
        self.phase = 1
