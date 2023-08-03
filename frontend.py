import os

import requests
import streamlit as st

BACKEND_JWT = os.environ.get('FORGET_NOTHIN_BACKEND_JWT', '')
BACKEND_URL = os.environ.get('FORGET_NOTHIN_BACKEND_URL', '')


def main():
    st.set_page_config(page_title="ForgetNothin", page_icon="🤔")

    if 'disabled' not in st.session_state:
        st.session_state.disabled = False

    if 'backend_error_response' not in st.session_state:
        st.session_state.backend_error_response = ''

    st.title("🤔 ForgetNothin")
    st.subheader("Reminder app, SMS based. Bare-bones, no fluff")

    left_co, cent_co, last_co = st.columns(3)
    with cent_co:
        st.image('demo.gif')

    st.divider()

    st.subheader("Join the beta")

    with st.form("reminder_form"):
        st.text_input(
            'Name',
            label_visibility='collapsed',
            placeholder='YOUR NAME',
            max_chars=20,
            key='name',
            disabled=st.session_state.disabled,
        )
        st.text_input(
            'Phone',
            label_visibility='collapsed',
            placeholder='YOUR PHONE NUMBER',
            max_chars=10,
            key='phone',
            disabled=st.session_state.disabled,
        )
        st.selectbox(
            'timezone',
            ('US/Pacific', 'US/Eastern', 'US/Central', 'US/Mountain'),
            label_visibility='collapsed',
            key='timezone',
            disabled=st.session_state.disabled,
        )

        def callback():
            if not st.session_state.name or not st.session_state.phone:
                return

            r = requests.post(
                BACKEND_URL,
                headers={'Authorization': f'Bearer {BACKEND_JWT}'},
                json={
                    'name': st.session_state.name,
                    'phone': st.session_state.phone,
                    'timezone': st.session_state.timezone,
                },
            )
            if r.status_code != 201:
                result = r.json()
                st.session_state.backend_error_response = result['message']
                return

            st.session_state.backend_error_response = ''
            st.session_state.disabled = True

        submitted = st.form_submit_button(
            'SUBMIT', disabled=st.session_state.disabled, on_click=callback
        )

        if submitted:
            if not st.session_state.name:
                st.warning('Please input a name.')
                st.stop()

            if not st.session_state.phone:
                st.warning('Please input a phone.')
                st.stop()

            if st.session_state.backend_error_response:
                st.warning(st.session_state.backend_error_response)
                st.stop()

    if submitted:
        st.snow()
        st.toast("Sweet, you're in!", icon='😍')


if __name__ == '__main__':
    main()
