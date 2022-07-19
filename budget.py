# **** --- CREATED BY --- ****
# ->->  Dr. Hafeez Anwar  <-<-
#  -> Date: June 26, 2022  <-
# ****************************
# The sentences from the problem statement are
# given before each statement, to show that the 
# solution is drafted as per the requirements of
# the problem

# Complete the Category class in budget.py
class Category:
# It should be able to instantiate objects based on different budget
  # categories like food, clothing, and entertainment. When objects are
  # created, they are passed in the name of the category.
  def __init__(self,nam):
    self.name = nam
    # The class should have an instance variable called ledger that
    # is a list
    self.ledger = list()
    #print(self.name,'constructed')

  # A deposit method that accepts an amount and description
  def deposit(self, amnt, description=None):
    # If no description is given, it should default to an empty string.
    if description is None:
        object_to_append = {"amount":amnt, "description":''}
    else:
        object_to_append = {"amount":amnt, "description":description}
    # The method should append an object to the ledger list in the form of
    # {"amount": amount, "description": description}
    self.ledger.append(object_to_append)

  def withdraw(self, amnt, description=None):
    # If there are not enough funds, nothing should be added to the ledger
    #Check for the funds, if the requested withdrawl can be covered by 
    #the total amount
    if self.check_funds(amnt) is True:
        # the amount passed in should be stored in the ledger as a negative
        # number
        amnt = -1*amnt
        if description is None:
            object_to_append = {"amount":amnt , "description":""}
        else:
            object_to_append = {"amount":amnt , "description":description}

        self.ledger.append(object_to_append)
        # This method should return True if the withdrawal took place
        return True
    else:
        # and False otherwise
        return False

  # A GET_BALANCE method that returns the current balance of the budget
  # category based on the deposits and withdrawals that have occurred.
  def get_balance(self):
    credit = 0
    debit = 0
    for entry in self.ledger:
      ledger_amount = entry["amount"]
      if ledger_amount>=0:
        credit+=ledger_amount
      else:
        debit+=(-1)*ledger_amount
    return (credit-debit)
# A TRANSFER method that accepts an amount and another budget category
# as arguments.
  def transfer(self, amnt, receiving_category):

    # If there are not enough funds, nothing should be added
    # to either ledgers.
    # Check the funds before transferring
    if self.check_funds(amnt) is True:
        # The method should add a withdrawal with the amount and the description
        # "Transfer to [Destination Budget Category]"
        object_to_append_donor = {"amount":-1*amnt,"description":"Transfer to "+receiving_category.name}
        # Amount is given by the object, hence appended to the list
        # while the amount is already deducted
        self.ledger.append(object_to_append_donor)
        # The method should then add a deposit to the other budget category
        # with the amount and the description "Transfer from
        # [Source Budget Category]"
        object_to_append_receiver = {"amount":amnt,"description":"Transfer from "+self.name}
        # Amount is given to the target object, hence appended to its list
        # and then the its amount is incremented by the donation
        receiving_category.ledger.append(object_to_append_receiver)
        # This method should return True if the transfer took place
        return True
    else:
        # and False otherwise
        return False

# A check_funds method that accepts an amount as an argument
  def check_funds(self,amnt):
    # It returns False if the amount is greater than the balance of the
    # budget category
    if amnt<=self.get_balance():
        return True
    else:
    # and returns True otherwise
        return False

  def __str__(self):
    #STEP 1: A title line of 30 characters where the name of the category is
    #        centered in a line of * characters.
    receipt = ""
    len_category_name = len(self.name)
    len_stars = 30-len_category_name
    title_string = '*'*(int(len_stars/2))+self.name+'*'*(int(len_stars/2))
    receipt = ''.join([receipt,title_string])
    # STEP 2:
    # a. A list of the items in the ledger
    for entry in self.ledger:

    # b. Each line should show the description and amount
        ledger_description = entry["description"]
        ledger_amount = entry["amount"]

    # c. The first 23 characters of the description should be displayed,
    #    then the amount.
        len_ledger_description = len(ledger_description)
        if len_ledger_description>23:
            ledger_description = ledger_description[:23]
            len_ledger_description = len(ledger_description)

    # d. The amount should be right aligned, contain two decimal places,
    #    and display a maximum of 7 characters
        ledger_amount = str("{:.2f}".format(ledger_amount))
        len_ledger_amount = len(ledger_amount)
        if len_ledger_amount>7:
            ledger_amount = ledger_amount[0:7]
            len_ledger_amount = len(ledger_amount)

    # alignment: The description should be left aligned and the amount
    #            should be right aligned.
        len_stars = 30-(len_ledger_description+len_ledger_amount)
        entry_string = ledger_description+' '*len_stars+ledger_amount

    # Concatenating entry strings from each iteration into the receipt
        receipt = '\n'.join([receipt,entry_string])

    # e. A line displaying the category total.
    final_amount = str("{:.2f}".format(self.get_balance()))
    # FINAL RECEIPT
    receipt = '\n'.join([receipt,'Total: '+final_amount])
    return receipt

def create_spend_chart(categories):
  # a list to store the names of the categories to be used for x-label
  category_names = list()
  # percentage withdraw for each category
  percentage_withdraw = list()
  # total withdrawl across all the categories for percentage calculation
  total_withdrawl = 0
  
  for a_category in categories:
    # store the name of the category
    category_names.append(a_category.name)
    # initialize the withdrawl for a given category
    withdrawl = 0
    # iterate through all the enteries of the category ledger
    for entry in a_category.ledger:
      # if the amount is deducted but not beacuase of transfer
      if entry["amount"]<0 and entry["description"][:7]!="Transfer":
        # accumulate the withdrawls
        withdrawl+=(-1)*entry["amount"]
    # append the withdrawl to the list of withdrawls
    percentage_withdraw.append(withdrawl)
    # sum all the withdrawls
    total_withdrawl+=withdrawl
    
  # Convert the withdrawl per category to percentages and then to the nearest
  # 10
  for i, withdrawl in enumerate(percentage_withdraw):
    withdrawl = int((withdrawl/total_withdrawl)*100)
    withdrawl = (int(withdrawl/10))*10
    percentage_withdraw[i] = withdrawl
  #--------------------------------------------------------------
  # Calculate x-y plane and the plotting patterns per category
  #           using the calculated percentages
  #--------------------------------------------------------------
  plan = "Percentage spent by category"+'\n'
  y_labels = ['100|',' 90|',' 80|',' 70|',' 60|',' 50|',' 40|',' 30|',' 20|',' 10|','  0|']
  # The maximum percentage by a category. This will be used to run the loop
  # to that value to plot the 'o's
  max_percentage = round(max(percentage_withdraw)/10)
  # The percentages ABOVE the maximum percentage must be appended with SPACES
  # as seen by the "dashes" in the horizontal line above the x-label, 
  # for each category name in the x-label, there are
  # three "dashes", so ONE SPACE after the y-label, and three spaces per 
  # category name and then finally a NEW LINE character, if there are three 
  # categories, following is an example, Food, Clothing, Auto
  #             F               C               A
  # 100|SPACE SPACESPACESPACE SPACESPACESPACE SPACESPACESPACE\n
  for k in range(len(y_labels)-(max_percentage+1)):
    plan = plan+y_labels[k]+' '+' '*(3*len(percentage_withdraw))+'\n'

  # Now iterate in a reverse order from the Maximum percentage until 0
  for i in range(max_percentage+1,0,-1):
    # Pick the y-label of the MAXIMUM percentage, 
    y_label = y_labels[len(y_labels)-i]
    # Toggle the start of the row
    row_start = 1
    for percentage in percentage_withdraw:
      # if it is the start of the row, it should start with the y-label
      if row_start == 1:
        # If the legth of the category name is less than i, just put a SPACE
        # after y-label and a SPACE at the place of the letter
        if round(percentage/10)<i-1:
          y_label = y_label + ' '*1
          y_label = y_label + ' '*1
        else:
        # If the length of the category name is not less than i, put a SPACE
        # after y-label and a 'o'
          y_label = y_label + ' '
          y_label = y_label + 'o'
        plan = plan+y_label
      else:
        # If it is not start of the row, check the length, if it is less,
        # Put a space
        if round(percentage/10)<i-1:
          plan = plan+ ' '*1
        # else put a 'o'
        else:
          plan = plan+'o'
      # Toggle the start of the row to zero
      row_start = 0
      # After each 'o' or a SPACE put TWO SPACES
      plan = plan+' '*2
    # PUT a '\n' at the end of the row
    plan = plan+'\n'

  #--------------------------------------------------------------
  #   Calculate x-label from using the names of the categories
  #--------------------------------------------------------------
  #--------------------------------------------------------------
  #   Calculate x-label from using the names of the categories
  #--------------------------------------------------------------
  # row 1-->  SPACE * 5 'F' SPACE*2 'C' SPACE*2 'A' SPACE*2 'E' SPACE*2
  # row 2-->  SPACE * 5 'O' SPACE*2 'L' SPACE*2 'U' SPACE*2 'N' SPACE*2
  # row 3-->  SPACE * 5 'O' SPACE*2 'O' SPACE*2 'T' SPACE*2 'T' SPACE*2
  # row 4-->  SPACE * 5 'D' SPACE*2 'T' SPACE*2 'O' SPACE*2 'E' SPACE*2
  # row 5-->  SPACE * 5 ' ' SPACE*2 'H' SPACE*2 ' ' SPACE*2 'R' SPACE*2
  # row 6-->  SPACE * 5 ' ' SPACE*2 'I' SPACE*2 ' ' SPACE*2 'T' SPACE*2
  # row 7-->  SPACE * 5 ' ' SPACE*2 'N' SPACE*2 ' ' SPACE*2 'A' SPACE*2
  # row 8-->  SPACE * 5 ' ' SPACE*2 'G' SPACE*2 ' ' SPACE*2 'I' SPACE*2
  # row 9-->  SPACE * 5 ' ' SPACE*2 ' ' SPACE*2 ' ' SPACE*2 'N' SPACE*2
  # row 10--> SPACE * 5 ' ' SPACE*2 ' ' SPACE*2 ' ' SPACE*2 'M' SPACE*2
  # row 11--> SPACE * 5 ' ' SPACE*2 ' ' SPACE*2 ' ' SPACE*2 'E' SPACE*2
  # row 12--> SPACE * 5 ' ' SPACE*2 ' ' SPACE*2 ' ' SPACE*2 'N' SPACE*2
  # row 13--> SPACE * 5 ' ' SPACE*2 ' ' SPACE*2 ' ' SPACE*2 'T' SPACE*2

  x_label = ''
  # Get the category name with maximum length, This will be the total number
  # of rows, while the number of categories will correspond to the total
  # number of columns
  max_len_string = len(max(category_names,key=len))
  # Iterate through every character in category list name, offcourse, this
  # outer loop will run according to the name with maximum length
  for i in range(max_len_string):
    # This is for the first character in a row where we should add 5 SPACES
    row_start = 1
    # Iterate through each category name, and pick ith Character
    for a_name in category_names:
        if row_start==1:
          # If the character comes in the start of the row, append 5
          # spaces
          x_label = x_label+' '*5
        else:
          # If the character is not the first one in the row, just append
          # two spaces which is between two characters
          x_label = x_label+' '*2
        if i<len(a_name):
          # If the ith character exists in the category name, i.e. within
          # the length of the name, append it
          x_label = x_label+a_name[i]
        else:
          # if the variable 'i' exceeds the length of the name, just put
          # an empty space
          x_label = x_label+' '*1
        # Toggle the position variable, to show, that we are no more at the
        # start of the row
        row_start = 0
    # Append two spaces, and then go to the next row, if it is the last row,
    # do not append NEWLINE
    if i<(max_len_string-1):
        x_label = x_label+' '*2+'\n'
    else:
        x_label = x_label+' '*2
  # Finally, make the dashes, FOUR SPACES in the beginning which is for 3-DIGITS and the pipe sign, i.e. "100|", then the dashes are three times the number of categories, PLUS one dash after the PIPE sign,
  end_bars = ' '*4+'-'*(len(categories)*3+1)+'\n'
  # Finally, concatenate, plan, dashes, and x-label
  plan = plan+end_bars+x_label
  return plan