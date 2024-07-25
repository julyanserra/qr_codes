# QR Shirts

QR Shirts is a web application that allows users to create, manage, and share custom shirts with QR codes. Built with Flask, PostgreSQL, and HTML/JS, this application provides a seamless experience for users to design their own shirts and generate corresponding QR codes. 

It's missing the t-shirt design part, but has all the QR functionality.

## Features

- User authentication (signup, login, logout)
- Create, edit, and delete custom shirts
- Generate QR codes for each shirt
- Upload and manage shirt images
- View a list of all created shirts
- Redirect to custom URLs via QR code scans

## Tech Stack

- Backend: Python 3 with Flask
- Database: PostgreSQL
- Frontend: HTML, JavaScript
- Image Processing: Pillow (PIL)
- QR Code Generation: qrcode
- Image Upload: Cloudinary

## Setup and Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/qr-shirts.git
   cd qr-shirts
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Set up your PostgreSQL database and update the connection details in `db.py`.

4. Set up your Cloudinary account and update the credentials in the appropriate configuration file.

5. Set the necessary environment variables:
   ```
   export FLASK_APP=server.py
   export FLASK_ENV=development
   export SHIRT_HOST=https://yourdomain.com/shirt/
   ```

6. Initialize the database (make sure to create the necessary tables as defined in your schema).

7. Run the application:
   ```
   flask run
   ```

## Usage

1. Navigate to `http://localhost:5000` in your web browser.
2. Sign up for a new account or log in if you already have one.
3. Use the interface to create, edit, or delete shirts.
4. Each shirt will have a unique QR code generated for it.
5. Share the QR codes or use the provided URLs to showcase your shirts.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
