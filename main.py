import streamlit as st
import sqlite3
import datetime
import calendar
from tips import python_tips
from tips import budget_tips


# Create a function to initialize the database connection and create the table
def init_db():
    conn = sqlite3.connect('todo_db.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS todos
                      (id INTEGER PRIMARY KEY AUTOINCREMENT, date DATE, subject TEXT)''')
    conn.commit()
    conn.close()

init_db()



def month_view():
    # Get the current month and year
    current_date = datetime.datetime.now()
    current_month = current_date.strftime("%B")

    # Create a dictionary to map month names to their numeric values
    month_to_num = {month: num for num, month in enumerate(calendar.month_name) if month}

    # Get the numeric value of the current month
    current_month_num = month_to_num[current_month]

    # Display the name of the current month
    st.write(f"This is the Month View for {current_month}")

    # Add a beautiful image as background (replace 'autumn2.png' with your image)
    st.image('images/autumn2.png', use_column_width=True)

    # Generate the calendar for the current month
    cal = calendar.month(current_date.year, current_month_num)
    st.text(cal)
    
    # Display the money-saving tip for the current month
    # Ensure that you have 12 tips in your budget_tips list
    current_tip = budget_tips[current_month_num - 1]
    st.markdown(
        f'<div class="tip-card">{current_tip}</div>',
        unsafe_allow_html=True
     )

# Create a function for the week view (you can customize this)
def week_view():
    st.write("This is the Week View")
    # Add your week-specific content here

# Initialize the to-do list if it doesn't exist in the session state
if 'todo_list' not in st.session_state:
    st.session_state.todo_list = []

# Create a function for the day view with date selection and to-do list
# Create a function for the day view with date selection and to-do list
def day_view():

     # Get the current month and year
    current_date = datetime.datetime.now()
    current_month = current_date.strftime("%B")
    st.write(f" {current_month}")


    # Allow the user to select a specific date
    selected_date = st.date_input("Select a Date", datetime.date.today())

    # Format the date as "day/month"
    formatted_date = selected_date.strftime("%d/%m")
    # Add a beautiful image as background
    st.image('images/autumn.png', use_column_width=True)

    # Create a to-do list
    st.subheader("To-Do List")
    todo_item = st.text_input("Add a Task")
    if st.button("Add Task"):
        # Save the task to the database
        conn = sqlite3.connect('todo_db.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO todos (date, subject) VALUES (?, ?)", (formatted_date, todo_item))
        conn.commit()
        conn.close()
    
    # Display the saved to-do list from the database
    st.write("Tasks:")
    conn = sqlite3.connect('todo_db.db')
    cursor = conn.cursor()
    cursor.execute("SELECT date, subject FROM todos WHERE date=?", (formatted_date,))
    tasks = cursor.fetchall()
    conn.close()
    
    for task in tasks:
        st.markdown(
            f'<div class="task-card"><p class="task-date">Date: {task[0]}</p><p class="task-subject">Task: {task[1]}</p></div>',
            unsafe_allow_html=True
        )

# Add some basic CSS to style the tasks
st.markdown("""
<style>

* {
font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
font-size:
24px; 
color: #333; }

.custom-title {
    font-size: 28px;
    color: #333;
}

.custom-subheader {
    font-size: 24px;
    color: #555;
}
.task-card {
    background-color: #f0f0f0;
    border: 1px solid #ddd;
    padding: 10px;
    margin: 10px 0;
    border-radius: 5px;
    box-shadow: 0 4px 4px rgba(0, 0, 0, 0.1);
}

.task-date {
    font-weight: bold;
    margin-bottom: 5px;
    color: #333;
}

.task-subject {
    margin-top: 5px;
    color: #555;
}
/* Change sidebar background color */
.css-6qob1r{
    background-color: #fffff; /* Change this to your desired background color */
}

</style>
""", unsafe_allow_html=True)


# Create a sidebar with buttons to switch views
view = st.sidebar.radio("Select a View", ("Month", "Week", "Day"),key="view_selection")

# Display the selected view based on the user's choice
if view == "Month":
    month_view()
elif view == "Week":
    week_view()
else:
    day_view()
    
 
# Get the current day of the year (ranging from 1 to 365)
current_day = datetime.datetime.now().timetuple().tm_yday

st.sidebar.title("Python Tip of the Day")

# Apply the custom CSS to the card
custom_css = """
<style>
   
    .tip-card {
        font-size: 18px;
        background-color: #f0f0f0;
        border-radius: 10px;
        padding: 10px;
        margin: 10px 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# Display the tip within the card
st.sidebar.markdown(f'<div class="tip-card">{python_tips[current_day - 1]}</div>', unsafe_allow_html=True)

