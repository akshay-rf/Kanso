
# Kanso簡素

Welcome to Kanso, your ultimate home decor companion! Transform your living spaces virtually, experiment with colors and textures, and let our AI painter suggest and apply the perfect shades for a personalized touch.

## 🌟 Features

- **Virtual Visualization**: See your room come to life by visualizing new decor virtually.
- **Color Customization**: Experiment with a wide range of wall colors to find the perfect match.
- **Texture Selection**: Add textures to your walls to enhance the overall ambiance.
- **AI Painter**: Let our AI painter recommend and apply the best-suited colors for a harmonious look.
## 📌 Requirements

-   Python 3.11.x
-   Pillow
- TTkbootstarp
- Extcolors
- NumPy
- OpenCV
- Torch
- Ultralytics


## 🛠️ Build

1. **Clone the repository:**
   ```bash
   git clone https://github.com/akshay-rf/Kanso.git
   cd Kanso
   ```
2. **Install dependencies:**
	```bash
	pip install -r requirements.txt
	```
 
 3.  **Set up the YOLOv8n model:**
   -   Open the `config.yaml` file in `Model` folder.
  -   Specify and update path for your training, validation and testing dataset.
  - Run the `train.py` script to train your own YOLOv8 model.
4. **Run the script:**
	```bash
	python predict.py
	```

This will set up the necessary files and dependencies to build Kanso locally.

## 🎉 Usage
### 1. Run Kanso 
```bash
	python predict.py
``` 

### 2. Virtual Visualization
- Click on the "Open Image" button to upload a photo of your room.    
![enter image description here](https://i.ibb.co/9vxNfNJ/x1.png)
### 3. Color Customization

- Choose the "Color" option to access the color customization feature.
![enter image description here](https://i.ibb.co/BNXNwnR/x2.png)
- Select a color from the color palette to apply to the walls.
![enter image description here](https://i.ibb.co/gycDKcY/Screenshot-2023-12-19-195527.png)
- Experiment with various colors until you find the perfect one. Toggle Color in the Paint section and Click Paint to paint the walls.
![enter image description here](https://i.ibb.co/6t515ZR/x2.png)
    

### 4. Texture Selection

- Explore the "Textures" section to add textures to your walls.
![enter image description here](https://i.ibb.co/3vd44rk/x3.png)
- Toggle Texture in the Paint section. Click on a wall to apply it to the selected texture after clicking the paint button.
![enter image description here](https://i.ibb.co/5BJTF6H/Screenshot-2023-12-19-201135.png)

### 5. AI Painter

- Activate the "AI Painter" to let our intelligent system recommend the best-suited colors for your room.
![enter image description here](https://i.ibb.co/9wBHrNP/Screenshot-2023-12-19-201520.png)

## 🤖 YOLOv8n Model
The Model used in the app is trained on a dataset of 4200 images. The training dataset included four labels `['People', 'Ceiling', 'Floor', 'Walls']` . Other labels are added for the model to not confuse floor or ceiling with a wall.

![enter image description here](https://i.ibb.co/Wtv9YGf/Box-F1-curve.png)
![enter image description here](https://i.ibb.co/p2HxDvr/Box-P-curve.png)
![enter image description here](https://i.ibb.co/wJD4zFF/Box-PR-curve.png)
![enter image description here](https://i.ibb.co/m6fmR2d/Box-R-curve.png)
![enter image description here](https://i.ibb.co/27Zx8t8/confusion-matrix.png)
![enter image description here](https://i.ibb.co/9VQpgC9/Mask-F1-curve.png)
![enter image description here](https://i.ibb.co/znpsL4p/results.png)

## 🤝 Contributing
We welcome contributions! Feel free to open issues, submit pull requests, or provide feedback.

## 📝 License

This project is licensed under the [MIT License](https://github.com/akshay-rf/Kanso/blob/main/LICENSE).

----------
Happy Decorating with Kanso簡素! 🏡✨
