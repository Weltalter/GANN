import streamlit as st
from src import additional_functionality as af


def column_details(*args, **kwargs):
    st.session_state.selected_column = ''.join(args)


st.set_page_config(layout='wide', page_title='Предобработка данных')
st.markdown(af.set_size_text('Предобработка данных', 10, bold=True))
st.divider()

st.markdown(af.set_size_text(f'Имя файла: {st.session_state.uploading_dataframe.name}'))
st.markdown(af.set_size_text('Размер файла: {:2.2f} Kb'.format(st.session_state.uploading_dataframe.size / 1024)))
st.markdown(af.set_size_text(f'Количество атрибутов: {len(st.session_state.dataset.input_columns)}'))
st.markdown(af.set_size_text(f'Количество записей: {st.session_state.dataset.count_input_row}'))

st.divider()

with st.status(label=af.set_size_text('Загрузка данных...'), expanded=False) as status:
    tmp_2_1, tmp_2_2 = st.columns([1, 5])
    with tmp_2_1.container(border=1, height=645):
        columns_collection = {}
        for column in st.session_state.dataset.input_columns:
            column = str(column)
            if len(column) > 10:
                columns_collection[column] = column[:6] + '...'
            else:
                columns_collection[column] = column
        for full_column, short_column in columns_collection.items():
            st.button(label=af.set_size_text(short_column),
                      key=full_column,
                      help=af.set_size_text(full_column),
                      on_click=column_details,
                      use_container_width=True,
                      args=full_column)
    with tmp_2_2.container(border=1):
        if st.session_state.selected_column is not None and st.session_state.selected_column in st.session_state.dataset.dataset.columns:
            c_column = st.session_state.dataset.get_column(st.session_state.selected_column)

            tmp_3_1, tmp_3_2, tmp_3_3 = st.tabs([af.set_size_text('Описание атрибута'),
                                                 af.set_size_text('Предобработка данных'),
                                                 af.set_size_text('Поиск аномалий')])
            with tmp_3_1.container():
                st.markdown(af.set_size_text('Пустых значений в свойстве: ' + str(c_column.isnull().sum())))
                st.markdown(af.set_size_text('Уникальных значений в свойстве: ' + str(len(set(c_column)))))
            with tmp_3_2.container():
                tmp_4_1, tmp_4_2 = st.columns([1, 1])
                with tmp_4_1.container():
                    if st.button(label=af.set_size_text('Удалить свойство'),
                                 use_container_width=True):
                        st.session_state.dataset.delete_column(st.session_state.selected_column)
                        st.rerun()
                    if st.button(af.set_size_text('Удалить пропуски'),
                                 use_container_width=True):
                        st.session_state.dataset.delete_void_dataset(st.session_state.selected_column)
                        st.rerun()
                    if st.button(label=af.set_size_text('Усреднить пропуски'),
                                 use_container_width=True):
                        st.session_state.dataset.mean_void_dataset(st.session_state.selected_column)
                        st.rerun()
                with tmp_4_2.container():
                    if st.button(label=af.set_size_text('Порядковое кодирование'),
                                 use_container_width=True,
                                 help=af.set_size_text('OrdinalEncoder')):
                        st.session_state.dataset.ordinal_encoder_column(st.session_state.selected_column)
                        st.rerun()
                    if st.button(label=af.set_size_text('Бинарное кодирование'),
                                 use_container_width=True,
                                 help=af.set_size_text('OneHotEncoder')):
                        st.session_state.dataset.one_hot_encoder_column(st.session_state.selected_column)
                        st.rerun()
                    if st.button(label=af.set_size_text('Выбор выходной переменной'),
                                 use_container_width=True,
                                 help=af.set_size_text('Назначить свойством, которое будет предсказываться')):
                        st.session_state.dataset.output_column = list(
                            st.session_state.dataset.dataset.columns).index(
                            st.session_state.selected_column)
            if st.session_state.selected_column in st.session_state.dataset.dataset_save.select_dtypes(
                    include='number').columns:
                with tmp_3_3.container():
                    form = st.form(key='AnomaliesDelete')
                    maximum = form.slider(label=af.set_size_text('Верхний порог'),
                                          min_value=min(c_column),
                                          max_value=max(c_column),
                                          value=max(c_column))
                    minimum = form.slider(label=af.set_size_text('Нижний порог'),
                                          min_value=min(c_column),
                                          max_value=max(c_column),
                                          value=min(c_column))
                    submit = form.form_submit_button(af.set_size_text('Удалить данные вне порога'))

                    if submit:
                        st.session_state.dataset.delete_anomalies_dataset(st.session_state.selected_column,
                                                                          minimum,
                                                                          maximum)
                        st.rerun()

            # -----------------------------------ОПИСАНИЕ ДАННЫХ
            if st.session_state.selected_column in st.session_state.dataset.dataset_save.select_dtypes(
                    include='number').columns:
                st.divider()
                st.markdown(af.set_size_text('Количественное свойство ``' + st.session_state.selected_column + '"', size=7))
                # -----------------------------------ГРАФИК
                if c_column.isnull().sum() == 0:
                    import altair as alt
                    import pandas as pd

                    data = [[a, b] for a, b in zip([x for x in range(st.session_state.dataset.count_input_row)], sorted([y for y in c_column]))]
                    chart_data = pd.DataFrame(data=data,
                                              columns=['x', 'y'])
                    fig = (
                        alt.Chart(data=chart_data).mark_circle().encode(
                            x='x',
                            y='y')
                    )
                    st.altair_chart(fig, use_container_width=True)
            else:
                st.divider()
                st.markdown(af.set_size_text('Категориальное свойство ``' + st.session_state.selected_column + '"', size=7))

    a, tmp_5_1, tmp_5_2 = st.columns([1, 2.5, 2.5])
    with tmp_5_1.container():
        if st.button(label=af.set_size_text('Нормализовать свойства'), use_container_width=True):
            st.session_state.dataset.normalized_dataset(st.session_state.model_parameters)
            st.rerun()
    with tmp_5_2.container():
        if st.button(af.set_size_text('Восстановить свойства'), use_container_width=True):
            st.session_state.dataset.recover_dataset()
            st.rerun()

    status.update(label=af.set_size_text('Загрузка завершена!'), state='complete', expanded=True)
with st.status(label=af.set_size_text('Загрузка данных...'), expanded=False) as status:
    st.checkbox(af.set_size_text('Расширить столбцы по ширине страницы'), value=False, key='use_container_width')
    st.checkbox(af.set_size_text('Убрать индексы'), value=False, key='hide_index')
    st.dataframe(st.session_state.dataset.dataset,
                 use_container_width=st.session_state.use_container_width,
                 hide_index=st.session_state.hide_index)
    status.update(label=af.set_size_text('Загрузка завершена!'), state='complete', expanded=True)

st.session_state.main_menu_disable = [False, False, False, True, True]
af.main_menu()
