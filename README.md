# Sytlus_snake_game
## The game is mage with 3 basic steps
## 1.To take a template\sample of the stylus
> ### This helps to get imp. information about the stylus i.e., there HSV values(max. and min). The "CAPTURING WINDOW" looks like this:
![Screenshot 2021-10-12 234425](https://user-images.githubusercontent.com/83019850/137132267-dd7d7137-a833-4e91-98a4-fb419112b065.png)
> ### For this we used the OpenCv And its video capturing function.
## 2.To make the basic sanke game :-
> * ### This is done using pygame library.
>  * We just created the list that stores snake body and hurdle ,fruit,snake's head coordinates . And they are displayed on sreen using fuvtions of pygame.
>  * Snakes is moved and its collision and eating of food is checked and score keeps on increasing.
![ezgif-1-69da4e3bc154](https://user-images.githubusercontent.com/83019850/137133655-6e0b1db6-68d0-4201-afa6-ac0ac3f178aa.gif)
> In the above gif Snake is in "GREEEN", fruit is in "White" , and hurdle is in "BLUE".
## 3.To track the movment of stylus and move snake accordingly:-
> * This is the unique part of the game. The sample stylus is been detected and tracked so that the snake can be moved(up,down,right,left).
> * For detection of stylus position : concept of hsv thresholding an concept of conture is used. Using OpenCv fuctions.
> * For detection of direction: Position of stylus in current and the 10th before frame is used.
> * Using this two points slope has been calculated . and applying some thershold conditions direction of stylus is calculated.
## The sample video is given below 


https://user-images.githubusercontent.com/83019850/137156283-92f83305-ae25-4e87-a611-85297025fe72.mp4

