from datetime import datetime
start_time = datetime.now()

import os
import csv
os.system("cls") # clearing screen
os.chdir(r'C:\Users\User\Documents\GitHub\Scoreboard') # active directory to current directory by providing the location
	
def read_innings(next_ball,opp_dict,our_dict,our_bat,our_bowl,opp_extras,our_runs,our_fow,our_w,our_runs_pp,our_inn_end,bowl_order,bat_order):
	last_over=0; run_over=0; last_ball=""
	for i in range(0,len(next_ball),2):
		try:
			sp1=next_ball[i].split(',') # splitting the commentary by comma
			sp2=sp1[0].split(" to ") # splitting the 1st part of line
		except Exception as e:
			print(e,i,next_ball[i])
			print("Error in splitting or stripping the line")
			exit()

		bat=our_dict[sp2[1]] # from 2nd part of 1st part of line (after "to")
		sp3=sp2[0].split() # ball number + bowler name
		ball=sp3[0] # o.b (over.ball)
		bowl=""
		sp1[1]=sp1[1].strip()
		
		for j in range(1,len(sp3)): 
			bowl+=sp3[j] # bowler name
			if j!=len(sp3)-1: bowl+=" " # to give spaces
		bowl=opp_dict[bowl]
			
		if bat not in bat_order: bat_order.append(bat) # order of batsman whenever new batsman comes
		if bowl not in bowl_order: bowl_order.append(bowl) # order of bowler whenever new bowler comes
		
		sp4=sp1[1].split() # runs part
		runs=sp4[0] # we will be working on this
		try:
			over=int(ball.split('.')[0]) # over number
			count_ball=int(ball.split('.')[1]) # ball number
		except Exception as e:
			print(e)
			print("Error in getting the over and ball number")
		
		if last_over!=over: # next over starts
			if last_over==5: # powerplay runs
				our_runs_pp=our_runs
			
			our_bowl[last_ball]["O"]+=1 # increment in over of previous bowler when his over ends
			
			if run_over==0: # maiden over
				our_bowl[last_ball]["M"]+=1
			else: # otherwise add runs to his list
				our_bowl[last_ball]["R"]+=run_over
			
			run_over=0 # again initialize run_over to zero
			
		last_over=over
		last_ball=bowl
		our_bat[bat]["B"]+=1
		our_bat[bat]["status"]="not out" # initialize the status of batsman with not out
		
		if runs=="out": # out case
			our_w+=1 # increase in count of wicket
			if sp4[1][0]=='L': # lbw case
				our_bat[bat]["status"]="lbw " # status of batsman
			elif sp4[1][0]=='C': # Caught case
				temp=""
				if sp4[3][-1]=='!': temp=sp4[3][:-2] # name is followed with 2 exclamation marks, so we have to remove them
				else: temp=sp4[3]+" "+sp4[4][:-2] # in case of full name
				our_bat[bat]["status"]="c " + temp +" " # status of batsman
			else:
				our_bat[bat]["status"]="" # status of batsman
			
			our_bat[bat]["status"]+="b " + bowl # status of batsman
			
			try:
				our_fow+=str(our_runs) + "-"+ str(our_w) + " (" + bat + ", " + ball + "), "
			except Exception as e:
				print(e)
				print("Error in getting fall of wickets")
				exit()
		elif runs=="wide": # wide case, here there is only 1 wide runs
			run_over+=1 # increasing over run
			our_runs+=1 # increasing team run
			count_ball-=1 # reducing the ball count
			our_bat[bat]["B"]-=1 # removing the ball count of the batsman which was added earlier
			our_bowl[bowl]["WD"]+=1  # adding it to bowler spell
			opp_extras["w"]+=1 # adding to the extras
		elif runs=="FOUR": # 4 case
			run_over+=4
			our_runs+=4
			our_bat[bat]["R"]+=4
			our_bat[bat]["4s"]+=1
		elif runs=="SIX": # 6 case
			run_over+=6
			our_runs+=6
			our_bat[bat]["R"]+=6
			our_bat[bat]["6s"]+=1
		elif runs=="leg" or runs=="byes": # leg byes runs or byes runs
			sp1[2]=sp1[2].strip()
			sp5=sp1[2].split()
			try:
				if sp5[0]=="FOUR" or sp5[0]=='4': r=4
				else: r=int(sp5[0])
			except Exception as e:
				print(e)
				print("Error in getting runs for leg byes or byes")
				exit()
			our_runs+=r
			if runs=="byes": opp_extras["b"]+=r
			else: opp_extras["lb"]+=r
		elif runs=="1" or runs=="2" or runs=="3" or runs=="4":
			try:
				run_over+=int(runs)
				our_runs+=int(runs)
			except:
				print("Error in runs of 1 or 2 or 3 or 4(wides)")
				exit()
			if sp4[1]=="wides": # wide case, here there is more than 1 wide runs
				our_bowl[bowl]["WD"]+=int(runs) # adding it to bowler spell
				count_ball-=1 # reducing the ball count
				our_bat[bat]["B"]-=1  # removing the ball count of the batsman which was added earlier
				opp_extras["w"]+=int(runs) # adding to the extras
			else:
				our_bat[bat]["R"]+=int(runs) # otherwise adding it to batsman runs
					
	our_bowl[opp_dict[last_ball]]["R"]+=run_over
	if count_ball==6: # last ball case
		our_bowl[opp_dict[last_ball]]["O"]+=1 # increase the over count
		our_inn_end=last_over+1 # last ball of the inning
		if run_over==0: # increasing maiden count if last over was complete and the bowler did not conceded even a single run
			our_bowl[opp_dict[last_ball]]["M"]+=1
	else:
		our_inn_end=last_over+count_ball/10 # last ball of the inning
		our_bowl[opp_dict[last_ball]]["O"]+=count_ball/10 # count of over in decimal form
		
	extras=0
	for item in opp_extras: extras+=opp_extras[item] # all the extras
	extras=str(extras)+" ("
	try:
		for key,value in opp_extras.items(): 
			extras+=str(key)+" "+ str(value)+", "
	except Exception as e:
		print(e)
		print("Error in getting extras of the bowling team")
		exit()
	extras=extras[:-2]+")" # removing th elastr two characters from the extras strings
	return [our_bat,our_bowl,extras,our_runs,our_fow[:-2],our_w,our_runs_pp,our_inn_end,bowl_order,bat_order] # return  a list of value

def calculate(over,run): # getting economy
	over=over//1+(over%1)*10/6
	return round(run/over,2)

def scoreboard():
	with open(r"teams.txt",'r') as file: # opening the teams.txt to get the names of players of both the teams
		team=file.readline()
		try:
			team_pak=((team.split(":"))[1]).split(',')
			file.readline()
			team=file.readline()
			team_india=((team.split(":"))[1]).split(',')
		except Exception as e:
			print(e)
			print("Error in storing the names of team players")
			exit()
		
		team_pak=[i.strip() for i in team_pak]
		team_india=[i.strip() for i in team_india]
	
	# a dictionary which will be used to refer the names of players from commentary
	pak_dict={'Babar Azam':'Babar Azam(c)','Rizwan':'Mohammad Rizwan(w)','Fakhar Zaman':'Fakhar Zaman','Iftikhar Ahmed':'Iftikhar Ahmed','Khushdil':'Khushdil Shah','Shadab Khan':'Shadab Khan','Asif Ali':'Asif Ali','Mohammad Nawaz':'Mohammad Nawaz','Haris Rauf':'Haris Rauf','Naseem Shah':'Naseem Shah','Dahani':'Shahnawaz Dahani'} 
	
	ind_dict={'Rohit':'Rohit Sharma(c)','Rahul':'KL Rahul','Kohli':'Virat Kohli','Suryakumar Yadav':'Suryakumar Yadav','Hardik Pandya':'Hardik Pandya','Karthik':'Dinesh Karthik(w)','Jadeja':'Ravindra Jadeja','Bhuvneshwar':'Bhuvneshwar Kumar','Avesh Khan':'Avesh Khan','Arshdeep Singh':'Arshdeep Singh','Chahal':'Yuzvendra Chahal'} 
	
	pak_bat={}; pak_bowl={}; pak_bowl_line=[]; pak_bat_line=[] # line up is a list where we will have the bowlers, batsman in order of batting/bowling lineup
	for player in team_pak: # making a dictionary for all the players where we will maintain the counts needed of their batting 
		pak_bat[player]={"status":"Did not Bat","R":0,"B":0,"4s":0,"6s":0,"SR":0.00}
		pak_bowl[player]={"status":"Did not Bowl","O":0,"M":0,"R":0,"W":0,"NB":0,"WD":0,"ECO":0.00}
	
	ind_bat={}; ind_bowl={}; ind_bowl_line=[]; ind_bat_line=[] # line up is a list where we will have the bowlers, batsman in order of batting/bowling lineup
	for player in team_india: # making a dictionary for all the players where we will maintain the counts needed of their batting 
		ind_bat[player]={"status":"Did not Bat","R":0,"B":0,"4s":0,"6s":0,"SR":0.00}
		ind_bowl[player]={"status":"Did not Bowl","O":0,"M":0,"R":0,"W":0,"NB":0,"WD":0,"ECO":0.00}
	
	# variables that we will be needing
	extras_pak={"b":0,"lb":0,"w":0,"nb":0,"p":0}; pak_runs=0; wic_pak=""; wic_p=0; pow_runs_p=0; last_p=0 
	extras_ind={"b":0,"lb":0,"w":0,"nb":0,"p":0}; ind_runs=0; wic_ind=""; wic_i=0; pow_runs_i=0; last_i=0
	
	with open(r'pak_inns1.txt','r') as f: # team_pak Innings
		next_ball=f.readlines()
		pak_bat,ind_bowl,extras_ind,pak_runs,wic_pak,wic_p,pow_runs_p,last_p,ind_bowl_line,pak_bat_line=read_innings(next_ball,ind_dict,pak_dict,pak_bat,ind_bowl,extras_ind,pak_runs,wic_pak,wic_p,pow_runs_p,last_p,ind_bowl_line,pak_bat_line)
		
	with open(r'india_inns2.txt','r') as f: # team_india Innings
		next_ball=f.readlines()
		ind_bat,pak_bowl,extras_pak,ind_runs,wic_ind,wic_i,pow_runs_i,last_i,pak_bowl_line,ind_bat_line=read_innings(next_ball,pak_dict,ind_dict,ind_bat,pak_bowl,extras_pak,ind_runs,wic_ind,wic_i,pow_runs_i,last_i,pak_bowl_line,ind_bat_line)
	
	with open('scoreboard.csv', 'w', newline='') as f: # writing in csv file
		writer=csv.writer(f)
		
		writer.writerow(["India won by 5 wkts"])
		writer.writerow(["Pakistan Innings","","","","","",str(pak_runs)+"-"+str(wic_p)+" (" +str(last_p) +" Ov)"])
		writer.writerow(["Batter","","R","B","4s","6s","SR"])
		
		for batter in pak_bat_line: # batsman
			writer.writerow([batter,pak_bat[batter]["status"],pak_bat[batter]["R"],pak_bat[batter]["B"],pak_bat[batter]["4s"],pak_bat[batter]["6s"],round((pak_bat[batter]["R"]/pak_bat[batter]["B"])*100,2)])
		
		writer.writerow(["Extras","",extras_ind]) # extras
		writer.writerow(["Total","",str(pak_runs)+" ("+str(wic_p)+" wkts, "+str(last_p)+" Ov)"]) # total
		if len(pak_bat_line)!=11: # Did not bat
			temp=""
			try:
				for player in team_pak:
					if player not in pak_bat_line: temp+=player+", "
			except Exception as e:
				print(e)
				print("Error in getting players who did not bat from the team_pak team")
			writer.writerow(["Did not Bat",temp[:-2]])
		
		writer.writerow(["Fall of wickets"])
		writer.writerow([wic_pak]) # fall of wickets
		
		writer.writerow(["Bowler","O","M","R","W","NB","WD","ECO"])
		for bowler in ind_bowl_line: # bowlers
			writer.writerow([bowler,ind_bowl[bowler]["O"],ind_bowl[bowler]["M"],ind_bowl[bowler]["R"],ind_bowl[bowler]["W"],ind_bowl[bowler]["NB"],ind_bowl[bowler]["WD"],calculate(ind_bowl[bowler]["O"],ind_bowl[bowler]["R"])])
			
		writer.writerow(["Powerplays","Overs","Runs"])
		writer.writerow(["Mandatory","0.1-6",str(pow_runs_p)]) # powerplay
		
		writer.writerow(["India Innings",str(ind_runs)+"-"+str(wic_i)+" (" +str(last_i) +" Ov)"]) # team_india Innings
		writer.writerow(["Batter","","R","B","4s","6s","SR"])
		
		for batter in ind_bat_line:
			writer.writerow([batter,ind_bat[batter]["status"],ind_bat[batter]["R"],ind_bat[batter]["B"],ind_bat[batter]["4s"],ind_bat[batter]["6s"],round((ind_bat[batter]["R"]/ind_bat[batter]["B"])*100,2)])
		
		writer.writerow(["Extras","",extras_pak])
		writer.writerow(["Total","",str(ind_runs)+" ("+str(wic_i)+" wkts, "+str(last_i)+" Ov)"])
		if len(ind_bat_line)!=11:
			temp=""
			try:
				for player in team_india:
					if player not in ind_bat_line: temp+=player+", "
			except Exception as e:
				print(e)
				print("Error in getting players who did not bat from the team_indian team")
			writer.writerow(["Did not Bat",temp[:-2]])
		
		writer.writerow(["Fall of wickets"])
		writer.writerow([wic_ind])
		
		writer.writerow(["Bowler","O","M","R","W","NB","WD","ECO"])
		for bowler in pak_bowl_line:
			writer.writerow([bowler,pak_bowl[bowler]["O"],pak_bowl[bowler]["M"],pak_bowl[bowler]["R"],pak_bowl[bowler]["W"],pak_bowl[bowler]["NB"],pak_bowl[bowler]["WD"],calculate(pak_bowl[bowler]["O"],pak_bowl[bowler]["R"])])
			
		writer.writerow(["Powerplays","Overs","Runs"])
		writer.writerow(["Mandatory","0.1-6",str(pow_runs_i)])
			
from platform import python_version
ver = python_version()

if ver == "3.8.10":
	print("Correct Version Installed")
else:
	print("Please install 3.8.10. Instruction are present in the GitHub Repo/Webmail. Url: https://pastebin.com/nvibxmjw")

scoreboard()

end_time = datetime.now()
print('Duration of Program Execution: {}'.format(end_time - start_time))