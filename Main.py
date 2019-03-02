import requests
from bs4 import BeautifulSoup
import time

import News_Database
import User_Database
import Inform_User

News = News_Database.Database_Post()
Mail = User_Database.Database_User()

print("""
Enter '1' to organize user database.
Enter '2' to start the program.
Enter 'q' to exit program.
""")

while True:

	number = input("Command: ")

	if (number == "1"):

		print("""
		Enter '1' to see all users.
		Enter '2' to add a new user.
		Enter '3' to delete a user.
		Enter '4' to update a user.
		Enter '5' to see total number of users.
		Enter '6' to go back to main menu.
		Enter 'q' to exit the program.
		""")

		while True:

			command = input("\nCommand for mail: ")

			if (command == "1"):
				Mail.show_mails()

			elif (command == "2"):
				print("Enter a new mail address:")
				new_mail = input().lower()

				if (Mail.check_if_mail_exists(new_mail)):
					print("\n" + new_mail, "already exists on database. Please try again.\n")
					continue

				print("Would you want to receive mails? (Y/N):")
				user_stat = input().upper()

				if (user_stat == "Y"):
					user_stat = True
					text = new_mail + " successfully added to database."

				elif (user_stat == "N"):
					user_stat = False
					text = new_mail + " successfully added to database. Be aware that you wont receive any mails."

				else:
					print("\nInvalid command. Try again.\n")
					continue

				new_user = User_Database.User(new_mail, user_stat)
				Mail.add_mail(new_user)

				print(text)


			elif (command == "3"):

				if (Mail.total_user() == 0):
					print("\nNo user found on database.\n")
					continue

				print("Enter the mail address you want to delete:")
				del_mail = input("Mail: ")

				if (Mail.check_if_mail_exists(del_mail) == 0):
					print("There is not such mail address as " + del_mail + ". Please try again")
					continue

				print("Are you sure you want to delete " + del_mail + "? (Y/N):")
				yes_no = input().upper()

				if (yes_no == "Y"):
					Mail.delete_mail(del_mail)
					print(del_mail, " successfully deleted from database.")

				elif (yes_no == "N"):
					print("Process canceled.")
					continue
				else:
					print("\nInvalid command. Please try again.")


			elif (command == "4"):

				if (Mail.total_user() == 0):
					print("\nNo user found on database.\n")
					continue

				print("Enter the mail address you want to update: ")
				update_mail = input()

				if (Mail.check_if_mail_exists(update_mail) == 0):
					print("There is not such mail address as " + update_mail + ". Please try again")
					continue

				print("What would you want to change? "
					  "To go back, enter 'q' , to change mail, "
					  "enter M, to change status, enter S:")

				change_what = input().upper()

				# Updating User Mail
				if (change_what == "M"):
					new_mail = input("Enter a new mail address: ")
					Mail.update_mail(update_mail, new_mail)
					print(update_mail, "changed to", new_mail + ".")

				# Updating Status (if 0, wont receive mails, else will)
				elif (change_what == "S"):
					print("Would you want to get mails or not? (Y/N)")
					yes_no = input().upper()
					if (yes_no == "Y"):
						Mail.update_stat(update_mail, True)
						print(update_mail, "will now receive mails.")
					elif (yes_no == "N"):
						Mail.update_stat(update_mail, False)
						print(update_mail, "will not receive mails anymore.")
					else:
						print("Wrong command. Please try again.")
						continue

				elif (change_what == "Q"):
					print("You are back to menu.")

				else:
					print("\nInvalid comamnd. Try again.\n")


			elif (command == "5"):

				total = Mail.total_user()

				if (total != 0):
					print("Total number of users: ", total)
				else:
					print("No user found on database.")

			elif (command == "6"):
				# Going Back to Main Menu
				print("\nYou are on main menu right now.\n")
				break

			elif (command == "q"):
				exit()

			else:
				print("Invalid command. Try again.")


	elif (number == "2"):

		while True:

			new_posts = 0

			# Checking if there are any users on database
			if (Mail.total_user() == 0):

				print("No user found on database. You have to add at least one user to continue.")
				user_mail = input("Mail: ").lower()
				print("Would you want to receive mails?")
				print("(If you are running this program for the first time, \nwe recommend "
					  "turning notifications off if you don't\nwant get several mails"
					  " in your first run.\nAfter the first run, the posts will be added to database"
					  " and you can turn notifications on.)")

				stat = input("Y/N: ").upper()

				# Checking Stat
				if (stat == "Y"):
					stat = True
				elif (stat == "N"):
					stat = False
				else:
					print("\nWrong command. Try again.\n")
					continue

				user_info = User_Database.User(user_mail, stat)

				# Adding user to database
				Mail.add_mail(user_info)

				print(user_mail, "successfully added to database.")

			
			try:
				url = "https://www.ghacks.net/"
				response = requests.get(url)
				html_content = response.content
			except Exception as e:
				print("Something unexpected happened. Waiting for 3 min..")
				time.sleep(180)
				continue


			soup = BeautifulSoup(html_content, "html.parser")

			post_info_html = soup.find("div",{"class":"row nocol xs-all-12-centered"})

			picture = post_info_html.img['src']
			title = post_info_html.find("h2",{"class":"heading--medium mb--10"}).text
			link = post_info_html.find("h2",{"class":"heading--medium mb--10"}).a['href']
			date = post_info_html.find("div",{"class":"opacity--90 text--tiny ghacks-links ghacks-links--smallunderline mb--10"}).text[1:]
			info = post_info_html.find("div",{"class":"excerpt"}).text


			if (not News.check_if_post_exists(link = link) and not News.check_if_post_exists(picture = picture)):

				Post = News_Database.News(title,date,info,link,picture)
				News.add_post(Post)

				mail_list = Mail.get_mails()

				text_mail = Post.text_of_mail()

				new_posts += 1

				for user in mail_list:
					Inform_User.send_mail(user[0], text_mail)


			print(str("0" + str(new_posts)) + " new post released. Waiting for 5 min")
			time.sleep(300)			


	elif (number.lower() == "q"):
		exit()

	else:
		print("Invalid command. Try again.")