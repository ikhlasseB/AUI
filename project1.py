import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(layout="wide")

# Load data
df_quizzes = pd.read_excel(r'C:\Users\HP\Desktop\PTJ\FeatureUseinCourseswithActivity.xlsx', sheet_name='Quizzes')
df_assignments = pd.read_excel(r'C:\Users\HP\Desktop\PTJ\FeatureUseinCourseswithActivity.xlsx', sheet_name='Assignments')
df_Absences = pd.read_excel(r'C:\Users\HP\Desktop\PTJ\FeatureUseinCourseswithActivity.xlsx', sheet_name='Attendance')

# Main title
st.title("Course Count of Quizzes and Assignments Analysis")

# Sidebar title
st.sidebar.title("📌Select a School, Category, and Course")

# Select a school
school_names = df_quizzes["Account Name"].unique()
school = st.sidebar.selectbox("Select a School", ["Select a School"] + list(school_names))

if school != "Select a School":
    st.write(f"**📊 Average Count of Quizzes and Assignments for Each School**")

    # Create an empty list to store data for the DataFrame
    school_avg_count_data = []

    # Calculate average counts for each school
    for school_name in school_names:
        school_df_quizzes = df_quizzes[df_quizzes["Account Name"] == school_name]
        school_df_assignments = df_assignments[df_assignments["Account Name"] == school_name]

        avg_count_quizzes = school_df_quizzes["Count"].mean()
        avg_count_assignments = school_df_assignments["Count2"].mean()

        school_avg_count_data.append({"School": school_name, "Average Count Quizzes": avg_count_quizzes, "Average Count Assignments": avg_count_assignments})

    # Create DataFrame
    school_avg_count_df = pd.DataFrame(school_avg_count_data)

    # Create bar chart for schools
    bar_names = ["Quizzes", "Assignments"]
    dataframes = [school_avg_count_df[["School", "Average Count Quizzes"]], school_avg_count_df[["School", "Average Count Assignments"]]]
    fig_school = go.Figure()

    for bar_name, df in zip(bar_names, dataframes):
        fig_school.add_trace(go.Bar(x=df["School"], y=df[f"Average Count {bar_name}"], name=bar_name,
                                    marker_color='#009639' if bar_name == "Quizzes" else 'lightgray'))

    # Update layout
    fig_school.update_layout(barmode='group', xaxis_tickangle=-45, xaxis_title='School', yaxis_title='Average Count')

    # Display chart
    st.plotly_chart(fig_school)


if school != "Select a School":
    category_mapping = {
        "Business Administration": [("Entrepreneurship", "MGT"), ("Accounting", "ACC"), ("Statistics", "GBU"), ("Marketing", "MKT")],
        "Humanities and Social Sciences": [("Writing", "ENG"), ("Psychology", "PSY"), ("Arabic Literature", "ARB"), ("Research", "SSC"), ("Academic Skills", "FAS")],
        "Language Center": [("Korean", "KOR"), ("Spanish", "SPN")],
        "Science and Engineering": [("Mathematics", "MTH"), ("Physics", "PHY"), ("Engineering", "ENG")]
    }

    category = st.sidebar.selectbox("Select a Category", ["Select a Category"] + [item[0] for item in category_mapping[school]])

    if category != "Select a Category":
        st.write(f"**📊 Average Count of Quizzes and Assignments for Each Category**")
        selected_category = next(item[1] for item in category_mapping[school] if item[0] == category)

        # Create an empty list to store data for the DataFrame
        category_avg_count_data = []

        for cat_name, cat_code in category_mapping[school]:
            category_df_quizzes = df_quizzes[(df_quizzes["Account Name"] == school) & (df_quizzes["Course Name"].str[5:8] == cat_code)]
            category_df_assignments = df_assignments[(df_assignments["Account Name"] == school) & (df_assignments["Course Name"].str[5:8] == cat_code)]

            # Calculate the average count for quizzes and assignments for the category
            avg_count_quizzes = category_df_quizzes["Count"].mean()
            avg_count_assignments = category_df_assignments["Count2"].mean()

            # Append data as dictionaries to the list
            category_avg_count_data.append({"Category": cat_name, "Average Count Quizzes": avg_count_quizzes, "Average Count Assignments": avg_count_assignments})

        # Create the DataFrame from the list of dictionaries
        category_avg_count_df = pd.DataFrame(category_avg_count_data)

        # Create a list of bar names
        bar_names = ["Quizzes", "Assignments"]

        # Create a list of dataframes
        dataframes = [category_avg_count_df[["Category", "Average Count Quizzes"]], category_avg_count_df[["Category", "Average Count Assignments"]]]

        # Create a grouped bar chart using Plotly for categories
        fig_category = go.Figure()

        # Iterate over the bar names and dataframes to add traces
        for bar_name, df in zip(bar_names, dataframes):
            fig_category.add_trace(go.Bar(x=df["Category"], y=df[f"Average Count {bar_name}"], name=bar_name,
                                          marker_color='#009639' if bar_name == "Quizzes" else 'lightgray'))

        # Update layout to show grouped bars
        fig_category.update_layout(barmode='group', xaxis_tickangle=-45, xaxis_title='Category', yaxis_title='Average Count')

        st.plotly_chart(fig_category)

        new_df1_quizzes = df_quizzes[(df_quizzes["Account Name"] == school) & (df_quizzes["Course Name"].str[5:8] == selected_category)]
        new_df1_assignments = df_assignments[(df_assignments["Account Name"] == school) & (df_assignments["Course Name"].str[5:8] == selected_category)]
        course_names = new_df1_quizzes["Course Name"]
        course = st.sidebar.selectbox("Select a Course", ["Select a Course"] + list(course_names))

        course_avg_count_data = []

        for course_name in course_names:
            course_df_quizzes = new_df1_quizzes[new_df1_quizzes["Course Name"] == course_name]
            course_df_assignments = new_df1_assignments[new_df1_assignments["Course Name"] == course_name]

            # Calculate the average count for quizzes and assignments for the course
            avg_count_quizzes = course_df_quizzes["Count"].mean()
            avg_count_assignments = course_df_assignments["Count2"].mean()

            # Append data as dictionaries to the list
            course_avg_count_data.append({"Course": course_name, "Average Count Quizzes": avg_count_quizzes, "Average Count Assignments": avg_count_assignments})

        # Create the DataFrame from the list of dictionaries
        course_avg_count_df = pd.DataFrame(course_avg_count_data)

        # Create a list of bar names
        bar_names = ["Quizzes", "Assignments"]

        # Create a list of dataframes
        dataframes = [course_avg_count_df[["Course", "Average Count Quizzes"]], course_avg_count_df[["Course", "Average Count Assignments"]]]

        # Create a grouped bar chart using Plotly for courses
        fig_course = go.Figure()

        # Iterate over the bar names and dataframes to add traces
        for bar_name, df in zip(bar_names, dataframes):
            fig_course.add_trace(go.Bar(x=df["Course"], y=df[f"Average Count {bar_name}"], name=bar_name,
                                        marker_color='#009639' if bar_name == "Quizzes" else 'lightgray'))

        # Update layout to show grouped bars
        fig_course.update_layout(barmode='group', xaxis_tickangle=-45, xaxis_title='Course', yaxis_title='Average Count')
        st.write(f"**📊 Average Count of Quizzes and Assignments for Each Course**")
        st.plotly_chart(fig_course)

        if course != "Select a Course":
            course_df_quizzes = new_df1_quizzes[new_df1_quizzes["Course Name"] == course]
            course_df_assignments = new_df1_assignments[new_df1_assignments["Course Name"] == course]

            # Retrieve attendance data for the selected course
            course_df_attendance = df_Absences[df_Absences["Course Name"] == course]

            # Calculate the counts for quizzes, assignments, absences, and presence for the selected course
            count_quizzes = len(course_df_quizzes)
            count_assignments = len(course_df_assignments)
            count_absences = course_df_attendance["Attendance"].eq("Absent").sum()
            count_presence = len(course_df_attendance) - count_absences

            # Create a bar chart for the selected course
            fig_selected_course = go.Figure()
            fig_selected_course.add_trace(go.Bar(x=["Quizzes", "Assignments", "Absences", "Presence"],
                                                y=[count_quizzes, count_assignments, count_absences, count_presence],
                                                marker_color=['#009639', 'lightgray', 'red', 'blue']))
            fig_selected_course.update_layout(title=f"📊 Counts for {course}",
                                            xaxis_title='Activity',
                                            yaxis_title='Count')

            # Display the counts for the selected course
            st.sidebar.markdown(
            f"<div style='font-size: 20px; font-weight: bold; background-color: #90EE90; color: white; padding: 10px; border-radius: 5px; text-align: center;'>"
            f"<p style='margin-bottom: 5px;'>Counts for <code>{course}</code>:</p>"
            f"<p style='margin-bottom: 5px;'><span style='background-color: #009639; padding: 5px; border-radius: 5px;'>Quizzes: {count_quizzes}</span></p>"
            f"<p style='margin-bottom: 5px;'><span style='background-color: lightgray; padding: 5px; border-radius: 5px;'>Assignments: {count_assignments}</span></p>"
            f"<p style='margin-bottom: 5px;'><span style='background-color: red; padding: 5px; border-radius: 5px;'>Absences: {count_absences}</span></p>"
            f"<p style='margin-bottom: 0;'><span style='background-color: blue; padding: 5px; border-radius: 5px;'>Presence: {count_presence}</span></p>"
            "</div>",
            unsafe_allow_html=True
            )

            # Show the bar chart for the selected course
            st.plotly_chart(fig_selected_course)
