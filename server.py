from selenium import webdriver
from flask import Flask, request
import time

app = Flask(__name__)


def start_send_accept_requests(username_text, password_text, no_of_connections_to_send):
    driver = webdriver.Chrome('./chromedriver')

    # login into account
    driver.get('https://www.linkedin.com/checkpoint/rm/sign-in-another-account?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin')
    username = driver.find_element_by_id('username')
    username.send_keys(username_text)
    password = driver.find_element_by_id('password')
    password.send_keys(password_text)
    driver.find_element_by_css_selector('[type=submit]').click()

    driver.get('https://www.linkedin.com/mynetwork/')
    time.sleep(5)

    # close messages tab
    driver.find_elements_by_css_selector(
        '.msg-overlay-bubble-header__controls.display-flex > *')[2].click()

    # Accept all incoming
    accept_buttons = driver.find_elements_by_css_selector(
        '[aria-label^="Accept"]')
    for accept_button in accept_buttons:
        accept_button.click()
        time.sleep(3)

    # Send all that can be sent
    request_sent = 0
    connection_buttons = driver.find_elements_by_css_selector(
        '[aria-label^="Invite"]')
    for connect_button in connection_buttons:
        connect_button.click()
        request_sent += 1
        if request_sent >= no_of_connections_to_send:
            break
        time.sleep(3)

    driver.close()
    driver.quit()


@app.route('/send_requests')
def handle_send_requests():
    try:
        username = request.args.get('username')
        password = request.args.get('password')
        no_of_connections_to_send = int(
            request.args.get('no_of_connections_to_send'))

        if not username or not password or not no_of_connections_to_send:
            return "Send all params (username, password, no_of_connections_to_send)"

        start_send_accept_requests(
            username, password, no_of_connections_to_send)
        return "Requests sent"
    except:
        return "An error occurred"


if __name__ == '__main__':
    app.run()
