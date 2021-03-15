import npyscreen
import requests
import json

from npyscreen.wgtitlefield import TitleText

class App(npyscreen.NPSAppManaged):
    def onStart(self):
        #add forms to the application
        self.addForm('MAIN', FirstForm, name="Joke Machine")

# screen when starting the program
class FirstForm(npyscreen.ActionFormMinimal):
  def create(self):
    #add the textfield for entering the keyword that the program will look for in the jokes database
    self.add(npyscreen.TitleText, w_id="textfield", name="Enter a keyword: ")
    # add button "Search" and refer to the function btn.press
    self.add(npyscreen.ButtonPress, name="Search", when_pressed_function=self.btn_press)
    # add button "Display liked jokes" which refers to the function like_btn
    self.add(npyscreen.ButtonPress, name="Display liked jokes", when_pressed_function=self.like_btn)

  # function that will find a joke from the API database and print it out 
  def generateJoke(self):
    # connect to the API through an url with added keyword from input
    keyword = self.get_widget("textfield").value
    url = "https://v2.jokeapi.dev/joke/Any?contains=" + keyword
    getJoke = (requests.get(url)).json()
    global jokeID 
    jokeID = getJoke['id']
    # decide whether its a single or double line joke 
    # return the type 'joke' or 'setup' + 'delivery' depending on the joke type
    if getJoke['type'] == 'twopart':
      return getJoke['setup'] + "\n" + getJoke['delivery'] 
    else:
      return getJoke['joke'] 

# create global arraylist to be able to access to it from different parts of the program
  global likedJokes
  likedJokes = []

  # function that will be called when 'Search' button is pressed
  def btn_press(self):
    # new cariable referring to the generateJoke() function
    x = self.generateJoke()
    # generate a joke when the button is pressed and print this message
    message = 'Here is a joke for you: \n.\n' + x + '\n.\n.\n' + 'Did you like this joke?'
    
    # show 'yes' and 'no' buttons in the message with a joke
    popup = npyscreen.notify_yes_no(message, title="Message", form_color='STANDOUT', wrap=True, editw = 0)
    # if 'yes' is pressed then add the joke to the list of liked jokes 
    if popup == True:
      likedJokes.append(x)

  def on_ok(self):
    self.parentApp.switchForm(None)
  
  # function that will be called when the 'Display liked jokes' button is pressed
  def like_btn(self):
    # prints a list with all the liked jokes of the current session
    message = likedJokes
    npyscreen.notify_confirm (message, title="Your liked jokes", wrap=True, wide=True, editw=1)
      
# runs the program
app = App()
app.run()