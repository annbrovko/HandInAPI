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
    self.add(npyscreen.TitleText, w_id="textfield", name="Enter a keyword: ")
    self.add(npyscreen.ButtonPress, name="Search", when_pressed_function=self.btn_press)
    self.add(npyscreen.ButtonPress, name="Display liked jokes", when_pressed_function=self.like_btn)

  def generateJoke(self):
    # connecting to the API through an url with added keyword from input
    keyword = self.get_widget("textfield").value
    url = "https://v2.jokeapi.dev/joke/Any?contains=" + keyword
    getJoke = (requests.get(url)).json()
    global jokeID 
    jokeID = getJoke['id']
    # decide whether its a single or double line joke 
    if getJoke['type'] == 'twopart':
      return getJoke['setup'] + "\n" + getJoke['delivery'] 
    else:
      return getJoke['joke']

# created global arraylist to be able to access to it
  global likedJokes
  likedJokes = []

  def btn_press(self):
    x = self.generateJoke()
    #Generate a joke when the button is pressed
    message = 'Here is a joke for you: \n.\n' + x + '\n.\n.\n' + 'Did you like this joke?'
    
    popup = npyscreen.notify_yes_no(message, title="Message", form_color='STANDOUT', wrap=True, editw = 0)
    if popup == True:
      likedJokes.append(x)

  def on_ok(self):
    self.parentApp.switchForm(None)
  
  def like_btn(self):
    message = likedJokes
    npyscreen.notify_confirm (message, title="Your liked jokes", wrap=True, wide=True, editw=1)
      
app = App()
app.run()