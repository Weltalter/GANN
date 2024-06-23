import streamlit as st
from src import custom_class_dataset as ds
from src import additional_functionality as af

st.set_page_config(layout='wide', page_title='Загрузка данных')
st.markdown(af.set_size_text('Загрузка данных', 10, bold=True))
st.divider()

st.markdown(af.set_size_text('Загрузите файл набора данных в формате .CSV'))

st.session_state.uploading_dataframe = st.file_uploader('')
if st.session_state.uploading_dataframe is not None:
    try:
        st.session_state.dataset = ds.DS()
        st.session_state.dataset.read_dataset(st.session_state.uploading_dataframe)
    except:
        st.error(af.set_size_text('Не удалось прочитать файл'))
        st.session_state.main_menu_disable = [False, True, True, True, True]
    else:
        st.success(af.set_size_text('Файл успешно загружен'))
        st.session_state.main_menu_disable = [False, False, True, True, True]
else:
    st.session_state.main_menu_disable = [False, True, True, True, True]

af.main_menu()
