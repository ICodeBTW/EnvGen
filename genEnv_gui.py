import PySimpleGUI as sg
import genEnv as ge

sg.theme('Reddit')

ITBU_ALL = ['Green', 'Blue', 'Red']
ASSET_LIST = ['credentials','text','integer','boolean']
ENV_LIST = ['dev','prod']
FOLDER_LIST = ['default']
data= [["name","type","value","description"]]



def make_window1():
    title = 'Folder name'
    layout = [[sg.Titlebar(title, sg.CUSTOM_TITLEBAR_ICON)],
              [sg.Text(key='-STATUS-')],
              [sg.InputText(key="-FOLDER_NAME-", tooltip="Folder Name*",disabled=True),
               sg.FolderBrowse(button_text="Browse", initial_folder=".", tooltip="Browse for Uipath project folder")],
              [sg.Button('Next >'), sg.Button('Exit')]]

    return  sg.Window(title, layout, resizable=True, no_titlebar=True, keep_on_top=True, margins=(0, 0), finalize=True)


def make_window2():
    title = 'Environment Variables'
    layout = [ [sg.Titlebar(title, sg.CUSTOM_TITLEBAR_ICON)],
               [sg.Text("Choose the ITBU and Environment you want your script to be deployed to")],
               [sg.Text(key='-STATUS-')],
               [sg.Text("ITBU"), sg.Combo(ITBU_ALL, key='-ITBU-', tooltip="Choose your ITBU")],
               [sg.Text("Environment"), sg.Combo(ENV_LIST, key='-ENVLIST-', tooltip="Choose your Environment")],
               [sg.Button('< Prev'), sg.Button('Next >')]]

    return  sg.Window(title, layout, resizable=True, no_titlebar=True, keep_on_top=True, margins=(0, 0), finalize=True)


def make_window3():
    title = 'Asset Generation'
    headings = [str(data[0][x])+'     ..' for x in range(len(data[0]))]
    layout = [ [sg.Titlebar(title, sg.CUSTOM_TITLEBAR_ICON)],
               [sg.Text('Asset Generation')],
               [sg.Table(values=data[1:][:], headings=headings, max_col_width=25,
                        # background_color='light blue',
                        auto_size_columns=True,
                        display_row_numbers=True,
                        justification='right',
                        num_rows=5,
                        alternating_row_color='lightblue',
                        enable_click_events=True,
                        key='-TABLE-',
                        row_height=25,
                        tooltip='Assets Table'), sg.Button('Add',key='-ADD-'),sg.Button('Remove',key='-REMOVE-')],
               [sg.Text("Name"),sg.InputText(key="-NAME-"),sg.VerticalSeparator(pad=None),sg.Text("Type"),sg.Combo(ASSET_LIST,key="-TYPE-")],
               [sg.Text("Value"), sg.InputText(key="-VALUE-"), sg.VerticalSeparator(pad=None), sg.Text("Description"),
                sg.InputText(key="-DESC-")],
               [sg.Button('< Prev'),sg.Button('Generate csv',key='-GEN-'),sg.Button('Next >')]]

    return  sg.Window(title, layout, resizable=True, no_titlebar=True, keep_on_top=True, margins=(0, 0), finalize=True)

def make_window4():
    title = 'Publish to GitLab'
    layout = [ [sg.Titlebar(title, sg.CUSTOM_TITLEBAR_ICON)],
               [sg.Text('Window 4')],
               [sg.Button('< Prev'), sg.Button('Exit')]]
    return  sg.Window(title, layout, resizable=True, no_titlebar=True, keep_on_top=True, margins=(0, 0), finalize=True)

def main():
    # sg.theme('light green 3')
    # sg.theme('dark red')

    title = 'Customized Titlebar Window'

    window1, window2, window3, window4 = make_window1(), None, None, None

    while True:  # Event Loop
        window, event, values = sg.read_all_windows()
        if window == window1 and event in (sg.WIN_CLOSED, 'Exit'):
            break

        if window == window1:
            input_key_list = [key for key, value in window.key_dict.items()
                              if isinstance(value, sg.Input)]
            input = all(map(str.strip, [values[key] for key in input_key_list]))

            if event == 'Next >' and input == False:
                window1['-STATUS-'].update( "Please Enter a valid folder name")

            if event == 'Next >' and window2 is None and input == True:
                Folder_Name = values['-FOLDER_NAME-']
                Folder_Name = ge.relative_path(Folder_Name)
                window1['-STATUS-'].update( "")
                window1.hide()
                window2 = make_window2()
            elif event == 'Next >' and window2 is not None and input == True:
                window1['-STATUS-'].update( "")
                window2.un_hide()
                window1.hide()


        if window == window2:
            input_key_list = [key for key, value in window.key_dict.items()
                              if isinstance(value, sg.Combo)]
            input = all(map(str.strip, [values[key] for key in input_key_list]))
            if event == 'Next >' and input == False:
                window2['-STATUS-'].update("Please choose a vaild ITBU and Env to Deploy to")
            if event == 'Next >' and input == True:
                ITBU = values['-ITBU-']
                ENV = values['-ENVLIST-']
                ge.generate_env_file(Folder_Name,ITBU,ENV)
                window2.hide()
                window3 = make_window3()
            elif event in (sg.WIN_CLOSED, '< Prev'):
                window2.hide()
                window1.un_hide()

        if window == window3:
            if event == 'Next >':
                window3.hide()
                window4 = make_window4()
            elif event in (sg.WIN_CLOSED, '< Prev'):
                window3.hide()
                window2.un_hide()
            elif event == '-ADD-':
                name,value,type,desc = values['-NAME-'],values['-VALUE-'],values['-TYPE-'],values['-DESC-']
                data.append([name,value,type,desc])
                print(data)
                window['-TABLE-'].update(values=data[1:][:])
            elif event[0] == '-TABLE-':
                rowNum = event[2][0]
            elif event == '-REMOVE-':
                if rowNum is not None and  rowNum > -1 :
                    data.pop(rowNum)
                    window['-TABLE-'].update(values=data[1:][:])
            elif event == '-GEN-':
                ge.generate_csv_file(data)




        if window == window4:
            if event == '< Prev':
                window3.un_hide()
                window4.hide()
            elif event in ("Exit",sg.WIN_CLOSED):
                window3.close()
                window4.close()
                break

    window.close()
main()
# if "__name__" == '__main__':
#     main()