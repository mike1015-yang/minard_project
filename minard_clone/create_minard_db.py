import pandas as pd
from sqlalchemy import create_engine

class CreateMinardDB:
	def __init__(self):
		with open("minard_clone/data/minard.txt", encoding= "utf-8") as f:
			lines = f.readlines()
		column_names = lines[2].split()
		# print(column_names)
		patterns_to_be_replaced = {"(", ")", "$", ","}
		adjusted_column_names = []
		for column_name in column_names:
			for pattern in patterns_to_be_replaced:
				if pattern in column_name:
					column_name = column_name.replace(pattern, "")
			adjusted_column_names.append(column_name)
		# print(adjusted_column_names)
		self.lines = lines
		self.column_names_city = adjusted_column_names[:3]
		self.column_names_temp = adjusted_column_names[3:7]
		self.column_names_army = adjusted_column_names[7:]
		"""print(column_names_city)
		print(column_names_temp)
		print(column_names_army)"""
	def create_city_dataframe(self):
		i = 6
		lonc, latc, cities = [], [], []
		while i <= 25:
			lon, lat, city = self.lines[i].split()[:3]
			lonc.append(float(lon))
			latc.append(float(lat))
			cities.append(city)
			i += 1
		city_data = (lonc, latc, cities)
		city_df = pd.DataFrame()
		for column_name, data in zip(self.column_names_city, city_data):
			city_df[column_name] = data
		# print(city_df)
		return city_df
	def create_temp_dataframe(self):
		i = 6
		lont, temp, days, dates = [], [], [], []
		while i <= 14:
			line_split = self.lines[i].split()
			lont.append(float(line_split[3]))
			temp.append(int(line_split[4]))
			days.append(int(line_split[5]))
			if i == 10:
				dates.append("Nov 24")
			else:
				dates.append(line_split[6] + " " + line_split[7])
			i += 1
		temp_data = (lont, temp, days, dates)
		temp_df = pd.DataFrame()
		for column_name, data in zip(self.column_names_temp, temp_data):
			temp_df[column_name] = data
		# print(temp_df)
		return temp_df
	def create_army_dataframe(self):
		i = 6
		lonp, latp, surviv, direc, division = [], [], [], [], []
		while i <= 53:
			line_split = self.lines[i].split()
			lonp.append(float(line_split[-5]))
			latp.append(float(line_split[-4]))
			surviv.append(int(line_split[-3]))
			direc.append(line_split[-2])
			division.append(int(line_split[-1]))			   
			i += 1
		army_data = (lonp, latp, surviv, direc, division)
		army_df = pd.DataFrame()
		for column_name, data in zip(self.column_names_army, army_data):
			army_df[column_name] = data
		# print(army_df)
		return army_df
	def create_database(self):
		connection = create_engine('mysql+pymysql://root:password@localhost:3306/minard')
		city_df = self.create_city_dataframe()
		temp_df = self.create_temp_dataframe()
		army_df = self.create_army_dataframe()
		df_dict = {
			"cities": city_df,
			"temperatures": temp_df,
			"army": army_df
		}
		for k, v in df_dict.items():
			v.to_sql(name = k, con = connection, index = False, if_exists = "replace")

create_minard_db = CreateMinardDB()
create_minard_db.create_database()
