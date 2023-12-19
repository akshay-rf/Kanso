from ultralytics import YOLO
import torch
import cv2
from tkinter import *
from tkinter import filedialog
import ttkbootstrap as tb
from ttkbootstrap.constants import *
from ttkbootstrap.dialogs.colorchooser import ColorChooserDialog
from ttkbootstrap.dialogs.dialogs import Messagebox
import webbrowser
import numpy as np
import random
import extcolors
from PIL import ImageTk, Image


MODEL = YOLO('best.pt')


class Kanso(tb.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.pack(fill=BOTH, expand=YES)

        self.style = tb.Style()
        self.style.configure("C.TButton")

        self.MENU = True
        self.ORIGINAL_IMAGE=""
        self.COLOR = "#ff0000"
        self.TEXTURE = "Orange Peel"
        self.TEX_DIC = {
                        "Orange Peel":"textures/orange-peel.jpg",
                        "Knockdown": "textures/knockdown.jpg",
                        "Skip Trowel": "textures/skip-trowel.jpg",
                        "Slap Brush": "textures/slap-brush.jpg",
                        "Swirl":"textures/swirl.jpg",
                        "Venetian": "textures/venetian.jpg",
                        "Sand": "textures/sand.JPG",
                        "Brick": "textures/brick.jpg",
                        "Wood": "textures/wood.jpg"
                        }
        self.COLOR_DIC = {
                        'Red': '#FF0000',
                        'Green': '#00FF00',
                        'Blue': '#0000FF',
                        'Yellow': '#FFFF00',
                        'Purple': '#800080',
                        'Orange': '#FFA500'
                    }
        self.paintMode = False
        self.no_normal = False

        self.columnconfigure(0, weight=3)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)

        self.dff = tb.Frame(self, padding=10)
        self.dff.pack(fill=X, expand=YES)

        self.df = tb.Labelframe(self.dff, padding=30)
        self.df.pack(fill=Y)

        self.title_canvas = tb.Canvas(self.df)
        self.title_canvas.pack(fill=BOTH)

        self.title = ImageTk.PhotoImage(file="title.png")
        self.subtitle = ImageTk.PhotoImage(file="subtitle.png")
        self.title_label = tb.Label(self.title_canvas, image=self.title)
        self.title_label.pack()

        tb.Label(self.title_canvas, image=self.subtitle).pack()

        temp = tb.Labelframe(self.df, text="Get Started", padding=10)
        temp.pack(fill=Y, expand=YES, padx=10, pady=10)
        tb.Button(temp, bootstyle="success", text="Open Image", command=self.load_image).pack(pady=10, padx=10, fill=X)
        tb.Label(temp, text="Kanso: Your virtual decorator for experimenting with wall colors, textures, and an AI painter for personalized room transformations.").pack(pady=10, padx=10)
        tb.Label(temp, text="Built By Akshay RF").pack(pady=10, padx=10)
        
        tempp = tb.Frame(temp, padding=10)
        tempp.pack(fill=X)
        tempp.columnconfigure(0, weight=1)
        tempp.columnconfigure(1, weight=1)
        tempp.columnconfigure(2, weight=1)

        tb.Button(tempp, bootstyle="outline", text="Support", command=lambda: webbrowser.open("https://github.com/akshay-rf")).grid(row=0,column=0, sticky="nsew", padx=10)
        tb.Button(tempp, bootstyle="warning-outline", text="Fork", command=lambda: webbrowser.open("https://github.com/akshay-rf/Kanso/")).grid(row=0,column=1, sticky="nsew", padx=10)
        tb.Button(tempp, bootstyle="info-outline", text="Lisence", command=lambda: webbrowser.open("https://github.com/akshay-rf/Kanso/blob/main/LICENSE")).grid(row=0,column=2, sticky="nsew", padx=10)

    def create_widgets(self):
        col1 = tb.Frame(self, padding=10)
        col1.grid(row=0, column=0, sticky=NSEW)

        self.image_info = tb.Labelframe(col1, text="Image", padding=10)
        self.image_info.pack(side=TOP, fill=BOTH, expand=YES)

        self.canvas = tb.Canvas(self.image_info)
        self.canvas.pack()

        self.image_label = tb.Label(self.canvas)
        self.image_label.pack()

        col2 = tb.Frame(self, padding=10)
        col2.grid(row=0, column=1, sticky=NSEW)

        control_info = tb.Labelframe(col2, text="Controls", padding=10)
        control_info.pack(side=TOP, fill=BOTH, expand=YES)

        open_file = tb.Button(
            master=control_info,
            text='Open Image',
            compound=BOTTOM,
            command=self.load_image
        )
        open_file.pack(padx=10, pady=10, fill=X)

        color_set_frame = tb.Labelframe(control_info, text="Color", padding=10)
        color_set_frame.pack(side=TOP, fill=BOTH, pady=10, expand=YES)


        self.colors = ['Red', 'Green', 'Blue', 'Yellow', 'Purple', 'Orange']
        self.color_combobox = tb.Combobox(color_set_frame, values=self.colors)
        self.color_combobox.pack(padx=10,pady=10, fill=X)
        self.color_combobox.set("Red")

        self.cd = ColorChooserDialog()

        self.pick_color_button = tb.Button(color_set_frame, text="Custom Color", style="C.TButton", command=self.pick_color)
        self.pick_color_button.pack(padx=10, pady=10, fill=X)

        texture_set_frame = tb.Labelframe(control_info, text="Texture", padding=10)
        texture_set_frame.pack(side=TOP, fill=BOTH, pady=10, expand=YES)

        self.textures = ['Orange Peel', 'Knockdown', 'Skip Trowel', 'Slap Brush', 'Swirl', 'Venetian', 'Sand', 'Brick', 'Wood']
        self.texture_combobox = tb.Combobox(texture_set_frame, values=self.textures)
        self.texture_combobox.pack(padx=10,pady=10, fill=X)
        self.texture_combobox.set("Orange Peel")

        pick_texture_button = tb.Button(texture_set_frame, text="Custom Texture", command=self.pick_texture)
        pick_texture_button.pack(padx=10, pady=10, fill=X)

        paint_frame = tb.Labelframe(control_info, text="Paint", padding=10)
        paint_frame.pack(side=TOP, fill=BOTH, pady=10, expand=YES)
        paint_frame.columnconfigure(0, weight=1)
        paint_frame.columnconfigure(1, weight=1)

        self.var = IntVar()
        
        self.color = tb.Checkbutton(paint_frame, bootstyle="square-toggle",
            text="Color",
            variable=self.var,
            onvalue=1,
            offvalue=0)
        self.color.grid(row=0, column=0, padx=10, pady=10)

        self.texture = tb.Checkbutton(paint_frame, bootstyle="square-toggle",
            text="Texture",
            variable=self.var,
            onvalue=0,
            offvalue=1)
        self.texture.grid(row=0, column=1, padx=10, pady=10)

        self.paint_button = tb.Button(paint_frame, text="Paint", command=lambda: self.paint(self.var))
        self.paint_button.grid(row=1, padx=10, pady=10, column=0, columnspan=2, sticky="nsew")

        ai_button = tb.Button(paint_frame, text="AI Paint", command=self.ai_paint)
        ai_button.grid(row=2, padx=10, pady=10, column=0, columnspan=2, sticky="nsew")

        clear_button = tb.Button(paint_frame, text="Clear", command=self.clear)
        clear_button.grid(row=3, padx=10, pady=10, column=0, columnspan=2, sticky="nsew")

        export_frame = tb.Labelframe(control_info, text="Export as", padding=10)
        export_frame.pack(side=TOP, pady=10, fill=BOTH, expand=YES)

        export_jpeg_button = tb.Button(export_frame, text="JPEG", command=self.save_jpeg)
        export_jpeg_button.pack(padx=10, pady=10, fill=X)

        export_png_button = tb.Button(export_frame, text="PNG", command=self.save_png)
        export_png_button.pack(padx=10, pady=10, fill=X)

    def paint(self, var):
        if self.paintMode == True:
            self.config(cursor="")
            self.paintMode = False
            self.paint_button.config(text="Paint")
        else:
            var = var.get()
            if var==1 or var==0:
                self.paintMode = True
                self.paint_button.config(text=f"Cancel {'Color' if var==1 else 'Texture'} Paint")
                self.config(cursor="plus")

    def pick_color(self):
        self.cd.show()
        result = self.cd.result.hex
        self.COLOR = result

        self.style.configure("C.TButton", background=result)
        self.color_combobox.set("Custom")

    def pick_texture(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg;")])
        if file_path:
            self.TEXTURE = file_path
            self.texture_combobox.set("Custom")

    def clear(self):
        self.image_label.config(image=self.original_image)
        self.image = np.array(self.ORIGINAL_IMAGE)[:,:,::-1].copy()

    def save_jpeg(self):
        file_path = filedialog.asksaveasfilename(filetypes=[("JPEG", ".jpg")])
        if file_path:
            print(file_path)
            cv2.imwrite(file_path+".jpg", self.image)
            Messagebox.ok("File saved successfully.", title='Success', alert=False, parent=None,)
        

    def save_png(self):
        file_path = filedialog.asksaveasfilename(filetypes=[("PNG", ".png")])
        if file_path:
            print(file_path)
            cv2.imwrite(file_path+".png", self.image)
            Messagebox.ok("File saved successfully.", title='Success', alert=False, parent=None,)

    def ai_paint(self):
        self.clear()

        tolerance = 32
        limit = 24
        colors, pixel_count = extcolors.extract_from_image(self.ORIGINAL_IMAGE, tolerance, limit)
        
        wall_color = random.choice(colors)
        self.COLOR = '#%02x%02x%02x' % wall_color[0]
        print(self.COLOR)

        i=0
        for contours in self.wall_masks_cv:
            contour = cv2.resize(contours, (1100,750))
            contourC = cv2.cvtColor(contour, cv2.COLOR_GRAY2RGB)

            red = np.ones(contour.shape)
            red = red*255

            masked_image = self.overlay_color(self.image, contour, self.COLOR)
            
            self.masked_image = ImageTk.PhotoImage(image=Image.fromarray(masked_image))
            self.image_label.config(image=self.masked_image, text="")
            self.paintMode = False
            self.config(cursor="")
            i+=1


    def select_mask(self,event):
            x1, y1 = event.x, event.y

            if self.paintMode:
                if self.var.get() == 1:
                    if self.color_combobox.get() in self.colors:
                        self.COLOR = self.COLOR_DIC[self.color_combobox.get()]
                    i=0
                    for contours in self.wall_masks_cv:
                        contour = cv2.resize(contours, (1100,750))
                        contourC = cv2.cvtColor(contour, cv2.COLOR_GRAY2RGB)
                        
                        if contourC[y1,x1].tolist() == [255.0,255.0,255.0]:
                            
                            result_3d = self.overlay_color(self.image, contour, self.COLOR)
                            
                            self.masked_image = ImageTk.PhotoImage(image=Image.fromarray(result_3d))
                            self.image_label.config(image=self.masked_image, text="")
                            self.paintMode = False
                            self.config(cursor="")
                            break
                        i+=1
                else:
                    if self.texture_combobox.get() in self.textures:
                        self.TEXTURE = self.TEX_DIC[self.texture_combobox.get()]

                    else:
                        self.no_normal = True

                    texture = cv2.imread(self.TEXTURE)
                    i=0
                    for contours in self.wall_masks_cv:
                        contour = cv2.resize(contours, (1100,750))
                        contourC = cv2.cvtColor(contour, cv2.COLOR_GRAY2RGB)
                        
                        if contourC[y1,x1].tolist() == [255.0,255.0,255.0]:

                            masked_image = self.overlay_textures(self.image, contour, texture)
                            
                            self.masked_image = ImageTk.PhotoImage(image=Image.fromarray(masked_image))
                            self.image_label.config(image=self.masked_image, text="")
                            self.paintMode = False
                            self.config(cursor="")
                            self.no_normal = False
                            break
                        i+=1

            self.paint_button.config(text="Paint")


    def load_image(self):
        if self.MENU:
            self.dff.destroy()
            self.create_widgets()
            self.image_label.config(text="Loading image, Please wait...", font=("Arial", 28))
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.gif")])
        if file_path:
            image1 = Image.open(file_path)
            image1 = image1.resize((1100, 750), Image.ANTIALIAS)
            self.ORIGINAL_IMAGE = image1
            results = MODEL(image1)
            for result in results:
                masks = result.masks.data
                boxes = result.boxes.data
                clss = boxes[:, 5]
                print(clss)

                wall_indices = torch.where(clss==3)
                wall_masks = masks[wall_indices]
                self.wall_masks_cv = []
                i=0
                for wall in wall_masks:
                    wall_mask = wall * 255
                    wall_mask = wall_mask.cpu().numpy()
                    self.wall_masks_cv.append(wall_mask)
                    i+=1

            
            self.image = np.array(image1)[:,:,::-1].copy()
            self.original_image = ImageTk.PhotoImage(image=image1)
            self.image_label.config(image=self.original_image, text="")
            self.image_label.bind("<Button-1>", self.select_mask)

    def overlay_color(self, image, mask, hex_color):
        bgr_color = np.array([int(hex_color[i:i+2], 16) for i in (1, 3, 5)][::-1]).astype(np.uint8)
        mask = mask.astype(np.uint8)

        result = np.zeros_like(image, dtype=np.uint8)
        result[mask > 0] = bgr_color
        result = cv2.addWeighted(image, 1, result, 0.5, 0)

        self.image = result

        return cv2.cvtColor(result, cv2.COLOR_BGR2RGB)
    
    def overlay_textures(self, image_3d, mask, texture_3d, alpha=1):
        mask = mask.astype(np.uint8)
        normalized_mask = mask.astype(float) / 255.0

        result_3d = np.copy(image_3d)

        repeated_normal_map = self.resize_and_repeat_normal_map(texture_3d, repeat_horizontal=6, repeat_vertical=3).astype(np.uint8)
        repeated_normal_map = cv2.resize(repeated_normal_map, (1100, 750))


        masked_texture = cv2.bitwise_and(repeated_normal_map, repeated_normal_map, mask=mask)

        if not self.no_normal:
            repeated_normal_map = self.add_shadows(result_3d, masked_texture, np.array([-1, -1, -1]))

        result_3d = np.where(normalized_mask[..., None] > 0, repeated_normal_map, result_3d)

        self.image = result_3d

        return cv2.cvtColor(result_3d, cv2.COLOR_BGR2RGB)
    
    def add_shadows(self, image, normal_map, light_direction):
        normal_map = (normal_map / 255.0) * 2 - 1

        nx, ny, nz = cv2.split(normal_map)

        length = np.sqrt(nx**2 + ny**2 + nz**2)
        nx /= length
        ny /= length
        nz /= length

        dot_product = np.maximum(0, -(nx * light_direction[0] + ny * light_direction[1] + nz * light_direction[2]))

        illuminated_texture = image * dot_product[..., np.newaxis]

        illuminated_texture = np.clip(illuminated_texture, 0, 255).astype(np.uint8)

        return illuminated_texture
    

    def resize_and_repeat_normal_map(self, normal_map, repeat_horizontal=6, repeat_vertical=3):
        repeated_normal_map_horizontal = np.tile(normal_map, (1, repeat_horizontal, 1))
        repeated_normal_map = np.tile(repeated_normal_map_horizontal, (repeat_vertical, 1, 1))

        return repeated_normal_map

if __name__ == "__main__":
    root = tb.Window(themename="superhero")
    Kanso(root)
    root.iconbitmap('carp.ico')
    root.title('Kanso簡素')
    root.geometry("1500x850")
    root.mainloop()