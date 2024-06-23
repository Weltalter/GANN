import streamlit as st
import numpy as np
from src import custom_class_genetic_algorithm as ga
from src import additional_functionality as af

st.set_page_config(layout='wide', page_title='Построение модели')
st.markdown(af.set_size_text('Построение модели', 10, bold=True))
st.divider()

try:
    st.session_state.ga_class = ga.GA(st.session_state.model_parameters)
except:
    st.error(af.set_size_text('Не зарегистрированная ошибка!'))
else:
    tmp_3_1, tmp_3_2, tmp_3_3 = st.tabs([af.set_size_text('Данные об эволюции'),
                                         af.set_size_text('График алгоритма'),
                                         af.set_size_text('Статистика обучения')])
    with tmp_3_1.container(border=True, height=500):
        st.markdown(af.set_size_text('Данные об эволюции', 7, bold=True))
        if st.button(af.set_size_text('Начать')):
            st.session_state.end_algorithm = False
            st.markdown(af.set_size_text('Сведения о поколениях:'))
            st.session_state.ga_class.start()
    with tmp_3_2.container(border=True):
        st.markdown(af.set_size_text('График алгоритма', 7, bold=True))

        if st.session_state.end_algorithm and len(st.session_state.ga_class.fitness_value_list) > 0:
            import plotly.express as px

            fig_1 = px.line(x=range(0, len(st.session_state.ga_class.fitness_value_list), 1),
                            y=st.session_state.ga_class.fitness_value_list)
            fig_1.update_layout(width=890, height=390,
                                xaxis_title='Поколения',
                                yaxis_title='Точность лучшей колонии')
            st.plotly_chart(fig_1)
        else:
            st.info('Завершите эволюцию...')
    with tmp_3_3.container(border=True):
        st.markdown(af.set_size_text('Статистика обучения', 7, bold=True))

        if st.session_state.end_algorithm:
            st.markdown(af.set_size_text('Количество сформированных поколений: ')
                        + f'{st.session_state.ga_class.generations_count}'
                        + f'\\{st.session_state.ga_class.parameters.num_generations}')
            st.markdown(af.set_size_text('Поколение лучшего решения: ')
                        + f'{st.session_state.ga_class.best_solution_generation}')

            st.divider()
            st.session_state.save_statistic['Complete generations'] = st.session_state.ga_class.generations_count
            st.session_state.save_statistic['Train confusion matrix'] = st.session_state.ga_class.confusion_matrix(st.session_state.dataset.input_train_data,
                                                                                                                   st.session_state.dataset.output_train_data)
            st.session_state.save_statistic['Train accuracy'] = st.session_state.ga_class.accuracy(st.session_state.dataset.input_train_data,
                                                                                                   st.session_state.dataset.output_train_data)
            st.session_state.save_statistic['Train precision'] = st.session_state.ga_class.precision(st.session_state.dataset.input_train_data,
                                                                                                     st.session_state.dataset.output_train_data)
            st.session_state.save_statistic['Train recall'] = st.session_state.ga_class.recall(st.session_state.dataset.input_train_data,
                                                                                               st.session_state.dataset.output_train_data)
            st.session_state.save_statistic['Train f1'] = st.session_state.ga_class.f1(st.session_state.dataset.input_train_data,
                                                                                       st.session_state.dataset.output_train_data)
            st.session_state.save_statistic['Best solution'] = st.session_state.ga_class.best_solution[0]

            st.markdown(af.set_size_text('Матрица ошибок:'))
            st.table(st.session_state.save_statistic['Train confusion matrix'])
            st.markdown(af.set_size_text('Точность: ')
                        + f'{st.session_state.save_statistic["Train accuracy"]:.2f}%')
            st.markdown(af.set_size_text('Precision: ')
                        + f'{st.session_state.save_statistic["Train precision"]:.2f}%')
            st.markdown(af.set_size_text('Recall: ')
                        + f'{st.session_state.save_statistic["Train recall"]:.2f}%')
            st.markdown(af.set_size_text('F-мера: ')
                        + f'{st.session_state.save_statistic["Train f1"]:.2f}%')

            st.session_state.main_menu_disable = [False, False, False, False, False]
        else:
            st.info('Завершите эволюцию...')

af.main_menu()
