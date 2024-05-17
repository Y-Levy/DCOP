from Agent import Agent
import math
import random
import Message
import numpy as np


class AltruistAgent(Agent):
    def __init__(self, id, domainSize, privacyLevel=1):
        Agent.__init__(self, id, domainSize, privacyLevel)

    def __str__(self):
        s = "I am a Fully Altruist agent, ID: " + str(self.id) + ", utility: " + str(self.utility)
        return s

    # DATA
    def get_data(self):
        # Iteration, Assignment, Utility, None, None, None
        data = [self.iteration, self.id, self.assignment, self.utility]
        return data

    # _____________________________________________________________________________PRIVET METHODS:
    # PHASE 2
    def calculate_next_assignment(self, indications):
        criterion = -math.inf
        next_assignment = self.assignment
        for assignment in range(self.domainSize):
            social_gain = 0
            for neighbour_id in self.neighbours:
                # local changes for neighbours
                indications_list_from_n = indications[neighbour_id]
                n_gain = indications_list_from_n[assignment]
                social_gain = social_gain + n_gain
            if social_gain > criterion:
                criterion = social_gain
                next_assignment = assignment
        self.alterValue = next_assignment

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
        # no need to update alternative values
        self.clear_message_box()
        # no threshold

    def reply_phase_3(self):
        # send empty taboo to all neighbors
        self.send_messages(self.taboos)
        self.phase = 4

        # ________________________________________________________PHASE 4

    def listen_phase_4(self):  # not monotony
        # no need to update taboo messages
        self.clear_message_box()
        self.change_assignment()

    def reply_phase_4(self):
        # send value messages
        messages_to_send = self.make_value_messages()
        self.send_messages(messages_to_send)
        # finish iteration
        self.iteration = self.iteration + 1
        self.phase = 1