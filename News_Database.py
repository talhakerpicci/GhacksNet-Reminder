import sqlite3

class News():

    def __init__(self,title,date,info,link,picture):
        self.title = title
        self.date = date
        self.info = info
        self.link = link
        self.picture = picture

    def text_of_mail(self):

        return """
        <!DOCTYPE html>
        <html>
        <head>
            <title></title>
        </head>
        <body>

            <div id="main-div" style="width: 550px; height: auto; background-color: rgb(220, 226, 234);
                    border: 2px solid black;">
                
                <div id="content" style="margin-top: 5px; margin-left: 5px; overflow: hidden;">

                    <div id="image-poster" style="float: left;">
                        <a href='""" + self.link + """'><img src='""" + self.picture + """' width="150" height="150"></a>
                    </div>

                    
                    <div id="header" style="margin-left: 165px; width: 500px; font-size: 100%; font: inherit; height: 30px; ">
                            <a href='""" + self.link + """' style="text-decoration: none; color: black;"><h3>""" + self.title + """</h3></a>
                    </div>

                    <div id="date" style="font-size: 12px; margin-left: 165px; width: 500px; height: 20px;">
                        <span>""" + self.date + """</span>
                    </div>

                    <div id="text" style="font-weight: 400; font-size: 15px; color: #111; margin-left: 165px; width: 350px; font-size: 13px;">
                        <span>""" + self.info + """</span>
                    </div>
                    
                </div>

            </div>

        </body>
        </html>
        """


class Database_Post():

    def __init__(self):

        self.connect_database()

    def connect_database(self):

        self.connection = sqlite3.connect("Ghacks Net.db")
        self.cursor = self.connection.cursor()

        query = "create table if not exists " \
                "Tbl_Posts (" \
                "Title text," \
                "Date text," \
                "Info text," \
                "Link text," \
                "Picture text)"
        self.cursor.execute(query)
        self.connection.commit()

    def check_if_post_exists(self, link = "", picture = ""):

        select_ID = ""
        var_value = ""

        if (len(link) != 0):
            select_ID = "Link"
            var_value = link
        elif (len(picture) != 0):
            select_ID = "Picture"
            var_value = picture

        query = "select * from Tbl_Posts where " + select_ID + " = @p1"
        self.cursor.execute(query,(var_value,))
        posts = self.cursor.fetchall()

        if (len(posts) == 0):
            return 0
        else:
            return 1

    def add_post(self,News):

        query = "insert into Tbl_Posts values (@p1,@p2,@p3,@p4,@p5)"
        self.cursor.execute(query,(News.title,News.date,News.info,News.link,News.picture))
        self.connection.commit()