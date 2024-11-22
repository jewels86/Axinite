import dearpygui.dearpygui as dpg

def gui():
    dpg.create_context()
    dpg.create_viewport(title="Axinite", width=1000, height=600)
    dpg.setup_dearpygui()
    
    with dpg.window(label="Axinite"):
        dpg.add_text("Hello, world!")

    dpg.show_viewport()
    
    while dpg.is_dearpygui_running():
        dpg.render_dearpygui_frame()
    
    dpg.destroy_context()