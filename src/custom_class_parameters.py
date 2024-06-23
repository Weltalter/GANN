class Parameters(object):
    def __init__(self):
        self.__num_solutions = 5  # Количество решений
        self.__num_generations = 10  # Количество поколений
        self.__keep_elitism = 2  # Количество сохраняемых лучших решений
        self.__num_parents_mating = 2  # Количество родителей для размножения
        self.__keep_parents = 0  # Количество родителей, переживших эпоху

        self.__num_neurons_input = None  # Количество входных нейронов
        self.__num_neurons_output = None  # Количество выходных нейронов
        self.__num_neurons_hidden = None  # Количество скрытых слоев
        self.__hidden_activations = 'relu'  # Функция активации скрытого слоя
        self.__output_activations = 'softmax'  # Функция активации выходного слоя
        self.__init_range_high = 4.0  # Верхняя граница инициализации стартовой колонии генов
        self.__init_range_low = -4.0  # Нижняя граница инициализации стартовой колонии генов

        self.__parent_selection_type = 'sss'  # Способ выбора родителей для размножения
        self.__k_tournament = 1  # Количество родителей участвующих в турнирном отборе

        self.__crossover_type = 'single_point'  # Способ размножения
        self.__crossover_probability = None  # Вероятность учавствовать в размножении

        self.__mutation_type = 'random'  # Способ мутации
        self.__mutation_probability = 0.1  # Вероятность гена мутировать
        self.__mutation_percent_genes = {'adaptive': (10, 15), 'default': 10}  # Мутация x% всех генов
        self.__mutation_num_genes = 1  # x генов мутируют
        self.__mutation_by_replacement = False  # Полная мутация гена (True/False)
        self.__random_mutation_min_val = -1.0  # Нижняя граница возможной мутации
        self.__random_mutation_max_val = 1.0  # Верхняя граница возможной мутации

        self.__allow_duplicate_genes = True  # Разрешить повторяющиеся гены
        self.__stop_criteria = False
        self.__stop_criteria_reach = None  # Остановка по достижении точности
        self.__stop_criteria_saturate = None  # Остановка по отсутствию развития
        self.__random_seed = None  # Инициализатор генератора случайных чисел

        self.__convert_parameters = None

    @property
    def num_solutions(self):
        return self.__num_solutions

    @num_solutions.setter
    def num_solutions(self, num_solutions):
        if num_solutions is not None:
            if num_solutions > 0:
                self.__num_solutions = num_solutions

    @property
    def num_generations(self):
        return self.__num_generations

    @num_generations.setter
    def num_generations(self, num_generations):
        if num_generations is not None:
            if num_generations > 0:
                self.__num_generations = num_generations

    @property
    def keep_elitism(self):
        return self.__keep_elitism

    @keep_elitism.setter
    def keep_elitism(self, keep_elitism):
        if keep_elitism is not None:
            if keep_elitism >= 0:
                self.__keep_elitism = keep_elitism

    @property
    def num_parents_mating(self):
        return self.__num_parents_mating

    @num_parents_mating.setter
    def num_parents_mating(self, num_parents_mating):
        if num_parents_mating is not None:
            if num_parents_mating > 0:
                self.__num_parents_mating = num_parents_mating

    @property
    def keep_parents(self):
        return self.__keep_parents

    @keep_parents.setter
    def keep_parents(self, keep_parents):
        if keep_parents is not None:
            if keep_parents >= 0:
                self.__keep_parents = keep_parents

    @property
    def num_neurons_input(self):
        return self.__num_neurons_input

    @num_neurons_input.setter
    def num_neurons_input(self, num_neurons_input):
        if num_neurons_input is not None:
            if num_neurons_input > 0:
                self.__num_neurons_input = num_neurons_input - 1

    @property
    def num_neurons_output(self):
        return self.__num_neurons_output

    @num_neurons_output.setter
    def num_neurons_output(self, num_neurons_output):
        if num_neurons_output is not None:
            if num_neurons_output > 0:
                self.__num_neurons_output = num_neurons_output

    @property
    def num_neurons_hidden(self):
        return self.__num_neurons_hidden

    @num_neurons_hidden.setter
    def num_neurons_hidden(self, num_neurons_hidden):
        if num_neurons_hidden is not None:
            if num_neurons_hidden > 0 and self.__num_neurons_input is not None:
                self.__num_neurons_hidden = [self.__num_neurons_input - 1] * num_neurons_hidden

    @property
    def hidden_activations(self):
        return self.__hidden_activations

    @hidden_activations.setter
    def hidden_activations(self, hidden_activations):
        if hidden_activations is not None:
            self.__hidden_activations = hidden_activations

    @property
    def output_activations(self):
        return self.__output_activations

    @output_activations.setter
    def output_activations(self, output_activations):
        if output_activations is not None:
            self.__output_activations = output_activations

    @property
    def init_range_high(self):
        return self.__init_range_high

    @init_range_high.setter
    def init_range_high(self, init_range_high):
        if init_range_high is not None:
            self.__init_range_high = init_range_high

    @property
    def init_range_low(self):
        return self.__init_range_low

    @init_range_low.setter
    def init_range_low(self, init_range_low):
        if init_range_low is not None:
            self.__init_range_low = init_range_low

    @property
    def parent_selection_type(self):
        return self.__parent_selection_type

    @parent_selection_type.setter
    def parent_selection_type(self, parent_selection_type):
        if parent_selection_type is not None:
            parent_selection_type_convert = {'Метод стационарного выбора': 'sss',
                                             'Метод колеса рулетки': 'rws',
                                             'Метод случайного универсального выбора': 'sus',
                                             'Метод выбора ранга': 'rank',
                                             'Метод случайного выбора': 'random',
                                             'Метод турнира': 'tournament'}
            self.__parent_selection_type = parent_selection_type_convert[parent_selection_type]

    @property
    def k_tournament(self):
        return self.__k_tournament

    @k_tournament.setter
    def k_tournament(self, k_tournament):
        if k_tournament is not None:
            if k_tournament > 0:
                self.__k_tournament = k_tournament

    @property
    def crossover_type(self):
        return self.__crossover_type

    @crossover_type.setter
    def crossover_type(self, crossover_type):
        if crossover_type is not None:
            crossover_type_convert = {'Одноточечное пересечение': 'single_point',
                                      'Двухточечное пересечение': 'two_points',
                                      'Равномерное пересечение': 'uniform',
                                      'Рассеянное пересечение': 'scattered'}
            self.__crossover_type = crossover_type_convert[crossover_type]

    @property
    def crossover_probability(self):
        return self.__crossover_probability

    @crossover_probability.setter
    def crossover_probability(self, crossover_probability):
        if crossover_probability is not None:
            self.__crossover_probability = crossover_probability

    @property
    def mutation_type(self):
        return self.__mutation_type

    @mutation_type.setter
    def mutation_type(self, mutation_type):
        if mutation_type is not None:
            mutation_type_convert = {'Метод случайной мутации': 'random',
                                     'Метод мутации подкачки': 'swap',
                                     'Метод инверсионной мутации': 'inversion',
                                     'Метод мутации скремблирования': 'scramble',
                                     'Метод адаптивной мутации': 'adaptive'}
            self.__mutation_type = mutation_type_convert[mutation_type]

    @property
    def mutation_probability(self):
        return self.__mutation_probability

    @mutation_probability.setter
    def mutation_probability(self, mutation_probability):
        if mutation_probability is not None:
            if 1 >= mutation_probability >= 0:
                self.__mutation_probability = mutation_probability

    @property
    def mutation_percent_genes(self):
        return self.__mutation_percent_genes.get(self.mutation_type, self.__mutation_percent_genes.get('default'))

    @mutation_percent_genes.setter
    def mutation_percent_genes(self, mutation_percent_genes):
        if mutation_percent_genes is not None:
            self.__mutation_percent_genes[
                self.mutation_type if self.mutation_type in list(
                    self.__mutation_percent_genes.keys()) else 'default'] = mutation_percent_genes

    @property
    def mutation_num_genes(self):
        return self.__mutation_num_genes

    @mutation_num_genes.setter
    def mutation_num_genes(self, mutation_num_genes):
        if mutation_num_genes is not None:
            if mutation_num_genes >= 0:
                self.__mutation_num_genes = mutation_num_genes

    @property
    def mutation_by_replacement(self):
        return self.__mutation_by_replacement

    @property
    def random_mutation_min_val(self):
        return self.__random_mutation_min_val

    @random_mutation_min_val.setter
    def random_mutation_min_val(self, random_mutation_min_val):
        if random_mutation_min_val is not None:
            self.__random_mutation_min_val = random_mutation_min_val

    @property
    def random_mutation_max_val(self):
        return self.__random_mutation_max_val

    @random_mutation_max_val.setter
    def random_mutation_max_val(self, random_mutation_max_val):
        if random_mutation_max_val is not None:
            self.__random_mutation_max_val = random_mutation_max_val

    @property
    def allow_duplicate_genes(self):
        return self.__allow_duplicate_genes

    @allow_duplicate_genes.setter
    def allow_duplicate_genes(self, allow_duplicate_genes):
        if allow_duplicate_genes is True or False:
            self.__allow_duplicate_genes = allow_duplicate_genes

    @property
    def stop_criteria(self):
        return self.__stop_criteria

    @stop_criteria.setter
    def stop_criteria(self, stop_criteria):
        if stop_criteria is True or stop_criteria is False:
            self.__stop_criteria = stop_criteria

    @property
    def stop_criteria_reach(self):
        return self.__stop_criteria_reach

    @stop_criteria_reach.setter
    def stop_criteria_reach(self, stop_criteria_reach):
        if stop_criteria_reach is not None:
            self.__stop_criteria_reach = stop_criteria_reach

    @property
    def stop_criteria_saturate(self):
        return self.__stop_criteria_saturate

    @stop_criteria_saturate.setter
    def stop_criteria_saturate(self, stop_criteria_saturate):
        if stop_criteria_saturate is not None:
            self.__stop_criteria_saturate = stop_criteria_saturate

    @property
    def random_seed(self):
        return self.__random_seed

    @random_seed.setter
    def random_seed(self, random_seed):
        if random_seed is not None:
            self.__random_seed = random_seed

    def get_stop_criteria(self):
        if self.__stop_criteria_reach is not None and self.__stop_criteria_saturate is not None:
            return [f'reach_{self.__stop_criteria_reach}',
                    f'saturate_{self.__stop_criteria_saturate}']
        else:
            return None
