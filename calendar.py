import numpy as np
import pandas as pd
import streamlit as stl
from july.utils import date_range
from datetime import datetime as dt
from matplotlib import pyplot as plt
from streamlit_option_menu import option_menu

class Calendar:
	def __init__(self):
		self.events = {
			'database': 'events.csv',
			'primary_key': 'Event_Name',
			'check': {'Event_Type': ['BuildIn','UserSet']}
		}
		self.now = dt.now()
		self.month_map = {
			'January': 1,   'February': 2, 'March': 3,     'April': 4,
			'May': 5,       'June': 6,     'July': 7,      'August': 8,
			'September': 9, 'October': 10, 'November': 11, 'December': 12
		}
		self.reverse_month_map = {
			1: 'January',   2: 'February', 3: 'March',     4: 'April',
			5: 'May',       6: 'June',     7: 'July',      8: 'August',
			9: 'September', 10: 'October', 11: 'November', 12: 'December'
		}
		self.calendar = {'SUN': [], 'MON': [], 'TUE': [], 'WED': [], 'THU': [], 'FRI': [], 'SAT': []}

	def month_length(self, month, year):
		days = 31
		if month in ['April','June','September','November']: days = 30
		elif month == 'February' and self.leap_year(year): days = 29
		elif month == 'February' and not self.leap_year(year): days = 28
		return days

	def leap_year(self, year):
		k = 0
		if year == ' ' or year == 'XXXX': k = int(self.now.strftime('%Y'))
		else: k = int(year)
		a = k % 4
		b = k % 100
		c = k % 400
		if (a == 0 and b != 0) or c == 0: return True
		else: return False
	
	def create_cal(self, year, month):
		first = int(dt(int(year), self.month_map[month], 1).strftime('%w'))
		k = first
		week = list(self.calendar.keys())
		for i in range(first): self.calendar[week[i]].append(' ')
		for i in range(first, self.month_length(month, year) + first):
			self.calendar[week[k]].append(i - first + 1)
			k = k + 1
			if k == 7: k = 0
		if k > 0:
			for i in range(k,7): self.calendar[week[i]].append(' ')
	
	def calendar_page(self):
		stl.title('⚙ :green[Month Calendar]')
		stl.markdown("""---""")
		settings, main = stl.columns([0.4,0.6])
		with settings:
			month_number = app.month_map[app.now.strftime('%B')] - 1
			year = stl.text_input('**Enter Year to display Calendar**', app.now.strftime('%Y'))
			month = stl.selectbox('**Enter Month to display Calendar**', app.month_map.keys(), index = month_number)
			stl.markdown("""---""")
			stl.write(f"**{app.now.strftime('%d')} {app.now.strftime('%B')} {app.now.strftime('%Y')}, {app.now.strftime('%A')}**")
			self.display_current_event()
		with main:
			if year == '': year = self.now.strftime('%Y')
			stl.subheader(f"{month.upper()} :green[{year}]")
			app.create_cal(year, month)
			cal = pd.DataFrame(app.calendar)
			stl.markdown(cal.style.set_table_styles(styles).to_html(), unsafe_allow_html = True)
		stl.markdown("""---""")
	
	def event_mark_page(self):
		stl.title('⚙ :green[Event Settings]')
		stl.markdown("""---""")
		year, month, day, name = stl.columns([0.15,0.15,0.15,0.55])
		with year: event_year = stl.text_input('Event Year')
		with month: event_month = stl.selectbox('Event Month', list(range(1,13)))
		with day:
			if event_year == '': event_year = 'XXXX'
			if event_month in [4,6,9,11]: event_day = stl.selectbox('Event Date', list(range(1,31)))
			elif event_month == 2 and self.leap_year(event_year): event_day = stl.selectbox('Event Date', list(range(1,30)))
			elif event_month == 2 and not self.leap_year(event_year): event_day = stl.selectbox('Event Date', list(range(1,29)))
			else: event_day = stl.selectbox('Event Date', list(range(1,32)))
		with name: event_name = stl.text_input('Event Name')
		if stl.button('**INSERT EVENT**'): self.insert_event(event_year, event_month, event_day, event_name)
		stl.markdown("""---""")
		event_detail = stl.text_input('Event Name to Delete')
		if stl.button('**DELETE EVENT**'): self.delete_event(event_detail)
	
	def event_view_page(self):
		stl.title('⚙ :green[Search Events]')
		stl.markdown("""---""")
		by, value = stl.columns([0.25,0.75])
		with by: search_by = stl.selectbox('Search By', ['Name','Month'])
		with value:
			if search_by == 'Name': event_value = stl.text_input('Event Name')
			elif search_by == 'Month': event_month_val = stl.selectbox('Enter Month', list(self.month_map.keys()))
			else: event_value = stl.text_input('Enter Year')
		if stl.button('**GET EVENTS**'):
			if search_by == 'Name': self.search_event_name(event_value)
			elif search_by == 'Month': self.search_event_month(event_month_val)
	
	def insert_event(self, event_year, event_month, event_day, event_name):
		marker = False
		if event_year == 'XXXX':
			marker = True
			event_year = self.now.strftime('%Y')
		datestamp = dt(int(event_year), int(event_month), int(event_day))
		if datestamp < self.now and marker == False:
			stl.write('**WARNING** : Events must be set in Present or Future Date')
			return
		db = pd.read_csv(self.events['database'])
		event_names = db[self.events['primary_key']].values
		if event_name in event_names:
			stl.write('EVENT Already Exists')
			return
		if marker == True: values = ['XXXX', event_month, event_day, event_name, 'UserSet']
		else: values = [event_year, event_month, event_day, event_name, 'UserSet']
		db.loc[len(db)] = values
		db.to_csv(self.events['database'], index = False)
		stl.write('EVENT Successfully Added')
	
	def delete_event(self, event_name):
		df = pd.read_csv(self.events['database'])
		existing_events = df[self.events['primary_key']].values
		if event_name not in existing_events:
			stl.write('EVENT Does Not Exist')
			return
		index = list(existing_events).index(event_name)
		event_type = df['Event_Type'].values[index]
		if event_type == 'BuildIn':
			stl.write('BUILDIN Events Cannot be Deleted')
			return
		df = df.drop(index)
		df.to_csv(self.events['database'], index = False)
		stl.write('EVENT Successfully Deleted')
	
	def search_event_name(self, event_name):
		df = pd.read_csv(self.events['database'])
		existing_events = df[self.events['primary_key']].values
		if event_name not in existing_events:
			stl.write('EVENT Does Not Exist')
			return
		index = list(existing_events).index(event_name)
		event_day = df['Event_Day'].values[index]
		event_month = df['Event_Month'].values[index]
		event_year = df['Event_Year'].values[index]
		string = self.format_date(event_year, event_month, event_day)
		result = pd.DataFrame({'Event Date': [string], 'Event Name': [event_name]})
		stl.table(result)
	
	def search_event_month(self, event_month):
		df = pd.read_csv(self.events['database'])
		indices = [i for i in range(len(df)) if int(df['Event_Month'].values[i]) == self.month_map[event_month]]
		result = {'Event Date': [], 'Event Name': []}
		for i in indices:
			yr = df['Event_Year'].values[i]
			mn = df['Event_Month'].values[i]
			dy = df['Event_Day'].values[i]
			result['Event Date'].append(self.format_date(yr, mn, dy))
			result['Event Name'].append(df['Event_Name'].values[i])
		stl.table(pd.DataFrame(result))
	
	def format_date(self, event_year, event_month, event_day):
		dstring = ''
		dstring = self.reverse_month_map[int(event_month)]
		if int(event_day) < 10: dstring += ' 0' + str(event_day)
		else: dstring += ' ' + str(event_day)
		if event_year != 'XXXX': dstring += ' ' + str(event_year)
		return dstring
	
	def display_current_event(self):
		df = pd.read_csv(self.events['database'])
		current_year = self.now.strftime('%Y')
		current_month = self.month_map[self.now.strftime('%B')]
		current_day = int(self.now.strftime('%d'))
		checker = {'year': False, 'month': False, 'day': False}
		event_list = {'Events Today': []}
		for i in range(len(df)):
			y = df['Event_Year'].values[i]
			m = int(df['Event_Month'].values[i])
			d = int(df['Event_Day'].values[i])
			if current_year == 'XXXX' or current_year == y: checker['year'] = True
			if current_month == m: checker['month'] = True
			if current_day == d: checker['day'] = True
			if checker['year'] and checker['month'] and checker['day']: event_list['Events Today'].append(df['Event_Name'].values[i])
		if len(event_list['Events Today']) != 0: stl.table(event_list)

stl.set_page_config(page_title = 'Digital Calendar', layout = 'wide')
app = Calendar()

with stl.sidebar:
	page = option_menu(
		menu_title = 'Navigation',
		options = ['Calendar','Events Mark','Events View']
	)

th_props = [('font-size', '14px'), ('text-align', 'left'), ('font-weight', 'bold'), ('color', 'white'), ('background-color', '#2c729c'), ('border','1px solid #4793bf')]
td_props = [('font-size', '14px'), ('text-align', 'center'), ('border','1px solid #909496')]
cell_hover_props = [('background-color', 'black')]
headers_props = [('text-align','center'), ('font-size','1.0em')]

styles = [
	dict(selector = "th", props = th_props),
	dict(selector = "td", props = td_props),
	dict(selector = "td:hover", props = cell_hover_props),
	dict(selector = 'th.col_heading', props = headers_props),
	dict(selector = 'th.col_heading.level0', props = headers_props),
	dict(selector = 'th.col_heading.level1', props = td_props)
]
if page == 'Calendar': app.calendar_page()
if page == 'Events Mark': app.event_mark_page()
if page == 'Events View': app.event_view_page()
