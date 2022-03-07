#!/usr/bin/python3
import getopt
import sys
import dearpygui.dearpygui as dpg
import dearpygui.demo as demo


def main(argv):
    # dashboard needs
    # - window with list of servers and way to edit list
    #    - name, host, description, username
    #    - User should be able to select one, perhaps this will do login and get token
    #    - host details and token can be passed to tool
    # - Read a list of possible untilities out of dictionary (compiled in)
    #    - could be dynamic but that seems excessive
    #    - title, description, list of parameters it needs in addition to server details.

    dpg.create_context()
    dpg.create_viewport(title='ZoneMinder Utils', width=1200, height=1200)

    with dpg.window(label="Example Window"):
        dpg.add_text("Hello, world")
        dpg.add_button(label="Save")
        dpg.add_input_text(label="string", default_value="Quick brown fox")
        dpg.add_slider_float(label="float", default_value=0.273, max_value=1)
    # demo.show_demo()

    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()
    
    # options = commandOptions(argv)
    # if options['user'] != "" and options['pass'] != "":
    #     options['token'] = getToken(options)
    #     # print(token)
    #     if options['token'] != "":
    #         print('Logged In !')
    #         deleteEvents(options)
    #     else:
    #         print(' Did not log in')

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main(sys.argv[1:])
