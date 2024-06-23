import streamlit as st
from src import additional_functionality as af


def list_of_buttons(key, param, min_value, max_value):
    buttons = st.columns([1, 1, 1, 1, 1, 1])
    changes = param
    with buttons[0]:
        if st.button(label=af.set_size_text('-100', 3),
                     key=key + '_m100'):
            changes = param - 100
    with buttons[1]:
        if st.button(label=af.set_size_text('-10', 3),
                     key=key + '_m10'):
            changes = param - 10
    with buttons[2]:
        if st.button(label=af.set_size_text('-1', 3),
                     key=key + '_m1'):
            changes = param - 1
    with buttons[3]:
        if st.button(label=af.set_size_text('+1', 3),
                     key=key + '_p1'):
            changes = param + 1
    with buttons[4]:
        if st.button(label=af.set_size_text('+10', 3),
                     key=key + '_p10'):
            changes = param + 10
    with buttons[5]:
        if st.button(label=af.set_size_text('+100', 3),
                     key=key + '_p100'):
            changes = param + 100

    if changes < min_value:
        return min_value
    elif changes > max_value:
        return max_value
    else:
        return changes


st.set_page_config(layout='wide', page_title='Настройка модели')
st.markdown(af.set_size_text('Настройка модели', 10, bold=True))
st.divider()

tmp_1_1, tmp_1_2, tmp_1_3 = st.tabs(
    [af.set_size_text('Настройка генетического алгоритма'),
     af.set_size_text('Настройка нейронной сети'),
     af.set_size_text('Прочие настройки')]
)

st.session_state.dataset.set_data()

st.session_state.model_parameters.num_neurons_input = len(st.session_state.dataset.input_columns)
st.session_state.model_parameters.num_neurons_output = st.session_state.dataset.get_count_unique_output_row()
with tmp_1_1.container(border=True):
    st.markdown(af.set_size_text('Настройки колонии', 7, bold=True))
    tmp_2_1, tmp_2_2 = st.columns([1, 1])
    with tmp_2_1.container():
        with st.container(border=True):
            st.session_state.model_parameters.num_solutions = list_of_buttons(
                param=st.session_state.model_parameters.num_solutions,
                min_value=5,
                max_value=1000,
                key='num_solutions')
            st.write(af.set_size_text('Количество особей в поколении: '
                                      + str(st.session_state.model_parameters.num_solutions)))
        with st.container(border=True):
            st.session_state.model_parameters.num_parents_mating = list_of_buttons(
                param=st.session_state.model_parameters.num_parents_mating,
                min_value=2,
                max_value=st.session_state.model_parameters.num_solutions,
                key='num_parents_mating')
            st.write(af.set_size_text('Количество родителей: '
                                      + str(st.session_state.model_parameters.num_parents_mating)))
        with st.container(border=True):
            st.session_state.model_parameters.keep_parents = list_of_buttons(
                param=st.session_state.model_parameters.keep_parents,
                min_value=0,
                max_value=st.session_state.model_parameters.num_parents_mating,
                key='keep_parents')
            st.write(af.set_size_text('Переход родителей в новое поколение: '
                                      + str(st.session_state.model_parameters.keep_parents)))
    with tmp_2_2.container():
        with st.container(border=True):
            st.session_state.model_parameters.num_generations = list_of_buttons(
                param=st.session_state.model_parameters.num_generations,
                min_value=5,
                max_value=1000,
                key='num_generations')
            st.write(af.set_size_text('Количество поколений: '
                                      + str(st.session_state.model_parameters.num_generations)))
        with st.container(border=True):
            st.session_state.model_parameters.keep_elitism = list_of_buttons(
                param=st.session_state.model_parameters.keep_elitism,
                min_value=0,
                max_value=st.session_state.model_parameters.num_solutions,
                key='keep_elitism')
            st.write(af.set_size_text('Переход лучшей особи в новое поколение: '
                                      + str(st.session_state.model_parameters.keep_elitism)))

    st.markdown(af.set_size_text('Настройки мутации', 7, bold=True))
    tmp_3_1, tmp_3_2 = st.columns([1, 1])
    with tmp_3_1.container():
        with st.container(border=True):
            st.session_state.model_parameters.mutation_type = st.radio(
                label=af.set_size_text('Метод мутации'),
                options=('Метод случайной мутации',
                         'Метод мутации подкачки',
                         'Метод инверсионной мутации',
                         'Метод мутации скремблирования',
                         'Метод адаптивной мутации'))
    with tmp_3_2.container():
        with st.container(border=True):
            if st.session_state.model_parameters.mutation_type is not None:
                if st.session_state.model_parameters.mutation_type == 'random':
                    (st.session_state.model_parameters.random_mutation_min_val,
                     st.session_state.model_parameters.random_mutation_max_val) = st.slider(
                        label=af.set_size_text('Вероятность мутации гена'),
                        min_value=0,
                        max_value=100,
                        value=(15, 30))
                else:
                    mutation_chance_type = st.radio(
                        label=af.set_size_text('Способ отбора генов для мутации'),
                        options=('Вероятность мутации гена',
                                 'Процент мутирующих генов',
                                 'Количество мутирующих генов'))

                    if mutation_chance_type == 'Вероятность мутации гена':
                        st.session_state.model_parameters.mutation_probability = st.slider(
                            label=' ',
                            min_value=0.0,
                            max_value=1.0,
                            step=0.01,
                            value=0.1)
                    elif mutation_chance_type == 'Процент мутирующих генов':
                        if st.session_state.model_parameters.mutation_type == 'adaptive':
                            st.session_state.model_parameters.mutation_percent_genes = st.slider(
                                label=af.set_size_text(' '),
                                min_value=0,
                                max_value=100,
                                value=(10, 15))
                        else:
                            st.session_state.model_parameters.mutation_percent_genes = st.slider(
                                label=' ',
                                min_value=1,
                                max_value=100,
                                value=10)
                    elif mutation_chance_type == 'Количество мутирующих генов':
                        st.session_state.model_parameters.mutation_num_genes = st.slider(
                            label=' ',
                            min_value=1,
                            max_value=len(st.session_state.dataset.input_columns) - 1,
                            value=1)

    st.markdown(af.set_size_text('Настройки селекции', 7, bold=True))
    tmp_4_1, tmp_4_2 = st.columns([1, 1])
    with tmp_4_1.container():
        with st.container(border=True):
            st.session_state.model_parameters.parent_selection_type = st.radio(
                label=af.set_size_text('Способ выбора родителей для селекции'),
                options=('Метод стационарного выбора',
                         'Метод колеса рулетки',
                         'Метод случайного универсального выбора',
                         'Метод выбора ранга',
                         'Метод случайного выбора',
                         'Метод турнира'))

        if st.session_state.model_parameters.parent_selection_type == 'tournament':
            if st.session_state.model_parameters.num_parents_mating == 1:
                st.session_state.model_parameters.k_tournament = 1
            else:
                with st.container(border=True):
                    st.session_state.model_parameters.k_tournament = list_of_buttons(
                        param=st.session_state.model_parameters.k_tournament,
                        min_value=1,
                        max_value=st.session_state.model_parameters.num_parents_mating,
                        key='k_tournament')
                    st.write(af.set_size_text('Количество родителей, участвующих в турнире: '
                                              + str(st.session_state.model_parameters.k_tournament)))
    with tmp_4_2.container():
        with st.container(border=True):
            st.session_state.model_parameters.crossover_type = st.radio(
                label=af.set_size_text('Способ скрещивания'),
                options=('Одноточечное пересечение',
                         'Двухточечное пересечение',
                         'Равномерное пересечение',
                         'Рассеянное пересечение'))

            if st.checkbox(label=af.set_size_text('Вероятность скрещивания', 4)):
                st.session_state.model_parameters.crossover_probability = st.slider(
                    label=af.set_size_text('Вероятность выбрать родителя для скрещивания'),
                    min_value=0.0,
                    max_value=1.0,
                    step=0.01,
                    value=0.5)
            else:
                st.session_state.model_parameters.crossover_probability = None
with tmp_1_2.container(border=True):
    tmp_5_1, sp_4, tmp_5_2, sp_5, tmp_5_3 = st.columns([1, 0.1, 1, 0.1, 1])
    with tmp_5_1.container():
        st.session_state.model_parameters.num_neurons_hidden = st.number_input(
            label=af.set_size_text('Количество скрытых слоев'),
            min_value=1,
            max_value=10,
            value=1)
    with tmp_5_2.container():
        st.session_state.model_parameters.hidden_activations = st.radio(
            label=af.set_size_text('Функция скрытого слоя'),
            options=['relu'])
    with tmp_5_3.container():
        st.session_state.model_parameters.output_activation = st.radio(
            label=af.set_size_text('Функция выходного слоя'),
            options=['softmax'])
    (st.session_state.model_parameters.init_range_low, st.session_state.model_parameters.init_range_high) = st.slider(
        label=af.set_size_text('Диапазон инициализируемых генов'),
        min_value=-50.0,
        max_value=50.0,
        value=(-4.0, 4.0))
with tmp_1_3.container(border=True):
    st.session_state.model_parameters.allow_duplicate_genes = st.checkbox(
        label=af.set_size_text('Разрешить повторяющиеся значения генов', 4))
    st.session_state.model_parameters.stop_criteria = st.checkbox(
        label=af.set_size_text('Настроить критерии принудительной остановки', 4))
    if st.session_state.model_parameters.stop_criteria:
        st.session_state.model_parameters.stop_criteria_reach = st.slider(
            label=af.set_size_text('Необходимый предел точности'),
            min_value=0.0,
            max_value=100.0,
            value=100.0)
        st.session_state.model_parameters.stop_criteria_saturate = st.slider(
            label=af.set_size_text('Количество поколений без развития'),
            min_value=0,
            max_value=st.session_state.model_parameters.num_generations,
            value=st.session_state.model_parameters.num_generations)
    else:
        st.session_state.model_parameters.stop_criteria_reach = None
        st.session_state.model_parameters.stop_criteria_saturate = None

    if st.checkbox(label=af.set_size_text('Настроить seed случайных чисел', 4)):
        st.session_state.model_parameters.random_seed = st.number_input(
            label=af.set_size_text('Random seed'),
            min_value=0,
            max_value=64536,
            value=0)
    else:
        st.session_state.model_parameters.random_seed = None

st.session_state.main_menu_disable = [False, False, False, False, True]
af.main_menu()
