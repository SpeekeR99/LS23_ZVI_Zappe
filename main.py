import numpy as np
import cv2
import OpenGL.GL as gl
import glfw
import imgui
from imgui.integrations.glfw import GlfwRenderer

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
fullscreen = False
show_settings_window = False
show_about_window = False
show_edge_detection_window = False


def impl_glfw_init():
    window_name = "Main Window"

    if not glfw.init():
        print("Could not initialize OpenGL context")
        exit(1)

    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)

    glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, gl.GL_TRUE)
    glfw.window_hint(glfw.RESIZABLE, gl.GL_FALSE)

    window = glfw.create_window(int(WINDOW_WIDTH), int(WINDOW_HEIGHT), window_name, None, None)
    glfw.make_context_current(window)
    mode = glfw.get_video_mode(glfw.get_primary_monitor())
    glfw.set_window_pos(window, int((mode.size.width - WINDOW_WIDTH) / 2), int((mode.size.height - WINDOW_HEIGHT) / 2))

    if not window:
        glfw.terminate()
        print("Could not initialize Window")
        exit(1)

    return window


def texture_image(img):
    texture = gl.glGenTextures(1)
    gl.glBindTexture(gl.GL_TEXTURE_2D, texture)
    gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_S, gl.GL_CLAMP_TO_EDGE)
    gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_T, gl.GL_CLAMP_TO_EDGE)
    gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_LINEAR)
    gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_LINEAR)
    gl.glTexImage2D(gl.GL_TEXTURE_2D, 0, gl.GL_RGB, img.shape[1], img.shape[0], 0, gl.GL_RGB, gl.GL_UNSIGNED_BYTE, img)
    return texture


def show_image(texture, img, window_name="Image"):
    _, close_bool = imgui.begin(window_name, True)
    imgui.image(texture, img.shape[1], img.shape[0])
    imgui.end()
    return close_bool


def main():
    global WINDOW_WIDTH, WINDOW_HEIGHT, fullscreen, show_settings_window, show_about_window, show_edge_detection_window

    imgui.create_context()
    window = impl_glfw_init()
    impl = GlfwRenderer(window)

    mode = glfw.get_video_mode(glfw.get_primary_monitor())

    img = cv2.imread("img/lenna.png", cv2.IMREAD_COLOR)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    texture = texture_image(img)

    while not glfw.window_should_close(window):
        glfw.poll_events()
        impl.process_inputs()

        imgui.new_frame()

        if imgui.begin_main_menu_bar():
            if imgui.begin_menu("File"):
                clicked_new, _ = imgui.menu_item("New Blank Project", None, False, True)
                if clicked_new:
                    pass

                clicked_load, _ = imgui.menu_item("Load Image...", None, False, True)
                if clicked_load:
                    pass

                clicked_save, _ = imgui.menu_item("Save Image as...", None, False, True)
                if clicked_save:
                    pass

                imgui.separator()

                clicked_exit, _ = imgui.menu_item("Exit", 'Alt+F4', False, True)
                if clicked_exit:
                    glfw.set_window_should_close(window, True)

                imgui.end_menu()
            if imgui.begin_menu("Edit"):
                clicked_back, _ = imgui.menu_item("Back", None, False, True)
                if clicked_back:
                    pass

                imgui.separator()

                clicked_edge_detect, _ = imgui.menu_item("Edge Detection...", None, False, True)
                if clicked_edge_detect:
                    show_edge_detection_window = True

                imgui.end_menu()
            if imgui.begin_menu("Settings"):

                clicked_settings, _ = imgui.menu_item("Window Settings...", None, False, True)
                if clicked_settings:
                    show_settings_window = True

                imgui.end_menu()
            if imgui.begin_menu("Help"):

                clicked_about, _ = imgui.menu_item("About...", None, False, True)
                if clicked_about:
                    show_about_window = True

                imgui.end_menu()
            imgui.end_main_menu_bar()



        if show_settings_window:
            imgui.set_next_window_size(400, 200, imgui.ONCE)
            imgui.set_next_window_position(int((WINDOW_WIDTH - 400) / 2), int((WINDOW_HEIGHT - 200) / 2), imgui.ONCE)
            _, show_settings_window = imgui.begin("Settings", True)
            imgui.text("Window Settings")
            if imgui.button("Set 1280x720"):
                WINDOW_WIDTH = 1280
                WINDOW_HEIGHT = 720
                glfw.set_window_size(window, WINDOW_WIDTH, WINDOW_HEIGHT)
                glfw.set_window_pos(window, int((mode.size.width - WINDOW_WIDTH) / 2),
                                    int((mode.size.height - WINDOW_HEIGHT) / 2))
            imgui.same_line()
            if imgui.button("Set 1600x900"):
                WINDOW_WIDTH = 1600
                WINDOW_HEIGHT = 900
                glfw.set_window_size(window, WINDOW_WIDTH, WINDOW_HEIGHT)
                glfw.set_window_pos(window, int((mode.size.width - WINDOW_WIDTH) / 2),
                                    int((mode.size.height - WINDOW_HEIGHT) / 2))
            imgui.same_line()
            if imgui.button("Set 1920x1080"):
                WINDOW_WIDTH = 1920
                WINDOW_HEIGHT = 1080
                glfw.set_window_size(window, WINDOW_WIDTH, WINDOW_HEIGHT)
                glfw.set_window_pos(window, int((mode.size.width - WINDOW_WIDTH) / 2),
                                    int((mode.size.height - WINDOW_HEIGHT) / 2))
            imgui.same_line()
            if fullscreen:
                if imgui.button("Windowed"):
                    fullscreen = False
                    WINDOW_WIDTH = 1280
                    WINDOW_HEIGHT = 720
                    glfw.set_window_monitor(window, None, 0, 0, WINDOW_WIDTH, WINDOW_HEIGHT, 0)
                    glfw.set_window_pos(window, int((mode.size.width - WINDOW_WIDTH) / 2),
                                        int((mode.size.height - WINDOW_HEIGHT) / 2))
            else:
                if imgui.button("Fullscreen"):
                    fullscreen = True
                    WINDOW_WIDTH = mode.size.width
                    WINDOW_HEIGHT = mode.size.height
                    glfw.set_window_monitor(window, glfw.get_primary_monitor(), 0, 0, WINDOW_WIDTH, WINDOW_HEIGHT,
                                            mode.refresh_rate)
            imgui.end()

        if show_about_window:
            imgui.set_next_window_size(300, 100, imgui.ALWAYS)
            imgui.set_next_window_position(int((WINDOW_WIDTH - 300) / 2), int((WINDOW_HEIGHT - 100) / 2), imgui.ALWAYS)
            _, show_about_window = imgui.begin("About", True, imgui.WINDOW_ALWAYS_AUTO_RESIZE | imgui.WINDOW_NO_SAVED_SETTINGS | imgui.WINDOW_NO_NAV | imgui.WINDOW_NO_COLLAPSE)
            imgui.text("This application was made by:\nDominik Zappe")
            imgui.end()

        gl.glClearColor(1., 1., 1., 1)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)

        imgui.render()
        impl.render(imgui.get_draw_data())
        glfw.swap_buffers(window)

    impl.shutdown()
    glfw.terminate()


if __name__ == "__main__":
    main()
