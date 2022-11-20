# from model import db, ProgrammingLanguage, UserProgrammingLanguageMapping, User, UserTimeSlotMapping, TimeSlot, Prompt

# prompt_filename = 'Leetcode-data - leetcode.csv'

# def populate_prompt_tb():

#     with open(prompt_filename, 'r') as csvfile:
#         datareader = csv.reader(csvfile)
#         for row in datareader:
#             split_data = row[0].split("--")
#             prompt_name_data, prompt_link_data, prompt_difficulty_data = split_data
#             populate_prompt = Prompt(prompt_name = prompt_name_data, prompt_link = prompt_link_data, prompt_difficulty = prompt_difficulty_data )
#             db.session.add(populate_prompt)
#             db.session.commit()

# user_filename = 'User-data.csv'

# def populate_user_tb():

#     with open(user_filename, 'r') as csvfile:
#         datareader = csv.reader(csvfile)
#         for row in datareader:
#             split_data = row[0].split("--")

#             first_name_data, last_name_data, email_data, pwd_data, prompt_diff_data, primary_lang_data, timezone_data, prog_name_data, selected_timeslots_data = split_data
#             print(first_name_data)
#             # breakpoint()
#             populate_user = User(first_name = first_name_data, last_name = last_name_data, email = email_data, password = pwd_data, prompt_difficulty_level=prompt_diff_data,primary_language=primary_lang_data, timezone_name= timezone_data )

#             db.session.add(populate_user)
#             db.session.commit()
#             user_id = User.query.filter(email=email_data).first().user_id
#             # timeslots = TimeSlot.query.all()
#             # for time in timeslots:
#             #     if selected_timeslots_data == time:
#             get_timeslot_id = TimeSlot.query.filter(timeslot_name = selected_timeslots_data).first().timeslot_id
#             populate_timeslot = UserTimeSlotMapping(user_id=user_id, timeslot_id=get_timeslot_id)

#             db.session.add(populate_timeslot)
#             db.session.commit()


# def populate_initial_db():
#     programming_language_py = ProgrammingLanguage(programming_language_name = 'Python', programming_language_label = 'py')
#     programming_language_js = ProgrammingLanguage(programming_language_name = 'Javascript', programming_language_label = 'js')
#     programming_language_ja = ProgrammingLanguage(programming_language_name = 'Java', programming_language_label = 'ja')
#     prog_language_c_plus_plus = ProgrammingLanguage(programming_language_name = 'C++', programming_language_label = 'C++')
#     prog_language_c = ProgrammingLanguage(programming_language_name = 'C', programming_language_label = 'C')
#     timeslot_7am = TimeSlot(timeslot_name = '7am - 10am', timeslot_label = '7am')
#     timeslot_10am = TimeSlot(timeslot_name = '10am - 1pm', timeslot_label = '10am')
#     timeslot_1pm = TimeSlot(timeslot_name = '1pm - 4pm', timeslot_label = '1pm')
#     timeslot_4pm = TimeSlot(timeslot_name = '4pm - 7pm', timeslot_label = '4pm')
#     timeslot_7pm = TimeSlot(timeslot_name = '7pm - 10pm', timeslot_label = '7pm')
#     timeslot_10pm = TimeSlot(timeslot_name = '10pm - 12am', timeslot_label = '10pm')

#     db.session.add_all([programming_language_py, programming_language_js,
#                         programming_language_ja, prog_language_c_plus_plus,
#                         prog_language_c, timeslot_7am, timeslot_10am,
#                         timeslot_1pm,timeslot_4pm, timeslot_7pm, timeslot_10pm])
#     db.session.commit()
