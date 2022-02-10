import numpy as np
from matplotlib import pyplot as plt
import math
import seaborn as sns
from scipy.stats import gaussian_kde
from .errorHandling import *


error = ErrorHandling._handle_error #Creating a simple way to access the errorHandling decorator


# Adding Graph Interactivity With mpdld3 and pygal
#add pyreverse uml diagram

#It is to be noted it was decided that all of the data checking would happen or data retrival.
#This way differnt checking functions wouldn't need to be created for each type of graph, which required differnt types of data.

class Graph(ErrorHandling):
    """This class is a basic Graph object that contains all the relevant attributes of a basic graph

    The Graph class also has get and set methods which should be the only way attributes are accessed or modified of the
    attributes. This class extends the errorHandling class which deals with all the error that each method can generate.
    This class should never be directly accessed. It should be created through other methods

    - **parameters**, **types**, **return**, and **return types**::

        :param data: a list of integer data to be graphed
        :param data_y: a list of integer data that is on the y-axis
        :param data_x: a list of inter data that is on the x-axis
        :param title_x: the title for the x-axis
        :param title_y: the title for the y-axis

    """

    @error #Calling the decorator
    def __init__(self, **kwargs):
        """
        The initializer for the Graph object. Note not all the attributes have to be filled upon object creation.
        They should only be edited when creating a graph or when using the update_vargs() method

        :param kwargs:
            :keyword data: stores the input data to graph defaults to [None]
            :keyword data_y: stores the y-axis data to graph defaults to [None]
            :keyword data_x: stores the x-axis data to graph defaults to [None]
            :keyword title_x: stores the x-axis title defaults to [""]
            :keyword title_y: stores the y-axis title defaults to [""]
            :keyword title_main: stores the main title for the graph defaults to [""]

        :return: a Graph object
        :rtype: object
        """
        self.data = kwargs.get("data")
        self.data_y = kwargs.get("data_y")
        self.data_x = kwargs.get("data_x")
        self.title_x = kwargs.get("title_x") or ""
        self.title_y = kwargs.get("title_y") or ""
        self.title_main = kwargs.get("title_main") or ""
        # print(self.data)

        # data, data_x, data_y, title_x, title_y, title_main

    @error #Calling the decorator
    def get_data(self):
        """
        Method that will check and return Graphs' data attribute

        The method checks if the data in not None and is of type list.

        :return: returns the data attribute
        """
        check_data(data=self.data, name="data", none=True, list=True, exept=False)
        return self.data

    @error #Calling the decorator
    def get_data_y(self):  # Checks Data is None ? Data must be numerical
        """
        Method that will check and return the Graphs' data_y attribute

        The method checks if the data in not None and is of type list.

        :return: returns the data_y attribute
        """
        check_data(data=self.data_y, name="data_y", none=True, list=True, exept=False)
        return self.data_y

    @error #Calling the decorator
    def get_data_x(self):
        """
        Method that will check and return the Graphs' data_x attribute

        The method checks if the data in not None and is of type list.

        :return: returns the data_x attribute
        """
        check_data(data=self.data_x, name="data_x", none=True, list=True, exept=False)
        return self.data_x

    @error #Calling the decorator
    def get_title_x(self):
        """
       Method that will check and return the Graphs' title_x attribute

       The method checks if the the title_x attribute is a non-empty string

       :return: returns the data_x attribute
       """
        return self.title_x

    @error #Calling the decorator
    def get_title_y(self):
        """
       Method that will check and return the Graphs' title_y attribute

       The method checks if the the title_y attribute is a non-empty string

       :return: returns the data_y attribute
       """
        return self.title_y

    @error #Calling the decorator
    def get_title_main(self):
        """
       Method that will check and return the Graphs' title_main attribute

       The method checks if the the title_main attribute is a non-empty string

       :return: returns the data_main attribute
       """
        return self.title_main

    @error #Calling the decorator
    def set_titles(self, ax, title, title_x="", title_y=""):
        """
        Sets the titles of the graph that is being created

        :param ax: the temporary pyplot plot object
        :param title: the main title of the graph
        :param title_y: the y-axis title of the graph defaults to [""]
        :param title_x: the x-axis title of the graph defaults to [""]
        :return: ax pyplot plot object
        """
        ax.set_ylabel(title_y)
        ax.set_xlabel(title_x)
        ax.set_title(title)
        return ax

    @error #Calling the decorator
    def single_data(self):
        if not (self.data is None):
            data = self.data
        elif not (self.data is None):
            data = self.data_x
        elif not (self.data_y is None):
            data = self.data_y
        else:
            raise Exception("No Inputted Data to Graph")
        return data

    @error #Calling the decorator
    def update_vars(self, **kwargs):  # add Excepions Here
        """
        updates the attributes of the graph class
        :param kwargs:
            :keyword data: updates the input data to graph defaults to [self.data]
            :keyword data_y: updates the y-axis data to graph defaults to [self.data_x]
            :keyword data_x: updates the x-axis data to graph defaults to [self.data_y]
            :keyword title_x: updates the x-axis title defaults to [self.title_main]
            :keyword title_y: updates the y-axis title defaults to [self.title_x]
            :keyword title_main: updates the main title for the graph defaults to [self.title_y]

        :return: This method returns nothing
        """
        
        #These Lines essentialy see if new data has been entered, if the data has not the value remains the same
        #as when the Categorical object was intialised 
        self.data = kwargs.get("data") or self.data
        self.data_x = kwargs.get("data_x") or self.data_x
        self.data_y = kwargs.get("data_y") or self.data_y
        self.title_main = kwargs.get("title_main") or self.title_main
        self.title_x = kwargs.get("title_x") or self.title_x
        self.title_y = kwargs.get("title_y") or self.title_y


class Categorical(Graph): #This class extends all of the Graph classes functionality but adds labels
    """
    Categorical graph class that inherits all of the Graph classes' attributes and methods and enables the graphing of
    categorical data. The attributes of the class should never be directly accessed. They should instead be updated
    through the update_vars() method and accessed through the get_... functions

    :param labels: stores the labels use to name the different classes of data
    :param kwargs:

        :keyword data: stores the input data to graph defaults to [None]
        :keyword data_y: stores the y-axis data to graph defaults to [None]
        :keyword data_x: stores the x-axis data to graph defaults to [None]
        :keyword title_x: stores the x-axis title defaults to [""]
        :keyword title_y: stores the y-axis title defaults to [""]
        :keyword title_main: stores the main title for the graph defaults to [""]


    :return: a Categorical object
    :rtype: object


    """
    def __init__(self, labels=None, **kwargs):
        super().__init__(**kwargs) #Call the Graph init method
        self.labels = labels #Add labels as an attribute

    @error #Calling the decorator
    def update_vars(self, **kwargs): #Overwrite the default method inherited to include updating the labels
        """
        Updates the attributes of the categorical Graph object with inputted kwargs

        :param kwargs:
            :keyword data: stores the input data to graph defaults to [None]
            :keyword data_y: stores the y-axis data to graph defaults to [None]
            :keyword data_x: stores the x-axis data to graph defaults to [None]
            :keyword title_x: stores the x-axis title defaults to [""]
            :keyword title_y: stores the y-axis title defaults to [""]
            :keyword title_main: stores the main title for the graph defaults to [""]
            :keyword labels: stores the labels use to name the different classes of data
        :return: Nothing returned
        """
        self.labels = kwargs.get("labels") or self.labels
        Graph.update_vars(self, **kwargs)

    @error #Calling the decorator
    def get_labels(self):
        """
        Checks the labels variable to see if it is not None, print warning and returns the attribute.
        :return: self.labels
        """
        return self.labels

    @error #Calling the decorator
    def graph_bar(self, **kwargs):
        """
        Generates a bar graph from a combination of the data entered and the attributes of the Categorical Object.
        This method will call the update_vars() method with the kwargs inputted.
        :param kwargs:
            :keyword data: stores the input data to graph defaults to [None]
            :keyword title_x: stores the x-axis title defaults to [""]
            :keyword title_y: stores the y-axis title defaults to [""]
            :keyword title_main: stores the main title for the graph defaults to [""]
            :keyword labels: stores the labels use to name the different classes of data
        :return: Nothing is returned
        """
        self.update_vars(**kwargs) #Update the attributes

        #Getting all of the data
        data = self.get_data()
        labels = self.labels
        title_main = self.get_title_main()
        title_x = self.get_title_x()
        title_y = self.get_title_y()

        data_y = np.arange(len(data)) #Create a list of ints the length of data
        fig, ax = plt.subplots()  # create a subplot
        hbars = ax.barh(data_y, data, align='center') #Graph the bar chart

        if not (labels is None): #Check if the labels attribute has been entered
            ax.set_yticks(ticks=data_y)
            ax.set_yticklabels(labels)
        ax.invert_yaxis() #Inverts the graph so that it is a horizontal bar chart
        ax = Graph.set_titles(self, ax, title_main, title_x, title_y) #sets the titles for the chart
        plt.show()

    @error #Calling the decorator
    def graph_pie(self, **kwargs):
        """
        Generates a pie graph using a combination of the data entered and the preset attributes of the Categorical
        class.
        This method will call the update_vars() method with the kwargs inputted.

        :param kwargs:
            :keyword data: stores the input data to graph defaults to [None]
            :keyword title_main: stores the main title for the graph defaults to [""]
        :return: Nothing is returned
        """
        self.update_vars(**kwargs) #Update the attributes

        #Getting the Data
        data = self.get_data()
        labels = self.labels
        title_main = self.get_title_main()
        title_x = self.get_title_x()
        title_y = self.get_title_y()

        total = np.sum(data) #Getting the sum of the data so that percentages can be calculated
        if total != 1: #If the total = 1 then the data is already in the format needed
            for i in range(len(data)):
                data[i] = data[i] / total * 100
        fig, ax = plt.subplots()
        text_args = dict(fontsize=10, weight='bold', color='black') #Create an arguments dictionary for font properties
        ax.pie(data, labels=labels, shadow=True, autopct='%1.1f%%', textprops=text_args) #Create the pie chart
        ax = Graph.set_titles(self, ax, title_main) #Set the titles for the chart
        plt.show()

    @error #Calling the decorator
    def replot(self):
        pass


class Other(Graph): #Class extends the graph class
    def __init__(self, **kwargs):
        super().__init__(**kwargs) #Call the other classes super method

    @error #Calling the decorator
    def graph_scatter(self, **kwargs):
        """
        Generates a scatter graph using a combination of the data entered and the preset attributes of the Categorical
        class.
        This method will call the update_vars() method with the kwargs inputted.

        :param kwargs:
            :keyword data_y: stores the y-axis data to graph defaults to [self.data_y] or [None]
            :keyword data_x: stores the x-axis data to graph defaults to [self.data_x] or [None]
            :keyword title_x: stores the x-axis title defaults to [self.title_x] or [""]
            :keyword title_y: stores the y-axis title defaults to [self.title_y] or [""]
            :keyword title_main: stores the main title for the graph defaults to [self.title_main] or [""]
        """
        #Updating the variables
        self.update_vars(**kwargs)

        #Getting all of the data
        data_x = self.get_data_x()
        data_y = self.get_data_y()
        title_main = self.get_title_main()
        title_x = self.get_title_x()
        title_y = self.get_title_y()

        fig, ax = plt.subplots()
        ax = sns.regplot(x=data_x, y=data_y, line_kws={"color": "r", "alpha": 0.7, "lw": 3}, fit_reg=False) #Create a plot using seaborn
        ax = Graph.set_titles(self, ax, title_main, title_x, title_y) #Set Graph titles
        plt.show()

    @error #Calling the decorator
    def graph_box(self, **kwargs):
        """
        Generates a box plot sing a combination of the data entered and the preset attributes of the Categorical
        class.
        This method will call the update_vars() method with the kwargs inputted.

        :param kwargs:
            :keyword data: stores the input data to graph defaults to [None]
            :keyword title_x: stores the x-axis title defaults to [self.title_x] or [""]
            :keyword title_y: stores the y-axis title defaults to [self.title_y] or [""]
            :keyword title_main: stores the main title for the graph defaults to [self.title_main] or [""]
        :param kwargs:
        :return: Nothing is returned
        """
        #Updates attributes
        self.update_vars(**kwargs)

        #Get required data
        data = self.get_data()
        title_main = self.get_title_main()
        title_x = self.get_title_x()
        title_y = self.get_title_y()

        
        fig, ax = plt.subplots()
        ax = sns.boxplot(x=data) #Create a boxplot using seaborn
        # ax.boxplot(data)
        ax = Graph.set_titles(self, ax, title_main, title_x=title_x)
        plt.show()

    @error #Calling the decorator
    def graph_density(self, fill=False, **kwargs):
        #This solution is taken from here https://www.python-graph-gallery.com/density-chart-matplotlib
        """
            Generates a density plot using a combination of the data entered and the preset attributes of the Categorical
            class.
            This method will call the update_vars() method with the kwargs inputted.

            :param fill: Determines if the graph is shaded in defaults to [False]
            :param kwargs:
                :keyword data: stores the input data to graph defaults to [None]
                :keyword title_x: stores the x-axis title defaults to [self.title_x] or [""]
                :keyword title_y: stores the y-axis title defaults to [self.title_y] or [""]
                :keyword title_main: stores the main title for the graph defaults to [self.title_main] or [""]
            :param kwargs:
            :return: Nothing is returned
        """
        #Updating the attributes
        self.update_vars(**kwargs)

        #Getting required data
        data = self.get_data()
        title_main = self.get_title_main()
        title_x = self.get_title_x()
        title_y = self.get_title_y()

        fig, ax = plt.subplots()
        # Build a "density" function based on the dataset
        # When you give a value from the X axis to this function, it returns the according value on the Y axis
        density = gaussian_kde(data)
        density.covariance_factor = lambda: .25
        density._compute_covariance()

        # Create a vector of 200 values going from 0 to 8:
        length = max(data) - min(data)
        xs = np.linspace(0, math.ceil(length), math.ceil(length * 20))
        # Make the chart
        # We're actually building a line chart where x values are set all along the axis and y value are
        # the corresponding values from the density function
        if fill:
            plt.fill_between(xs, density(xs), color="#69b3a2", alpha=0.4) #Shade under the density curve
        else:
            plt.plot(xs, density(xs)) #Plot the density curve
        ax = Graph.set_titles(self, ax, title_main, title_x, title_y) #Set the graph titles
        plt.show()

    @error #Calling the decorator
    def graph_violin(self, **kwargs):
        """
           Generates a density plot using a combination of the data entered and the preset attributes of the Categorical
           class.
           This method will call the update_vars() method with the kwargs inputted.

           :param kwargs:
                :keyword data: stores the input data to graph defaults to [None]
                :keyword title_x: stores the x-axis title defaults to [self.title_x] or [""]
                :keyword title_y: stores the y-axis title defaults to [self.title_y] or [""]
                :keyword title_main: stores the main title for the graph defaults to [self.title_main] or [""]
           :return: Nothing is returned
       """
        #Update the attributes
        self.update_vars(**kwargs)

        fig, ax = plt.subplots()
        
        #Get the Required data
        data = self.get_data()
        title_main = self.get_title_main()
        title_x = self.get_title_x()
        title_y = self.get_title_y()

        sns.violinplot(y=data) #plot the violin plot
        ax = Graph.set_titles(self, ax, title_main, title_x, title_y) #Set graph titles
        plt.show()

    @error #Calling the decorator
    def graph_loli(self, **kwargs):
        """
           Generates a density plot using a combination of the data entered and the preset attributes of the Categorical
           class.
           This method will call the update_vars() method with the kwargs inputted.

           :param kwargs:
               :keyword data: stores the input data to graph defaults to [None]
               :keyword title_x: stores the x-axis title defaults to [self.title_x] or [""]
               :keyword title_y: stores the y-axis title defaults to [self.title_y] or [""]
               :keyword title_main: stores the main title for the graph defaults to [self.title_main] or [""]
           :return: Nothing is returned
       """
        #Update the attributes
        self.update_vars(**kwargs)

        #Get required data
        data = self.get_data()
        title_main = self.get_title_main()
        title_x = self.get_title_x()
        title_y = self.get_title_y()

        fig, ax = plt.subplots()
        x = range(1,len(data)+1)
        ax.stem(x, data)  #Create a stem plot
        ax = Graph.set_titles(self, ax, title_main, title_y, title_x) #Adding titles to the Graph
        plt.show()

    @error #Calling the decorator
    def graph_line(self):
        pass
