import streamlit as st
import src.custom_class_parameters as param


def set_size_text(txt, size=5, bold=False, italic=False):
    if bold:
        txt = f'\\textbf{{{txt}}}'
    if italic:
        txt = f'\\textit{{{txt}}}'

    text_size = ['\\tiny',
                 '\\scriptsize',
                 '\\footnotesize',
                 '\\small',
                 '\\normalsize',
                 '\\large',
                 '\\Large',
                 '\\LARGE',
                 '\\huge',
                 '\\Huge']
    return fr"$\textsf{{{text_size[size - 1]} {txt}}}$"


def init_state():
    st.session_state.main_menu_disable = [False, True, True, True, True]

    st.session_state.uploading_dataframe = None

    st.session_state.use_container_width = False
    st.session_state.hide_index = False

    st.session_state.dataset = None
    st.session_state.selected_column = None

    st.session_state.ga_class = None
    st.session_state.end_algorithm = False

    st.session_state.model_parameters = param.Parameters()
    st.session_state.save_statistic = {}
    st.session_state.txt_statistic = ''
    st.session_state.download_disable = True

    st.switch_page("pages/1_uploading_data.py")


def main_menu():
    st.sidebar.title(set_size_text('Моделирование', 6, bold=True))

    st.sidebar.page_link(page='pages/1_uploading_data.py',
                         label=set_size_text('Загрузка данных', 6),
                         icon="📤",
                         disabled=st.session_state.main_menu_disable[0])
    st.sidebar.page_link(page='pages/2_data_preprocessing.py',
                         label=set_size_text('Предобработка данных', 6),
                         icon="📝",
                         disabled=st.session_state.main_menu_disable[1])
    st.sidebar.page_link(page='pages/3_setting_up_the_model.py',
                         label=set_size_text('Настройка модели', 6),
                         icon="⚙",
                         disabled=st.session_state.main_menu_disable[2])
    st.sidebar.page_link(page='pages/4_building_a_model.py',
                         label=set_size_text('Построение модели', 6),
                         icon="🔨",
                         disabled=st.session_state.main_menu_disable[3])
    st.sidebar.page_link(page='pages/5_evaluation_of_the_model.py',
                         label=set_size_text('Оценка модели', 6),
                         icon="📊",
                         disabled=st.session_state.main_menu_disable[4])
    st.sidebar.download_button(label=set_size_text('📥Сохранить модель', 6),
                               data=st.session_state.txt_statistic,
                               disabled=st.session_state.download_disable)
