import npyscreen
import requests
import json

from npyscreen.wgtitlefield import TitleText

class App(npyscreen.NPSAppManaged):
    def onStart(self):
        #add forms to the application
        self.addForm('MAIN', FirstForm, name="Joke Machine")
        #self.addForm('SECOND', SecondForm, name="second")

class FirstForm(npyscreen.ActionFormMinimal):
  def create(self):
    self.add(npyscreen.TitleText, w_id="textfield", name="Enter a keyword: ")
    self.add(npyscreen.ButtonPress, name="Search", when_pressed_function=self.btn_press)
    self.add(npyscreen.ButtonPress, name="Display liked jokes", when_pressed_function=self.like_btn)

  def generateJoke(self):
    #connecting to the API and adding keyword from input
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

  global likedJokes
  likedJokes = []

  def btn_press(self):
    #Generate a joke when the button is pressed
    message = 'Here is a joke for you: \n.\n' + self.generateJoke() + '\n.\n.\n' + 'Did you like this joke?'
  
    #npyscreen.notify_confirm (message, title="Joke", wrap=True, wide=True, editw=1)
    
    popup = npyscreen.notify_yes_no(message, title="Message", form_color='STANDOUT', wrap=True, editw = 0)
    if popup == True:
      likedJokes.append(jokeID)

  def on_ok(self):
    self.parentApp.switchForm(None)
  
  def like_btn(self):
    message = str(likedJokes)
    npyscreen.notify_confirm (message, title="like", wrap=True, wide=True, editw=1)
    """
    for x in range (likedJokes.len):
      getLikedJoke = ((requests.get(url = "https://v2.jokeapi.dev/joke/Any?idRange=" + x)).json())
      if getLikedJoke['type'] == 'twopart':
        print (getLikedJoke['setup'] + "\n" + getLikedJoke['delivery'])
      else:
        print (getLikedJoke['joke'])
    """

      
app = App()
app.run()

"""
class SecondForm(npyscreen.ActionFormMinimal):
  def create(self):
    self.add(npyscreen.ButtonPress, name="Like!", when_pressed_function=self.like_btn)
    self.add(npyscreen.ButtonPress, name="Next joke", when_pressed_function=self.generateJoke)

  def on_ok(self):
    self.parentApp.change_form(None)

  def btn_press(self):
    npyscreen.notify_confirm("You pressed the button :-)", title="Button Press", wrap=True, wide=True, editw=1)
    """
