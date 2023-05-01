import numpy as np
import cv2
from OpenGL.GL import *
import glfw
import imgui
from imgui.integrations.glfw import GlfwRenderer
import wx

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720

show_settings_window = False
show_about_window = False
show_edge_detection_window = False
show_save_as_dialog = False

imgs = {}
current_img = 0

edge_detection_methods = ["Defined Direction Edge Detection", "Gradient Magnitude Direction Edge Detection", "Mask Methods", "Laplacian Operator", "Line Detection", "Point Detection", "Canny Edge Detection", "Marr-Hildreth Edge Detection"]
current_edge_detection_method = 0

laplacian_cross = False
laplacian_square = True

canny_lower_thresh = 100
canny_upper_thresh = 200


def impl_glfw_init():
    window_name = "Edge Detection Semestral Work"

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
    glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, img.shape[1], img.shape[0], 0, GL_RGB, GL_UNSIGNED_BYTE, img)
    glBindTexture(GL_TEXTURE_2D, 0)
    return texture


def show_image(name):
    global imgs
    imgui.set_next_window_size(imgs[name]["render_img"].shape[1] + 15, imgs[name]["render_img"].shape[0] + 35, imgui.ONCE)
    _, close_bool = imgui.begin(name, True, imgui.WINDOW_NO_SAVED_SETTINGS | imgui.WINDOW_NO_COLLAPSE)
    window_size = imgui.get_window_size()
    dx = window_size[0] - 15 - imgs[name]["original_size"][0]
    dy = window_size[1] - 35 - imgs[name]["original_size"][1]
    scale = min((imgs[name]["original_size"][0] + dx) / (imgs[name]["original_size"][0]), (imgs[name]["original_size"][1] + dy) / (imgs[name]["original_size"][1]))
    scale = max(scale, 0.01)
    if dx or dy:
        imgs[name]["render_img"] = cv2.resize(imgs[name]["render_img"], (int(imgs[name]["original_size"][0] * scale), int(imgs[name]["original_size"][1] * scale)))
    imgui.image(imgs[name]["texture"], imgs[name]["render_img"].shape[1], imgs[name]["render_img"].shape[0])
    imgui.end()
    return close_bool


def create_render_img_and_texture(img):
    render_img = np.copy(img)
    texture = texture_image(render_img)
    dx = WINDOW_WIDTH * 0.4 - render_img.shape[0]
    dy = WINDOW_HEIGHT * 0.4 - render_img.shape[1]
    if abs(dx) < abs(dy):
        scale = (render_img.shape[0] + dx) / (render_img.shape[0])
    else:
        scale = (render_img.shape[1] + dy) / (render_img.shape[1])
    render_img = cv2.resize(render_img, (int(render_img.shape[1] * scale), int(render_img.shape[0] * scale)))
    return render_img, texture


def avoid_name_duplicates(filepath):
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
    return name + "." + extension


def load_image(filepath):
    global imgs
    filepath = filepath.replace("\\", "/")
    img = cv2.imread(filepath, cv2.IMREAD_COLOR)
    if img is None:
        print("Error loading image: " + filepath + "!")
        return
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    render_img, texture = create_render_img_and_texture(img)
    name = avoid_name_duplicates(filepath)
    imgs[name] = {"img": img, "render_img": render_img, "texture": texture, "show": True, "original_size": (img.shape[1], img.shape[0])}


def my_text_separator(text):
    imgui.separator()
    imgui.text(text)
    imgui.separator()


def defined_direction_edge_detection(img):
    print("defined_direction_edge_detection")
    return img


def gradient_magnitude_direction_edge_detection(img):
    print("gradient_magnitude_direction_edge_detection")
    return img


def mask_methods_edge_detection(img):
    print("mask_methods_edge_detection")
    return img


def laplacian_operator_edge_detection(img):
    img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    kernel = np.ones((3, 3))
    if laplacian_square:
        kernel[1, 1] = -8
    else:
        kernel[0, 0] = 0
        kernel[0, 2] = 0
        kernel[2, 0] = 0
        kernel[2, 2] = 0
        kernel[1, 1] = -4
    kernel = -1 * kernel
    res = cv2.filter2D(img, -1, kernel)
    return res


def line_detection_edge_detection(img):
    print("line_detection_edge_detection")
    return img


def point_detection_edge_detection(img):
    print("point_detection_edge_detection")
    return img


def canny_edge_detection(img):
    print("canny_edge_detection")
    res = cv2.Canny(img, canny_lower_thresh, canny_upper_thresh)
    return res


def marr_hildreth_edge_detection(img):
    print("marr_hildreth_edge_detection")
    return img


def generate_button_callback():
    global imgs
    edge_detection = [defined_direction_edge_detection, gradient_magnitude_direction_edge_detection, mask_methods_edge_detection, laplacian_operator_edge_detection, line_detection_edge_detection, point_detection_edge_detection, canny_edge_detection, marr_hildreth_edge_detection]
    img = imgs[list(imgs.keys())[current_img]]["img"]
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    res = edge_detection[current_edge_detection_method](img)
    res = cv2.cvtColor(res, cv2.COLOR_BGR2RGB)
    render_res, texture = create_render_img_and_texture(res)
    name = avoid_name_duplicates(list(imgs.keys())[current_img].split(".")[0] + " (" + edge_detection_methods[current_edge_detection_method] + ")." + list(imgs.keys())[current_img].split(".")[-1])
    imgs[name] = {"img": res, "render_img": render_res, "texture": texture,
                  "show": True, "original_size": (res.shape[1], res.shape[0])}


def main():
    global WINDOW_WIDTH, WINDOW_HEIGHT, show_settings_window, show_about_window, show_edge_detection_window, show_save_as_dialog, imgs, current_img, current_edge_detection_method, laplacian_kernel_size, laplacian_cross, laplacian_square, canny_lower_thresh, canny_upper_thresh

    app = wx.App()
    app.MainLoop()
    imgui.create_context()
    imgui.style_colors_dark()
    window = impl_glfw_init()
    impl = GlfwRenderer(window)
    mode = glfw.get_video_mode(glfw.get_primary_monitor())

    to_be_deleted = None
    current_style = 0
    background_color = (29. / 255, 29. / 255, 29. / 255)

    while not glfw.window_should_close(window):
        glfw.poll_events()
        impl.process_inputs()

        imgui.new_frame()

        if imgui.begin_main_menu_bar():
            if imgui.begin_menu("File"):
                clicked_new, _ = imgui.menu_item("New Blank Project", None, False, True)
                if clicked_new:
                    sure = wx.MessageDialog(None, "Are you sure you want to create a new project? All unsaved changes will be lost!", "New Project", wx.YES_NO | wx.ICON_QUESTION).ShowModal()
                    if sure == wx.ID_YES:
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
                    sure = wx.MessageDialog(None, "Are you sure you want to delete " + name + "? All unsaved changes will be lost!", "Delete Image", wx.YES_NO | wx.ICON_QUESTION).ShowModal()
                    if sure == wx.ID_YES:
                        to_be_deleted = name
                    else:
                        imgs[name]["show"] = True

        if show_save_as_dialog:
            imgui.set_next_window_size(500, 100, imgui.ONCE)
            imgui.set_next_window_position((WINDOW_WIDTH - 500) / 2, (WINDOW_HEIGHT - 100) / 2, imgui.ONCE)

            _, show_save_as_dialog = imgui.begin("Save Image as...", True, imgui.WINDOW_NO_COLLAPSE)

            imgui.text("Image Selection:")
            _, current_img = imgui.combo("Image", current_img, list(imgs.keys()))

            if imgui.button("Save as..."):
                if len(list(imgs.keys())) == 0 or current_img > len(list(imgs.keys())):
                    print("No image selected!")
                else:
                    filepath = wx.FileSelector("Save Image as...", default_filename=list(imgs.keys())[current_img], wildcard="Image Files (*.png;*.jpg;*.jpeg;*.bmp)|*.png;*.jpg;*.jpeg;*.bmp", flags=wx.FD_SAVE)
                    if filepath:
                        img = imgs[list(imgs.keys())[current_img]]["img"]
                        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                        cv2.imwrite(filepath, img)

            imgui.end()

        if show_edge_detection_window:
            imgui.set_next_window_size(500, 500, imgui.ONCE)
            imgui.set_next_window_position((WINDOW_WIDTH - 500) / 2, (WINDOW_HEIGHT - 500) / 2, imgui.ONCE)

            _, show_edge_detection_window = imgui.begin("Edge Detection", True, imgui.WINDOW_NO_COLLAPSE)

            my_text_separator("Image Selection")
            _, current_img = imgui.combo("Image", current_img, list(imgs.keys()))

            my_text_separator("Edge Detection Method")
            _, current_edge_detection_method = imgui.combo("Edge Detection Method", current_edge_detection_method, edge_detection_methods)

            if current_edge_detection_method == 0:  # Defined Direction
                pass
            elif current_edge_detection_method == 1:  # Gradient Magnitude
                pass
            elif current_edge_detection_method == 2:  # Mask Methods
                pass
            elif current_edge_detection_method == 3:  # Laplacian Operator
                imgui.text("Laplacian Kernel Type:")
                if imgui.radio_button("Cross", laplacian_cross):
                    laplacian_cross = True
                    laplacian_square = False
                if imgui.radio_button("Square", laplacian_square):
                    laplacian_cross = False
                    laplacian_square = True
            elif current_edge_detection_method == 4:  # Line Detection
                pass
            elif current_edge_detection_method == 5:  # Point Detection
                pass
            elif current_edge_detection_method == 6:  # Canny Edge Detection
                imgui.text("Canny Thresholds:")
                old_lower = canny_lower_thresh
                old_upper = canny_upper_thresh
                _, canny_lower_thresh = imgui.slider_int("Lower Threshold", canny_lower_thresh, 0, 254)
                _, canny_upper_thresh = imgui.slider_int("Upper Threshold", canny_upper_thresh, 1, 255)

                if old_lower != canny_lower_thresh and canny_lower_thresh >= canny_upper_thresh:
                    canny_upper_thresh = canny_lower_thresh + 1
                if old_upper != canny_upper_thresh and canny_upper_thresh <= canny_lower_thresh:
                    canny_lower_thresh = canny_upper_thresh - 1
            elif current_edge_detection_method == 7:  # Marr-Hildreth Edge Detection
                pass

            if imgui.button("Generate"):
                if len(list(imgs.keys())) == 0 or current_img > len(list(imgs.keys())):
                    print("No image selected!")
                else:
                    generate_button_callback()

            imgui.end()

        if show_settings_window:
            imgui.set_next_window_size(400, 200, imgui.ONCE)
            imgui.set_next_window_position(int((WINDOW_WIDTH - 400) / 2), int((WINDOW_HEIGHT - 200) / 2), imgui.ONCE)

            _, show_settings_window = imgui.begin("Settings", True, imgui.WINDOW_NO_COLLAPSE | imgui.WINDOW_NO_RESIZE)

            my_text_separator("Window Settings")
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

            my_text_separator("Style Settings")
            _, current_style = imgui.combo("Style", current_style, ["Dark", "Light", "Classic"])

            if current_style == 0:
                imgui.style_colors_dark()
                background_color = (29. / 255, 29. / 255, 29. / 255)
            elif current_style == 1:
                imgui.style_colors_light()
                background_color = (240. / 255, 240. / 255, 240. / 255)
            elif current_style == 2:
                imgui.style_colors_classic()
                background_color = (38. / 255, 38. / 255, 38. / 255)

            imgui.end()

        if show_about_window:
            imgui.set_next_window_size(300, 100, imgui.ALWAYS)
            imgui.set_next_window_position(int((WINDOW_WIDTH - 300) / 2), int((WINDOW_HEIGHT - 100) / 2), imgui.ALWAYS)

            _, show_about_window = imgui.begin("About", True, imgui.WINDOW_ALWAYS_AUTO_RESIZE | imgui.WINDOW_NO_SAVED_SETTINGS | imgui.WINDOW_NO_NAV | imgui.WINDOW_NO_COLLAPSE)
            imgui.text("This application was made by:\nDominik Zappe")

            imgui.end()

        glClearColor(background_color[0], background_color[1], background_color[2], 1)
        glClear(GL_COLOR_BUFFER_BIT)

        imgui.render()
        impl.render(imgui.get_draw_data())
        glfw.swap_buffers(window)

    impl.shutdown()
    glfw.terminate()


if __name__ == "__main__":
    main()
