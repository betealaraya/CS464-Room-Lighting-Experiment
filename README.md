# CS464-Room-Lighting-Experiment

## About the Project

This project tests how dark and light rooms affect computer task performance.

We created a Python program using Pygame to measure how quickly and accurately participants complete two computer tasks.

## Tasks

**Task A: Mouse Task**
- Move the mouse cursor into 10 rings.
- The rings appear one at a time.
- The program records how long it takes to finish all 10 rings.

**Task B: Keyboard Task**
- Copy the sentence displayed on the screen.
- Press Enter when finished.
- The program records typing time and the number of errors.

## What You Need

Before running the program, make sure you have:

- Python installed
- VS Code installed
- Pygame installed

## How to Download and Run the Program (Windows)

### Step 1: Download the Code

1. Open this GitHub repository.
2. Click the green **Code** button.
3. Select **Download ZIP**.
4. Extract the ZIP file.
5. Open VS Code.
6. Click **File → Open Folder** and select the extracted folder.

### Step 2: Check Python

In VS Code, click **Terminal → New Terminal**.

Type:

```powershell
py --version
```

If Python is installed, a version number should appear.

If Python is not installed, download it from https://www.python.org/downloads/ and install it.

### Step 3: Install Pygame

In the same VS Code terminal, type:

```powershell
py -m pip install pygame
```

Press Enter and wait for the installation to finish.

You only need to install Pygame once on your computer.

### Step 4: Run the Experiment

Make sure the terminal is inside the project folder.

Type:

```powershell
py CS464_experiment_fixed.py
```

Press Enter.

The program will ask for:

1. **Participant ID:** Enter a test ID such as `P01`.
2. **Room condition:** Type `dark` or `light`.
3. **Task order:** Type `AB` or `BA`.

**AB** means mouse task first, then typing task.

**BA** means typing task first, then mouse task.

A new window will open with the experiment. Follow the instructions on the screen.

### Step 5: View the Results

After completing both tasks, the program saves the results in a file called:

`experiment_results.csv`

The file includes:

- Participant ID
- Room condition
- Task order
- Mouse completion time
- Typing completion time
- Typing errors

You can open the CSV file in Excel to view the results.

## Important Notes

- Run the experiment directly on your computer, not through CSU's remote SSH server.
- Use the same computer and monitor settings when comparing dark and light rooms.
- Do not upload participant results or personal information to this public repository.
- This is a working prototype for our CS464 project.
