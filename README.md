# Red Eye Line - Face Anonymization Tool

A web-based application for real-time face anonymization using MediaPipe's face detection and mesh capabilities. This tool provides two anonymization techniques: face blurring and eye covering.

## 🚀 Features

- **Face Blur**: Automatically detect and blur faces in uploaded images
- **Eye Cover**: Draw red lines over detected eyes for privacy protection
- **Real-time Processing**: Instant image processing with MediaPipe
- **Download Support**: Save processed images with custom naming
- **Responsive Design**: Works on desktop and mobile devices
- **Multiple Format Support**: Upload JPG, JPEG, and PNG images

## 🛠️ Technologies Used

- **Streamlit** - Web application framework
- **MediaPipe** - Face detection and mesh analysis
- **OpenCV** - Image processing and manipulation
- **NumPy** - Numerical computations
- **Pillow** - Image handling

## 📋 Prerequisites

- Python 3.10 or higher
- pip package manager

## 🚀 Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd redlines
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   streamlit run app.py
   ```

4. **Open your browser**
   Navigate to `http://localhost:8501`

## 📖 Usage

1. **Select Anonymization Type**
   - Choose between "Face-Blur" or "Cover-Eyes" options

2. **Upload Image**
   - Click "Browse files" to upload an image (JPG, JPEG, PNG)
   - The application will automatically process the image

3. **View Results**
   - The anonymized image will be displayed below the upload area
   - Use the "Download Image" button to save the processed image

## 🔧 How It Works

### Face Blur
- Uses MediaPipe's BlazeFace short-range model for face detection
- Applies Gaussian blur to detected face regions
- Preserves image quality while ensuring privacy

### Eye Cover
- Utilizes MediaPipe's Face Mesh for precise facial landmark detection
- Draws red lines over detected eye positions
- Adapts line thickness based on face size

## 📁 Project Structure

```
redlines/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── runtime.txt           # Python version specification
├── blaze_face_short_range.tflite  # MediaPipe face detection model
├── assets/               # Sample images and assets
│   ├── Humans.png
│   ├── Humans-Face-Blur.png
│   ├── Humans-Cover-Eyes.png
│   └── image.png
└── README.md            # This file
```

## 🎯 Use Cases

- **Privacy Protection**: Anonymize faces in photos before sharing
- **Content Creation**: Create privacy-compliant content
- **Research**: Process images for academic or research purposes
- **Social Media**: Prepare images for platforms with privacy concerns

## 🔒 Privacy & Security

- All processing is done locally on your device
- No images are uploaded to external servers
- Temporary processing only - no data is stored

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **MediaPipe** for providing excellent face detection and mesh capabilities
- **Streamlit** for the intuitive web application framework
- **OpenCV** for robust image processing tools

## 📞 Support

If you encounter any issues or have questions, please open an issue on the repository.

---

**Note**: This application requires the `blaze_face_short_range.tflite` model file to function properly. Ensure it's present in the project root directory.
