import streamlit as st
from src import additional_functionality as af

st.set_page_config(layout='wide', page_title='Оценка модели')
st.markdown(af.set_size_text('Оценка модели', 10, bold=True))

if st.session_state.txt_statistic != '':
    st.session_state.txt_statistic = ''

with st.status(af.set_size_text('Идет тестирование'), expanded=False) as status:
    st.markdown(af.set_size_text('Размер тестовой выборки: ')
                + f'{len(st.session_state.dataset.output_test_data)}')

    st.session_state.txt_statistic += 'СТАСТИКА ТРЕНИРОВКИ МОДЕЛИ\n'
    st.session_state.txt_statistic += f'Количество сформированных поколений: {st.session_state.save_statistic["Complete generations"]}\n'
    st.session_state.txt_statistic += f'Матрица ошибок:\n'
    st.session_state.txt_statistic += '\n'.join(
        ' '.join(f'{x}' for x in row) for row in st.session_state.save_statistic['Train confusion matrix'])
    st.session_state.txt_statistic += '\n'
    st.session_state.txt_statistic += f'Точность: {st.session_state.save_statistic["Train accuracy"]:.2f}\n'
    st.session_state.txt_statistic += f'Precision: {st.session_state.save_statistic["Train precision"]:.2f}\n'
    st.session_state.txt_statistic += f'Recall: {st.session_state.save_statistic["Train recall"]:.2f}\n'
    st.session_state.txt_statistic += f'F-мера: {st.session_state.save_statistic["Train f1"]:.2f}\n'
    st.session_state.txt_statistic += f'Лучшее решение:\n{st.session_state.save_statistic["Best solution"]}\n\n'

    st.session_state.txt_statistic += 'СТАСТИКА ТЕСТИРОВАНИЯ МОДЕЛИ\n'
    st.session_state.save_statistic['Test confusion matrix'] = st.session_state.ga_class.confusion_matrix(
        st.session_state.dataset.input_test_data,
        st.session_state.dataset.output_test_data)
    st.session_state.save_statistic['Test accuracy'] = st.session_state.ga_class.accuracy(
        st.session_state.dataset.input_test_data,
        st.session_state.dataset.output_test_data)
    st.session_state.save_statistic['Test precision'] = st.session_state.ga_class.precision(
        st.session_state.dataset.input_test_data,
        st.session_state.dataset.output_test_data)
    st.session_state.save_statistic['Test recall'] = st.session_state.ga_class.recall(
        st.session_state.dataset.input_test_data,
        st.session_state.dataset.output_test_data)
    st.session_state.save_statistic['Test f1'] = st.session_state.ga_class.f1(
        st.session_state.dataset.input_test_data,
        st.session_state.dataset.output_test_data)

    st.markdown(af.set_size_text('Матрица ошибок:'))
    st.table(st.session_state.save_statistic['Test confusion matrix'])
    st.markdown(af.set_size_text('Точность: ')
                + f'{st.session_state.save_statistic["Test accuracy"]:.2f}%')
    st.markdown(af.set_size_text('Precision: ')
                + f'{st.session_state.save_statistic["Test precision"]:.2f}%')
    st.markdown(af.set_size_text('Recall: ')
                + f'{st.session_state.save_statistic["Test recall"]:.2f}%')
    st.markdown(af.set_size_text('F-мера: ')
                + f'{st.session_state.save_statistic["Test f1"]:.2f}%')

    st.session_state.txt_statistic += f'Матрица ошибок:\n'
    st.session_state.txt_statistic += '\n'.join(
        ' '.join(f'{x}' for x in row) for row in st.session_state.save_statistic['Test confusion matrix'])
    st.session_state.txt_statistic += '\n'
    st.session_state.txt_statistic += f'Точность: {st.session_state.save_statistic["Test accuracy"]:.2f}\n'
    st.session_state.txt_statistic += f'Precision: {st.session_state.save_statistic["Test precision"]:.2f}\n'
    st.session_state.txt_statistic += f'Recall: {st.session_state.save_statistic["Test recall"]:.2f}\n'
    st.session_state.txt_statistic += f'F-мера: {st.session_state.save_statistic["Test f1"]:.2f}\n'

    status.update(label=af.set_size_text('Тестирование завершено!'), state='complete', expanded=True)

st.session_state.download_disable = False

af.main_menu()
