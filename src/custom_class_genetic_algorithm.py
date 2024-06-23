import numpy as np
import pygad.gann
import pygad.nn
import streamlit as st


class GA(object):
    def __init__(self, param):
        self.__nn_parameters = param
        self.__inst_gann = pygad.gann.GANN(num_solutions=self.parameters.num_solutions,
                                           num_neurons_input=self.parameters.num_neurons_input,
                                           num_neurons_hidden_layers=self.parameters.num_neurons_hidden,
                                           num_neurons_output=self.parameters.num_neurons_output,
                                           hidden_activations=self.parameters.hidden_activations,
                                           output_activation=self.parameters.output_activations)

        self.create_ga()
        self.__fitness_value_list = []

    def fitness_func(self, ga_instance, solution, sol_idx):
        if sol_idx is None:
            sol_idx = 1

        predictions = pygad.nn.predict(last_layer=self.__inst_gann.population_networks[sol_idx],
                                       data_inputs=st.session_state.dataset.input_train_data)
        correct_predictions = np.where(predictions == st.session_state.dataset.output_train_data)[0].size
        solution_fitness = (correct_predictions / st.session_state.dataset.output_train_data.size) * 100

        return solution_fitness

    def callback_generation(self, ga_instance):
        population_matrices = pygad.gann.population_as_matrices(
            population_networks=self.__inst_gann.population_networks,
            population_vectors=ga_instance.population)
        self.__inst_gann.update_population_trained_weights(population_trained_weights=population_matrices)
        self.__fitness_value_list.append(ga_instance.best_solution()[1])

        st.divider()
        st.write(f"Generation = {ga_instance.generations_completed}")
        st.write(f"Fitness = {ga_instance.best_solution()[1]:.2f}")

    def stop_generation(self, ga_instance, last_solution):
        st.session_state.end_algorithm = True

    def create_ga(self):
        if self.parameters.mutation_type == 'adaptive':
            self.__inst_ga = pygad.GA(num_generations=self.parameters.num_generations,
                                      num_parents_mating=self.parameters.num_parents_mating,
                                      initial_population=pygad.gann.population_as_vectors(
                                          population_networks=self.__inst_gann.population_networks).copy(),
                                      fitness_func=self.fitness_func,
                                      init_range_low=self.parameters.init_range_low,
                                      init_range_high=self.parameters.init_range_high,
                                      parent_selection_type=self.parameters.parent_selection_type,
                                      crossover_type=self.parameters.crossover_type,
                                      crossover_probability=self.parameters.crossover_probability,
                                      mutation_type=self.parameters.mutation_type,
                                      mutation_percent_genes=self.parameters.mutation_percent_genes,
                                      mutation_by_replacement=self.parameters.mutation_by_replacement,
                                      K_tournament=self.parameters.k_tournament,
                                      random_mutation_min_val=self.parameters.random_mutation_min_val,
                                      random_mutation_max_val=self.parameters.random_mutation_max_val,
                                      keep_parents=self.parameters.keep_parents,
                                      keep_elitism=self.parameters.keep_elitism,
                                      allow_duplicate_genes=self.parameters.allow_duplicate_genes,
                                      random_seed=self.parameters.random_seed,
                                      suppress_warnings=True,
                                      on_generation=self.callback_generation,
                                      save_solutions=False,
                                      stop_criteria=self.parameters.get_stop_criteria(),
                                      on_stop=self.stop_generation)
        else:
            self.__inst_ga = pygad.GA(num_generations=self.parameters.num_generations,
                                      num_parents_mating=self.parameters.num_parents_mating,
                                      initial_population=pygad.gann.population_as_vectors(
                                          population_networks=self.__inst_gann.population_networks).copy(),
                                      fitness_func=self.fitness_func,
                                      init_range_low=self.parameters.init_range_low,
                                      init_range_high=self.parameters.init_range_high,
                                      parent_selection_type=self.parameters.parent_selection_type,
                                      crossover_type=self.parameters.crossover_type,
                                      crossover_probability=self.parameters.crossover_probability,
                                      mutation_type=self.parameters.mutation_type,
                                      mutation_probability=self.parameters.mutation_probability,
                                      mutation_percent_genes=self.parameters.mutation_percent_genes,
                                      mutation_num_genes=self.parameters.mutation_num_genes,
                                      mutation_by_replacement=self.parameters.mutation_by_replacement,
                                      K_tournament=self.parameters.k_tournament,
                                      random_mutation_min_val=self.parameters.random_mutation_min_val,
                                      random_mutation_max_val=self.parameters.random_mutation_max_val,
                                      keep_parents=self.parameters.keep_parents,
                                      keep_elitism=self.parameters.keep_elitism,
                                      allow_duplicate_genes=self.parameters.allow_duplicate_genes,
                                      random_seed=self.parameters.random_seed,
                                      suppress_warnings=True,
                                      on_generation=self.callback_generation,
                                      save_solutions=False,
                                      stop_criteria=self.parameters.get_stop_criteria(),
                                      on_stop=self.stop_generation)

    def start(self):
        self.__inst_ga.run()

    @property
    def fitness_value_list(self):
        return self.__fitness_value_list

    @property
    def parameters(self):
        return self.__nn_parameters

    @property
    def best_solution(self):
        return self.__inst_ga.best_solution()

    @property
    def best_solution_generation(self):
        return self.__inst_ga.best_solution_generation

    def predictions(self, data):
        return pygad.nn.predict(last_layer=self.__inst_gann.population_networks[self.best_solution[2]],
                                data_inputs=data)

    def confusion_matrix(self, input_data, output_data):
        from sklearn.metrics import confusion_matrix
        return confusion_matrix(list(output_data), list(self.predictions(input_data)))

    def accuracy(self, input_data, output_data):
        from sklearn.metrics import accuracy_score
        return 100 * accuracy_score(list(output_data), list(self.predictions(input_data)))

    def precision(self, input_data, output_data):
        from sklearn.metrics import precision_score
        return 100 * precision_score(list(output_data), list(self.predictions(input_data)))

    def recall(self, input_data, output_data):
        from sklearn.metrics import recall_score
        return 100 * recall_score(list(output_data), list(self.predictions(input_data)))

    def f1(self, input_data, output_data):
        from sklearn.metrics import f1_score
        return 100 * f1_score(list(output_data), list(self.predictions(input_data)), average='macro')

    @property
    def generations_count(self):
        return self.__inst_ga.generations_completed
