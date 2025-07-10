


import cv2
import numpy as np
import pandas as pd
import joblib



import time
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression

import matplotlib.pyplot as plt
from matplotlib.patches import Circle

from pylablib.devices import Thorlabs

from my_Linear import LinearStage




Thorlabs.list_cameras_tlcam()
cam = Thorlabs.ThorlabsTLCamera(serial="32756")
cam.set_roi(0, 1440, 0, 1080, 1, 1)


frame = cam.snap()
image_array = np.array(frame, dtype=np.uint8)
plt.imshow(image_array)
plt.colorbar()




ls = LinearStage()
lls = ls.find_devices()
print(lls)
info = ls.connect(lls[0])
print(info)




columns = ['position', 'image']
measurements_df = pd.DataFrame(columns=columns)




for pos in range(0, 47, 1):
    curr_pos = ls.move(pos)
    print(curr_pos)

    frame = cam.snap()
    image_array = np.array(frame, dtype=np.uint8)
    
    # Append to DataFrame
    new_row = pd.DataFrame({
        'position': [curr_pos],
        'image': [image_array]
    })
    measurements_df = pd.concat([measurements_df, new_row], ignore_index=True)

    # plt.imshow(image_array)
    # plt.colorbar()
    # plt.title(curr_pos)
    # plt.show()

    time.sleep(0.2)

measurements_df = joblib.load('./data/z_stage/z_stage_df.joblib')




measurements_df.head()


for i, row in measurements_df.iterrows():
    image = row['image']
    plt.imshow(image)
    plt.show()
    break


def normalize_images_to_max(df):
    # Create a new column for normalized images
    df['image_normalized'] = None
    
    # Process each image
    for idx, row in df.iterrows():
        image = row['image']
        
        normalized_image = np.maximum(image, 240)
        
        # Store normalized image in DataFrame
        df.at[idx, 'image_normalized'] = normalized_image
    
    return df


measurements_df = normalize_images_to_max(measurements_df)



def estimate_beam_parameters(image):
    # Convert image to grayscale if it isn't already
    if len(image.shape) == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    else:
        gray = image
    
    # Apply threshold to isolate the bright beam (adjust threshold as needed)
    _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
    # Find contours
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    if len(contours) == 0:
        return None  # No beam found
    
    # Get the largest contour (assumed to be the beam)
    largest_contour = max(contours, key=cv2.contourArea)
    
    # Fit an ellipse to the contour
    if len(largest_contour) >= 5:  # Need at least 5 points to fit an ellipse
        ellipse = cv2.fitEllipse(largest_contour)
        (center_x, center_y), (major_axis, minor_axis), angle = ellipse
        
        # Calculate radius (average of major and minor axes for approximation)
        radius = (major_axis + minor_axis) / 4.0  # Divide by 2 to get radius, then average
        
        return {
            'center_x': center_x,
            'center_y': center_y,
            'radius': radius,
            'major_axis': major_axis / 2.0,
            'minor_axis': minor_axis / 2.0,
            'angle': angle
        }
    else:
        return None  # Not enough points to fit ellipse

# Process all images in the DataFrame
def process_images(df):
    # Initialize new columns for parameters
    df['center_x'] = np.nan
    df['center_y'] = np.nan
    df['radius'] = np.nan
    df['major_axis'] = np.nan
    df['minor_axis'] = np.nan
    df['angle'] = np.nan
    
    # Process each image
    for idx, row in df.iterrows():
        # params = estimate_beam_parameters(row['image'])
        params = estimate_beam_parameters(row['image_normalized'])
        if params:
            df.at[idx, 'center_x'] = params['center_x']
            df.at[idx, 'center_y'] = params['center_y']
            df.at[idx, 'radius'] = params['radius']
            df.at[idx, 'major_axis'] = params['major_axis']
            df.at[idx, 'minor_axis'] = params['minor_axis']
            df.at[idx, 'angle'] = params['angle']
    
    return df




measurements_df = process_images(measurements_df)
measurements_df.head()


for i, row in measurements_df.iterrows():
    fig, ax = plt.subplots()
    image = row['image']  # Use the original image
    # image = row['image_normalized']
    center_x = row['center_x']
    center_y = row['center_y']
    radius = row['radius']

    circle = Circle((center_x, center_y), radius, color='purple', alpha=0.7)

    ax.add_patch(circle)
    plt.imshow(image)
    plt.title(f"({center_x:.1f}, {center_y:.1f}), radius={radius:.1f}")
    plt.show()
    break


df = measurements_df#[:-25]

# convert center and radius to mm, pixel size is 3.45um
df['center_x_mm'] = df['center_x'] * 3.45e-3
df['center_y_mm'] = df['center_y'] * 3.45e-3
df['radius_mm'] = df['radius'] * 3.45e-3


X = df['position'].values.reshape(-1, 1)  # Reshape for sklearn
y = df['radius_mm'].values

# Fit linear model
model = LinearRegression()
model.fit(X, y)

# Get slope and intercept
slope = model.coef_[0]
intercept = model.intercept_

# Generate points for the fitted line
x_fit = np.linspace(X.min(), X.max(), 100).reshape(-1, 1)
y_fit = model.predict(x_fit)

# Calculate R-squared
r_squared = model.score(X, y)

# Create scatter plot with fitted line
plt.figure(figsize=(10, 6))
plt.scatter(df['position'], df['radius_mm'], color='blue', label='Data')
plt.plot(x_fit, y_fit, color='red', label=f'Fit: y = {slope:.2f}x + {intercept:.2f}\nR² = {r_squared:.3f}')

# Add labels and title
plt.xlabel('Position (mm)')
plt.ylabel('Radius (mm)')
plt.title('Beam Radius vs. Position with Linear Fit')
plt.grid(True)
plt.legend()

# Show the plot
plt.show()

print(f"Slope: {slope:.2f}")