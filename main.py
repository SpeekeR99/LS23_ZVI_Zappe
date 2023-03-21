import numpy as np
import cv2
from OpenGL.GL import *
import glfw
import imgui
from imgui.integrations.glfw import GlfwRenderer
import wx

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
fullscreen = False
show_settings_window = False
show_about_window = False
show_edge_detection_window = False
show_save_as_dialog = False
current_img = 0
imgs = {}


def impl_glfw_init():
    window_name = "Main Window"

    if not glfw.init():
        print("Could not initialize OpenGL context")
        exit(1)

    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)

    glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, GL_TRUE)
    glfw.window_hint(glfw.RESIZABLE, GL_FALSE)

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
    texture = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, img.shape[1], img.shape[0], 0, GL_RGB, GL_UNSIGNED_BYTE, img)
    glBindTexture(GL_TEXTURE_2D, 0)
    return texture


def show_image(name):
    global imgs
    imgui.set_next_window_size(imgs[name]["img"].shape[1] + 15, imgs[name]["img"].shape[0] + 35, imgui.ONCE)
    _, close_bool = imgui.begin(name, True, imgui.WINDOW_NO_RESIZE)
    # window_size = imgui.get_window_size()
    # dx = window_size[0] - 15 - imgs[name]["original_size"][0]
    # dy = window_size[1] - 35 - imgs[name]["original_size"][1]
    # scale = min((imgs[name]["original_size"][0] + dx) / (imgs[name]["original_size"][0]), (imgs[name]["original_size"][1] + dy) / (imgs[name]["original_size"][1]))
    # if dx or dy:
    #     imgs[name]["img"] = cv2.resize(imgs[name]["img"], (int(imgs[name]["original_size"][0] * scale), int(imgs[name]["original_size"][1] * scale)))
    imgui.image(imgs[name]["texture"], imgs[name]["img"].shape[1], imgs[name]["img"].shape[0])
    imgui.end()
    return close_bool


def load_image(filepath):
    global imgs
    filepath = filepath.replace("\\", "/")
    try:
        img = cv2.imread(filepath, cv2.IMREAD_COLOR)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    except Exception:
        print("Error loading image: " + filepath + "!")
        return
    name = filepath.split("/")[-1].split(".")[0]
    extension = filepath.split("/")[-1].split(".")[-1]
    copy = 1
    while name + "." + extension in imgs:
        if copy == 1:
            name = name + " (1)"
        else:
            name = name[:-3]
            name = name + "(" + str(copy) + ")"
        copy += 1
    name = name + "." + extension
    imgs[name] = {"img": img, "texture": texture_image(img), "show": True, "original_size": (img.shape[1], img.shape[0])}


def main():
    global WINDOW_WIDTH, WINDOW_HEIGHT, fullscreen, show_settings_window, show_about_window, show_edge_detection_window, show_save_as_dialog, imgs, current_img

    app = wx.App()
    app.MainLoop()
    imgui.create_context()
    imgui.style_colors_dark()
    window = impl_glfw_init()
    impl = GlfwRenderer(window)
    mode = glfw.get_video_mode(glfw.get_primary_monitor())

    to_be_deleted = None

    while not glfw.window_should_close(window):
        glfw.poll_events()
        impl.process_inputs()

        imgui.new_frame()

        if imgui.begin_main_menu_bar():
            if imgui.begin_menu("File"):
                clicked_new, _ = imgui.menu_item("New Blank Project", None, False, True)
                if clicked_new:
                    imgs = {}
                    show_edge_detection_window = False
                    show_about_window = False
                    show_settings_window = False

                clicked_load, _ = imgui.menu_item("Load Image...", None, False, True)
                if clicked_load:
                    filepath = wx.FileSelector("Load Image", wildcard="Image Files (*.png;*.jpg;*.jpeg;*.bmp)|*.png;*.jpg;*.jpeg;*.bmp")
                    if filepath:
                        load_image(filepath)

                clicked_save, _ = imgui.menu_item("Save Image as...", None, False, True)
                if clicked_save:
                    show_save_as_dialog = True

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

        if to_be_deleted:
            glDeleteTextures(1, [imgs[to_be_deleted]["texture"]])
            imgs.pop(to_be_deleted)
            to_be_deleted = None

        for name in imgs:
            if imgs[name]["show"]:
                imgs[name]["show"] = show_image(name)
                if not imgs[name]["show"]:
                    to_be_deleted = name

        if show_save_as_dialog:
            _, show_save_as_dialog = imgui.begin("Save Image as...", True)
            _, current_img = imgui.combo("Image", current_img, list(imgs.keys()))
            if imgui.button("Save as..."):
                if len(list(imgs.keys())) == 0 or current_img > len(list(imgs.keys())):
                    print("No image selected!")
                else:
                    filepath = wx.FileSelector("Save Image as...", default_filename=list(imgs.keys())[current_img], wildcard="Image Files (*.png;*.jpg;*.jpeg;*.bmp)|*.png;*.jpg;*.jpeg;*.bmp", flags=wx.FD_SAVE)
                    if filepath:
                        img = imgs[list(imgs.keys())[current_img]]["img"]
                        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
                        cv2.imwrite(filepath, img)
            imgui.end()

        if show_edge_detection_window:
            _, show_edge_detection_window = imgui.begin("Edge Detection", True)
            imgui.end()

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

        glClearColor(1., 1., 1., 1)
        glClear(GL_COLOR_BUFFER_BIT)

        imgui.render()
        impl.render(imgui.get_draw_data())
        glfw.swap_buffers(window)

    impl.shutdown()
    glfw.terminate()


if __name__ == "__main__":
    main()
